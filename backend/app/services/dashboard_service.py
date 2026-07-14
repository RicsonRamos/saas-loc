from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.contrato import STATUS_ATIVO, Contrato
from app.models.financeiro import (
    STATUS_PAGAMENTO_PAGO,
    STATUS_PAGAMENTO_PENDENTE,
    Despesa,
    Pagamento,
)
from app.models.manutencao import Manutencao
from app.models.multa import STATUS_MULTA_PENDENTE, Multa
from app.models.plano_manutencao import PlanoManutencao
from app.models.veiculo import STATUS_ALUGADO, Veiculo
from app.schemas.dashboard import (
    AlertaOut,
    DashboardKpisOut,
    DashboardResumoOut,
    FinanceiroMensalOut,
    FinanceiroMesOut,
    PagamentosResumoOut,
    VencimentosResumoOut,
)
from app.services import contrato_service, plano_manutencao_service
from app.services.veiculo_service import calcular_status_efetivo

MESES_HISTORICO_FINANCEIRO = 6

ROTULOS_TIPO_PLANO_MANUTENCAO: dict[str, str] = {
    "troca_oleo": "Troca de óleo",
    "troca_filtros": "Troca de filtros",
    "pastilhas_freio": "Pastilhas de freio",
    "pneus": "Pneus",
    "revisao": "Revisão periódica",
    "alinhamento_balanceamento": "Alinhamento e balanceamento",
    "licenciamento": "Licenciamento",
    "seguro": "Seguro",
    "outro": "Manutenção",
}

JANELA_VENCIMENTO_DIAS = 30
JANELA_MANUTENCAO_KM = 500
JANELA_MANUTENCAO_DIAS = 7


def _veiculos_ativos(db: Session) -> list[Veiculo]:
    return list(db.execute(select(Veiculo).where(Veiculo.deleted_at.is_(None))).scalars().all())


def _contar_por_status(veiculos: list[Veiculo]) -> dict[str, int]:
    contagem: dict[str, int] = {}
    for veiculo in veiculos:
        situacao = calcular_status_efetivo(veiculo)
        contagem[situacao] = contagem.get(situacao, 0) + 1
    return contagem


def _contar_vencimentos(veiculos: list[Veiculo], hoje) -> VencimentosResumoOut:
    limite = hoje + timedelta(days=JANELA_VENCIMENTO_DIAS)
    seguro = sum(
        1 for v in veiculos if v.vencimento_seguro and hoje <= v.vencimento_seguro <= limite
    )
    licenciamento = sum(
        1
        for v in veiculos
        if v.vencimento_licenciamento and hoje <= v.vencimento_licenciamento <= limite
    )
    return VencimentosResumoOut(seguro_30_dias=seguro, licenciamento_30_dias=licenciamento)


def _financeiro_do_mes(db: Session, hoje: datetime) -> FinanceiroMesOut:
    receita = db.scalar(
        select(func.coalesce(func.sum(Pagamento.valor), 0)).where(
            Pagamento.status == STATUS_PAGAMENTO_PAGO,
            extract("year", Pagamento.data) == hoje.year,
            extract("month", Pagamento.data) == hoje.month,
        )
    ) or Decimal("0")
    despesas = db.scalar(
        select(func.coalesce(func.sum(Despesa.valor), 0)).where(
            extract("year", Despesa.data) == hoje.year,
            extract("month", Despesa.data) == hoje.month,
        )
    ) or Decimal("0")
    return FinanceiroMesOut(receita=receita, despesas=despesas, lucro=receita - despesas)


def _historico_financeiro(
    db: Session, hoje: date, meses: int = MESES_HISTORICO_FINANCEIRO
) -> list[FinanceiroMensalOut]:
    """Agrega receita/despesa por mês nos últimos `meses` meses (incluindo o atual).

    Duas queries agrupadas por ano/mês (uma para pagamentos pagos, outra para despesas)
    em vez de uma por mês — evita `meses` round-trips redundantes.
    """
    primeiro_mes = (hoje.replace(day=1) - timedelta(days=30 * (meses - 1))).replace(day=1)

    receitas_por_mes: dict[tuple[int, int], Decimal] = {}
    linhas_receita = db.execute(
        select(
            extract("year", Pagamento.data).label("ano"),
            extract("month", Pagamento.data).label("mes"),
            func.coalesce(func.sum(Pagamento.valor), 0).label("total"),
        )
        .where(Pagamento.status == STATUS_PAGAMENTO_PAGO, Pagamento.data >= primeiro_mes)
        .group_by("ano", "mes")
    ).all()
    for ano, mes, total in linhas_receita:
        receitas_por_mes[(int(ano), int(mes))] = Decimal(total)

    despesas_por_mes: dict[tuple[int, int], Decimal] = {}
    linhas_despesa = db.execute(
        select(
            extract("year", Despesa.data).label("ano"),
            extract("month", Despesa.data).label("mes"),
            func.coalesce(func.sum(Despesa.valor), 0).label("total"),
        )
        .where(Despesa.data >= primeiro_mes)
        .group_by("ano", "mes")
    ).all()
    for ano, mes, total in linhas_despesa:
        despesas_por_mes[(int(ano), int(mes))] = Decimal(total)

    historico: list[FinanceiroMensalOut] = []
    cursor = primeiro_mes
    for _ in range(meses):
        chave = (cursor.year, cursor.month)
        receita = receitas_por_mes.get(chave, Decimal("0"))
        despesa = despesas_por_mes.get(chave, Decimal("0"))
        historico.append(
            FinanceiroMensalOut(
                mes=f"{cursor.year:04d}-{cursor.month:02d}",
                receita=receita,
                despesas=despesa,
                lucro=receita - despesa,
            )
        )
        cursor = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)

    return historico


def _contratos_ativos_count(db: Session) -> int:
    return db.scalar(select(func.count()).where(Contrato.status == STATUS_ATIVO)) or 0


def _taxa_ocupacao(veiculos_por_status: dict[str, int], total_veiculos: int) -> float:
    if total_veiculos == 0:
        return 0.0
    alugados = veiculos_por_status.get(STATUS_ALUGADO, 0)
    return round(alugados / total_veiculos * 100, 1)


def _pagamentos_pendentes_e_atrasados(
    db: Session, hoje: date
) -> tuple[PagamentosResumoOut, PagamentosResumoOut]:
    pendentes = db.execute(
        select(func.count(), func.coalesce(func.sum(Pagamento.valor), 0)).where(
            Pagamento.status == STATUS_PAGAMENTO_PENDENTE
        )
    ).one()
    atrasados = db.execute(
        select(func.count(), func.coalesce(func.sum(Pagamento.valor), 0)).where(
            Pagamento.status == STATUS_PAGAMENTO_PENDENTE,
            func.date(Pagamento.data) < hoje,
        )
    ).one()
    return (
        PagamentosResumoOut(quantidade=pendentes[0], valor=Decimal(pendentes[1])),
        PagamentosResumoOut(quantidade=atrasados[0], valor=Decimal(atrasados[1])),
    )


def _montar_kpis(
    db: Session,
    hoje: date,
    veiculos_por_status: dict[str, int],
    total_veiculos: int,
    financeiro_mes: FinanceiroMesOut | None,
) -> DashboardKpisOut:
    contratos_ativos = _contratos_ativos_count(db)
    pendentes, atrasados = _pagamentos_pendentes_e_atrasados(db, hoje)

    ticket_medio = None
    receita_por_veiculo = None
    if financeiro_mes is not None:
        if contratos_ativos > 0:
            ticket_medio = financeiro_mes.receita / contratos_ativos
        if total_veiculos > 0:
            receita_por_veiculo = financeiro_mes.receita / total_veiculos

    return DashboardKpisOut(
        contratos_ativos=contratos_ativos,
        taxa_ocupacao=_taxa_ocupacao(veiculos_por_status, total_veiculos),
        ticket_medio=ticket_medio,
        receita_por_veiculo=receita_por_veiculo,
        pagamentos_pendentes=pendentes,
        pagamentos_atrasados=atrasados,
    )


def _alertas_documentos(veiculos: list[Veiculo], hoje) -> list[AlertaOut]:
    alertas: list[AlertaOut] = []
    for veiculo in veiculos:
        for vencimento, rotulo, tipo_vencido, tipo_vencendo in (
            (veiculo.vencimento_seguro, "Seguro", "seguro_vencido", "seguro_vencendo"),
            (
                veiculo.vencimento_licenciamento,
                "Licenciamento",
                "licenciamento_vencido",
                "licenciamento_vencendo",
            ),
        ):
            if vencimento is None:
                continue
            dias = (vencimento - hoje).days
            if dias < 0:
                alertas.append(
                    AlertaOut(
                        tipo=tipo_vencido,
                        mensagem=f"{rotulo} do veículo {veiculo.placa} está vencido.",
                        prioridade="critico",
                        veiculo_id=veiculo.id,
                        veiculo_placa=veiculo.placa,
                    )
                )
            elif dias <= JANELA_VENCIMENTO_DIAS:
                prazo = "amanhã" if dias == 1 else ("hoje" if dias == 0 else f"em {dias} dias")
                alertas.append(
                    AlertaOut(
                        tipo=tipo_vencendo,
                        mensagem=f"{rotulo} do veículo {veiculo.placa} vence {prazo}.",
                        prioridade="atencao",
                        veiculo_id=veiculo.id,
                        veiculo_placa=veiculo.placa,
                    )
                )
    return alertas


def _alertas_manutencao(db: Session, veiculos: list[Veiculo], hoje) -> list[AlertaOut]:
    veiculos_por_id = {v.id: v for v in veiculos}
    ultimas_por_veiculo: dict = {}
    manutencoes = (
        db.execute(
            select(Manutencao)
            .where(Manutencao.deleted_at.is_(None))
            .order_by(Manutencao.data.desc())
        )
        .scalars()
        .all()
    )
    for manutencao in manutencoes:
        ultimas_por_veiculo.setdefault(manutencao.veiculo_id, manutencao)

    alertas: list[AlertaOut] = []
    for veiculo_id, manutencao in ultimas_por_veiculo.items():
        veiculo = veiculos_por_id.get(veiculo_id)
        if veiculo is None:
            continue
        if manutencao.proxima_manutencao_km is not None:
            faltam_km = manutencao.proxima_manutencao_km - veiculo.km_atual
            if faltam_km <= JANELA_MANUTENCAO_KM:
                alertas.append(
                    AlertaOut(
                        tipo="revisao_km",
                        mensagem=(
                            f"Veículo {veiculo.placa} precisa de revisão em "
                            f"{max(faltam_km, 0)} km."
                        ),
                        prioridade="critico" if faltam_km <= 0 else "atencao",
                        veiculo_id=veiculo.id,
                        veiculo_placa=veiculo.placa,
                    )
                )
        if manutencao.proxima_manutencao_data is not None:
            dias = (manutencao.proxima_manutencao_data - hoje).days
            if dias <= JANELA_MANUTENCAO_DIAS:
                alertas.append(
                    AlertaOut(
                        tipo="revisao_data",
                        mensagem=f"Veículo {veiculo.placa} tem revisão agendada em breve.",
                        prioridade="critico" if dias <= 0 else "atencao",
                        veiculo_id=veiculo.id,
                        veiculo_placa=veiculo.placa,
                    )
                )
    return alertas


def _alertas_devolucao_hoje(db: Session, hoje) -> list[AlertaOut]:
    contratos = (
        db.execute(
            select(Contrato, Veiculo)
            .join(Veiculo, Veiculo.id == Contrato.veiculo_id)
            .where(Contrato.status == STATUS_ATIVO)
        )
        .all()
    )
    alertas: list[AlertaOut] = []
    for contrato, veiculo in contratos:
        if contrato.data_fim_prevista.date() == hoje:
            alertas.append(
                AlertaOut(
                    tipo="devolucao_hoje",
                    mensagem=f"Devolução do veículo {veiculo.placa} prevista para hoje.",
                    prioridade="atencao",
                    veiculo_id=veiculo.id,
                    veiculo_placa=veiculo.placa,
                )
            )
    return alertas


def _alertas_franquia_km(db: Session, hoje) -> list[AlertaOut]:
    contratos = (
        db.execute(
            select(Contrato, Veiculo)
            .join(Veiculo, Veiculo.id == Contrato.veiculo_id)
            .where(Contrato.status == STATUS_ATIVO, Contrato.km_contratado_mensal.isnot(None))
        )
        .all()
    )
    alertas: list[AlertaOut] = []
    for contrato, veiculo in contratos:
        consumo = contrato_service.calcular_consumo_km(contrato, veiculo, hoje)
        if consumo is None or consumo.nivel == "normal" or consumo.percentual is None:
            continue
        alertas.append(
            AlertaOut(
                tipo="franquia_km_excedida" if consumo.nivel == "critico" else "franquia_km_proxima",
                mensagem=(
                    f"Veículo {veiculo.placa} já rodou {consumo.percentual:.0f}% da "
                    "franquia de km contratada."
                ),
                prioridade=consumo.nivel,
                veiculo_id=veiculo.id,
                veiculo_placa=veiculo.placa,
            )
        )
    return alertas


def _alertas_planos_manutencao(db: Session, veiculos: list[Veiculo], hoje) -> list[AlertaOut]:
    veiculos_por_id = {v.id: v for v in veiculos}
    planos = (
        db.execute(
            select(PlanoManutencao).where(
                PlanoManutencao.ativo.is_(True), PlanoManutencao.deleted_at.is_(None)
            )
        )
        .scalars()
        .all()
    )

    alertas: list[AlertaOut] = []
    for plano in planos:
        veiculo = veiculos_por_id.get(plano.veiculo_id)
        if veiculo is None:
            continue
        prioridade, faltam_km, _faltam_dias = plano_manutencao_service.calcular_status(
            plano, veiculo, hoje
        )
        if prioridade == "normal":
            continue
        rotulo = ROTULOS_TIPO_PLANO_MANUTENCAO.get(plano.tipo, plano.tipo)
        situacao = "vencida" if prioridade == "critico" else "próxima do vencimento"
        alertas.append(
            AlertaOut(
                tipo=f"manutencao_{plano.tipo}",
                mensagem=f"{rotulo} do veículo {veiculo.placa} está {situacao}.",
                prioridade=prioridade,
                veiculo_id=veiculo.id,
                veiculo_placa=veiculo.placa,
            )
        )
    return alertas


def _alertas_multas_pendentes(db: Session, veiculos: list[Veiculo]) -> list[AlertaOut]:
    veiculos_por_id = {v.id: v for v in veiculos}
    multas_pendentes = (
        db.execute(
            select(Multa).where(
                Multa.status == STATUS_MULTA_PENDENTE, Multa.deleted_at.is_(None)
            )
        )
        .scalars()
        .all()
    )

    contagem_por_veiculo: dict = {}
    for multa in multas_pendentes:
        contagem_por_veiculo[multa.veiculo_id] = contagem_por_veiculo.get(multa.veiculo_id, 0) + 1

    alertas: list[AlertaOut] = []
    for veiculo_id, total in contagem_por_veiculo.items():
        veiculo = veiculos_por_id.get(veiculo_id)
        if veiculo is None:
            continue
        alertas.append(
            AlertaOut(
                tipo="multas_pendentes",
                mensagem=f"Veículo {veiculo.placa} tem {total} multa(s) pendente(s).",
                prioridade="atencao",
                veiculo_id=veiculo.id,
                veiculo_placa=veiculo.placa,
            )
        )
    return alertas


def resumo(db: Session, incluir_financeiro: bool) -> DashboardResumoOut:
    agora = datetime.now(UTC)
    hoje = agora.date()
    veiculos = _veiculos_ativos(db)
    veiculos_por_status = _contar_por_status(veiculos)

    alertas = [
        *_alertas_documentos(veiculos, hoje),
        *_alertas_manutencao(db, veiculos, hoje),
        *_alertas_devolucao_hoje(db, hoje),
        *_alertas_franquia_km(db, hoje),
        *_alertas_planos_manutencao(db, veiculos, hoje),
        *_alertas_multas_pendentes(db, veiculos),
    ]

    financeiro_mes = _financeiro_do_mes(db, agora) if incluir_financeiro else None

    return DashboardResumoOut(
        veiculos_por_status=veiculos_por_status,
        vencimentos=_contar_vencimentos(veiculos, hoje),
        financeiro_mes=financeiro_mes,
        financeiro_historico=_historico_financeiro(db, hoje) if incluir_financeiro else None,
        kpis=_montar_kpis(db, hoje, veiculos_por_status, len(veiculos), financeiro_mes),
        alertas=alertas,
    )
