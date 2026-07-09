import secrets
import uuid
from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria, serializar_campos
from app.exceptions import NotFoundError
from app.models.abastecimento import Abastecimento
from app.models.cliente import Cliente
from app.models.contrato import STATUS_ATIVO, STATUS_ENCERRADO, Contrato
from app.models.dano import Dano
from app.models.financeiro import STATUS_PAGAMENTO_PAGO, Despesa, Pagamento
from app.models.leitura_km import LeituraKm
from app.models.manutencao import Manutencao
from app.models.multa import Multa
from app.models.sinistro import Sinistro
from app.models.veiculo import (
    STATUS_DISPONIVEL,
    STATUS_LICENCIAMENTO_VENCIDO,
    STATUS_SEGURO_VENCIDO,
    Veiculo,
)
from app.schemas.dano import DanoOut
from app.schemas.multa import MultaOut
from app.schemas.sinistro import SinistroOut
from app.schemas.veiculo import (
    EventoKmOut,
    HistoricoContratoOut,
    HistoricoDespesaOut,
    HistoricoManutencaoOut,
    HistoricoVeiculoOut,
    IndicadoresVeiculoOut,
    VeiculoCreate,
    VeiculoUpdate,
)
from app.services.common import paginar


def calcular_status_efetivo(veiculo: Veiculo, hoje: date | None = None) -> str:
    """Deriva a situação exibida do veículo a partir do status operacional + vencimentos.

    Só sobrepõe quando o status bruto é "disponivel": um veículo alugado, em
    manutenção, sinistrado etc. mantém seu status operacional mesmo com
    documentação vencida — a sobreposição automática só faz sentido para o
    caso em que o veículo seria oferecido para locação.
    """
    if veiculo.status != STATUS_DISPONIVEL:
        return veiculo.status

    referencia = hoje or datetime.now(UTC).date()
    if veiculo.vencimento_licenciamento and veiculo.vencimento_licenciamento < referencia:
        return STATUS_LICENCIAMENTO_VENCIDO
    if veiculo.vencimento_seguro and veiculo.vencimento_seguro < referencia:
        return STATUS_SEGURO_VENCIDO
    return veiculo.status


def criar(
    db: Session,
    payload: VeiculoCreate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Veiculo:
    veiculo = Veiculo(**payload.model_dump())
    db.add(veiculo)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="veiculo",
        entidade_id=veiculo.id,
        dados_novos=serializar_campos(payload.model_dump()),
        ip=ip,
    )
    db.commit()
    db.refresh(veiculo)
    return veiculo


def listar(
    db: Session,
    page: int,
    limit: int,
    status: str | None = None,
    busca: str | None = None,
    marca: str | None = None,
    categoria: str | None = None,
    ano: int | None = None,
    filial_id: str | None = None,
) -> tuple[list[Veiculo], int]:
    stmt = select(Veiculo).where(Veiculo.deleted_at.is_(None)).order_by(Veiculo.created_at.desc())
    if status:
        stmt = stmt.where(Veiculo.status == status)
    if busca:
        termo = f"%{busca}%"
        stmt = stmt.where(
            or_(
                Veiculo.placa.ilike(termo),
                Veiculo.modelo.ilike(termo),
                Veiculo.chassi.ilike(termo),
            )
        )
    if marca:
        stmt = stmt.where(Veiculo.marca == marca)
    if categoria:
        stmt = stmt.where(Veiculo.categoria == categoria)
    if ano:
        stmt = stmt.where(Veiculo.ano == ano)
    if filial_id:
        stmt = stmt.where(Veiculo.filial_id == filial_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, veiculo_id: uuid.UUID) -> Veiculo:
    veiculo = db.get(Veiculo, veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def contrato_ativo_do_veiculo(db: Session, veiculo_id: uuid.UUID) -> Contrato | None:
    return db.scalar(
        select(Contrato).where(Contrato.veiculo_id == veiculo_id, Contrato.status == STATUS_ATIVO)
    )


def obter_por_codigo_publico(db: Session, codigo_publico: str) -> Veiculo:
    veiculo = db.scalar(
        select(Veiculo).where(
            Veiculo.codigo_publico == codigo_publico, Veiculo.deleted_at.is_(None)
        )
    )
    if veiculo is None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def regenerar_codigo_publico(
    db: Session,
    veiculo_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Veiculo:
    """Invalida o código público atual (ex.: QR extraviado) sem afetar `id`/FKs."""
    veiculo = obter(db, veiculo_id)
    codigo_anterior = veiculo.codigo_publico
    veiculo.codigo_publico = secrets.token_urlsafe(16)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="veiculo",
        entidade_id=veiculo.id,
        dados_anteriores={"codigo_publico": codigo_anterior},
        dados_novos={"codigo_publico": veiculo.codigo_publico},
        descricao="Código público do QR regenerado.",
        ip=ip,
    )
    db.commit()
    db.refresh(veiculo)
    return veiculo


def atualizar(
    db: Session,
    veiculo_id: uuid.UUID,
    payload: VeiculoUpdate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Veiculo:
    veiculo = obter(db, veiculo_id)
    campos_alterados = payload.model_dump(exclude_unset=True)
    dados_anteriores = {campo: getattr(veiculo, campo) for campo in campos_alterados}
    for campo, valor in campos_alterados.items():
        setattr(veiculo, campo, valor)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="veiculo",
        entidade_id=veiculo.id,
        dados_anteriores=serializar_campos(dados_anteriores),
        dados_novos=serializar_campos(campos_alterados),
        ip=ip,
    )
    db.commit()
    db.refresh(veiculo)
    return veiculo


def remover(
    db: Session,
    veiculo_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    veiculo = obter(db, veiculo_id)
    veiculo.deleted_at = datetime.now(UTC)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="excluir",
        entidade="veiculo",
        entidade_id=veiculo.id,
        ip=ip,
    )
    db.commit()


def _montar_eventos_km(
    contratos: list[tuple[Contrato, str]],
    manutencoes: list[Manutencao],
    abastecimentos: list[Abastecimento],
    leituras_km: list[LeituraKm] | None = None,
) -> list[EventoKmOut]:
    eventos: list[EventoKmOut] = []
    for contrato, _cliente_nome in contratos:
        if contrato.km_inicio is not None:
            eventos.append(
                EventoKmOut(
                    data=contrato.data_inicio,
                    km=contrato.km_inicio,
                    origem="contrato_saida",
                    descricao="KM de saída na locação",
                )
            )
        if contrato.km_final is not None and contrato.data_fim_real is not None:
            eventos.append(
                EventoKmOut(
                    data=contrato.data_fim_real,
                    km=contrato.km_final,
                    origem="contrato_devolucao",
                    descricao="KM na devolução da locação",
                )
            )
    for manutencao in manutencoes:
        eventos.append(
            EventoKmOut(
                data=manutencao.data,
                km=manutencao.km,
                origem="manutencao",
                descricao="Registrado em manutenção",
            )
        )
    for abastecimento in abastecimentos:
        eventos.append(
            EventoKmOut(
                data=abastecimento.data,
                km=abastecimento.km,
                origem="abastecimento",
                descricao="Registrado em abastecimento",
            )
        )
    for leitura in leituras_km or []:
        eventos.append(
            EventoKmOut(
                data=leitura.data_leitura,
                km=leitura.km,
                origem="leitura_km",
                descricao="Atualização periódica de quilometragem",
            )
        )
    eventos.sort(key=lambda e: e.data, reverse=True)
    return eventos


def _calcular_indicadores(
    db: Session,
    veiculo: Veiculo,
    contratos: list[tuple[Contrato, str]],
    manutencoes: list[Manutencao],
    despesas: list[Despesa],
    abastecimentos: list[Abastecimento],
) -> IndicadoresVeiculoOut:
    hoje = datetime.now(UTC).date()

    receita_total = (
        db.scalar(
            select(func.coalesce(func.sum(Pagamento.valor), 0))
            .join(Contrato, Contrato.id == Pagamento.contrato_id)
            .where(Contrato.veiculo_id == veiculo.id, Pagamento.status == STATUS_PAGAMENTO_PAGO)
        )
        or Decimal("0")
    )

    custo_manutencao = sum((m.custo for m in manutencoes), Decimal("0"))
    custo_despesas = sum((d.valor for d in despesas), Decimal("0"))
    custo_abastecimento = sum((a.valor for a in abastecimentos), Decimal("0"))
    custo_total = custo_manutencao + custo_despesas + custo_abastecimento

    data_referencia = veiculo.data_entrada_frota or veiculo.created_at.date()
    dias_desde_entrada = max(1, (hoje - data_referencia).days)

    dias_locado = 0
    for contrato, _cliente_nome in contratos:
        if contrato.status not in (STATUS_ATIVO, STATUS_ENCERRADO):
            continue
        fim = contrato.data_fim_real.date() if contrato.data_fim_real else hoje
        inicio = contrato.data_inicio.date()
        dias_locado += max(0, (fim - inicio).days) or 1

    dias_locado = min(dias_locado, dias_desde_entrada)
    dias_parado = max(0, dias_desde_entrada - dias_locado)
    taxa_utilizacao = round(Decimal(dias_locado) / Decimal(dias_desde_entrada) * 100, 2)

    km_rodado = veiculo.km_atual - (veiculo.km_inicial or 0)
    custo_por_km = round(custo_total / km_rodado, 2) if km_rodado > 0 else None

    return IndicadoresVeiculoOut(
        receita_total=receita_total,
        custo_total=custo_total,
        lucro=receita_total - custo_total,
        custo_por_km=custo_por_km,
        dias_desde_entrada=dias_desde_entrada,
        dias_locado=dias_locado,
        dias_parado=dias_parado,
        taxa_utilizacao=taxa_utilizacao,
    )


def historico(db: Session, veiculo_id: uuid.UUID) -> HistoricoVeiculoOut:
    veiculo = obter(db, veiculo_id)

    contratos = db.execute(
        select(Contrato, Cliente.nome)
        .join(Cliente, Cliente.id == Contrato.cliente_id)
        .where(Contrato.veiculo_id == veiculo_id)
        .order_by(Contrato.data_inicio.desc())
    ).all()

    manutencoes = (
        db.execute(
            select(Manutencao)
            .where(Manutencao.veiculo_id == veiculo_id, Manutencao.deleted_at.is_(None))
            .order_by(Manutencao.data.desc())
        )
        .scalars()
        .all()
    )

    despesas = (
        db.execute(
            select(Despesa)
            .where(Despesa.veiculo_id == veiculo_id, Despesa.deleted_at.is_(None))
            .order_by(Despesa.data.desc())
        )
        .scalars()
        .all()
    )

    multas = (
        db.execute(
            select(Multa)
            .where(Multa.veiculo_id == veiculo_id, Multa.deleted_at.is_(None))
            .order_by(Multa.data.desc())
        )
        .scalars()
        .all()
    )

    sinistros = (
        db.execute(
            select(Sinistro)
            .where(Sinistro.veiculo_id == veiculo_id, Sinistro.deleted_at.is_(None))
            .order_by(Sinistro.data.desc())
        )
        .scalars()
        .all()
    )

    danos = (
        db.execute(
            select(Dano)
            .where(Dano.veiculo_id == veiculo_id, Dano.deleted_at.is_(None))
            .order_by(Dano.data.desc())
        )
        .scalars()
        .all()
    )

    abastecimentos = (
        db.execute(
            select(Abastecimento)
            .where(Abastecimento.veiculo_id == veiculo_id, Abastecimento.deleted_at.is_(None))
            .order_by(Abastecimento.data.desc())
        )
        .scalars()
        .all()
    )

    leituras_km = (
        db.execute(
            select(LeituraKm)
            .where(LeituraKm.veiculo_id == veiculo_id, LeituraKm.deleted_at.is_(None))
            .order_by(LeituraKm.data_leitura.desc())
        )
        .scalars()
        .all()
    )

    return HistoricoVeiculoOut(
        contratos=[
            HistoricoContratoOut(
                id=contrato.id,
                cliente_id=contrato.cliente_id,
                cliente_nome=cliente_nome,
                data_inicio=contrato.data_inicio,
                data_fim_prevista=contrato.data_fim_prevista,
                data_fim_real=contrato.data_fim_real,
                status=contrato.status,
                valor_diaria=contrato.valor_diaria,
                km_inicio=contrato.km_inicio,
                km_final=contrato.km_final,
            )
            for contrato, cliente_nome in contratos
        ],
        manutencoes=[HistoricoManutencaoOut.model_validate(m) for m in manutencoes],
        despesas=[HistoricoDespesaOut.model_validate(d) for d in despesas],
        multas=[MultaOut.model_validate(m) for m in multas],
        sinistros=[SinistroOut.model_validate(s) for s in sinistros],
        danos=[DanoOut.model_validate(d) for d in danos],
        eventos_km=_montar_eventos_km(contratos, manutencoes, abastecimentos, leituras_km),
        indicadores=_calcular_indicadores(
            db, veiculo, contratos, manutencoes, despesas, abastecimentos
        ),
    )
