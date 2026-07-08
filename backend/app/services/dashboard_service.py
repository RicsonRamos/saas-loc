from datetime import UTC, datetime, timedelta
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.contrato import STATUS_ATIVO, Contrato
from app.models.financeiro import STATUS_PAGAMENTO_PAGO, Despesa, Pagamento
from app.models.manutencao import Manutencao
from app.models.veiculo import Veiculo
from app.schemas.dashboard import (
    AlertaOut,
    DashboardResumoOut,
    FinanceiroMesOut,
    VencimentosResumoOut,
)
from app.services.veiculo_service import calcular_status_efetivo

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
                    veiculo_id=veiculo.id,
                    veiculo_placa=veiculo.placa,
                )
            )
    return alertas


def resumo(db: Session, incluir_financeiro: bool) -> DashboardResumoOut:
    agora = datetime.now(UTC)
    hoje = agora.date()
    veiculos = _veiculos_ativos(db)

    alertas = [
        *_alertas_documentos(veiculos, hoje),
        *_alertas_manutencao(db, veiculos, hoje),
        *_alertas_devolucao_hoje(db, hoje),
    ]

    return DashboardResumoOut(
        veiculos_por_status=_contar_por_status(veiculos),
        vencimentos=_contar_vencimentos(veiculos, hoje),
        financeiro_mes=_financeiro_do_mes(db, agora) if incluir_financeiro else None,
        alertas=alertas,
    )
