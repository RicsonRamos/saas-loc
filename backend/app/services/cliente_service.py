import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.cliente import Cliente
from app.models.contrato import STATUS_ATIVO, STATUS_ENCERRADO, Contrato
from app.models.dano import Dano
from app.models.financeiro import (
    STATUS_PAGAMENTO_ESTORNADO,
    STATUS_PAGAMENTO_PAGO,
    STATUS_PAGAMENTO_PENDENTE,
    Pagamento,
)
from app.models.multa import STATUS_MULTA_PENDENTE, Multa
from app.models.sinistro import Sinistro
from app.models.veiculo import Veiculo
from app.schemas.cliente import (
    AlertaClienteOut,
    ClienteCreate,
    ClienteUpdate,
    FichaClienteOut,
    HistoricoClienteOut,
    HistoricoLocacaoClienteOut,
    ResumoFinanceiroClienteOut,
)
from app.schemas.dano import DanoOut
from app.schemas.multa import MultaOut
from app.schemas.sinistro import SinistroOut
from app.services.common import paginar

JANELA_CNH_DIAS = 30


def criar(db: Session, payload: ClienteCreate) -> Cliente:
    cliente = Cliente(**payload.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar(
    db: Session, page: int, limit: int, busca: str | None = None
) -> tuple[list[Cliente], int]:
    stmt = select(Cliente).where(Cliente.deleted_at.is_(None)).order_by(Cliente.created_at.desc())
    if busca:
        termo = f"%{busca}%"
        stmt = stmt.where(
            or_(
                Cliente.nome.ilike(termo),
                Cliente.documento.ilike(termo),
                Cliente.telefone.ilike(termo),
            )
        )
    return paginar(db, stmt, page, limit)


def obter(db: Session, cliente_id: uuid.UUID) -> Cliente:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None or cliente.deleted_at is not None:
        raise NotFoundError("Cliente não encontrado.")
    return cliente


def atualizar(db: Session, cliente_id: uuid.UUID, payload: ClienteUpdate) -> Cliente:
    cliente = obter(db, cliente_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


def remover(db: Session, cliente_id: uuid.UUID) -> None:
    cliente = obter(db, cliente_id)
    cliente.deleted_at = datetime.now(UTC)
    db.commit()


def _calcular_avaliacao(
    locacoes_realizadas: int,
    teve_atraso_devolucao: bool,
    tem_pendencia_em_aberto: bool,
    tem_multas: bool,
    tem_sinistros: bool,
) -> int:
    """Heurística de 1 a 5 estrelas com base em pontualidade, pendências,
    volume de locações, multas e sinistros. Ainda não considera danos leves
    (arranhões etc.) nem tempo como cliente — refinar quando fizer sentido.
    """
    if locacoes_realizadas == 0:
        return 3

    estrelas = 5
    if teve_atraso_devolucao:
        estrelas -= 1
    if tem_pendencia_em_aberto:
        estrelas -= 1
    if tem_multas:
        estrelas -= 1
    if tem_sinistros:
        estrelas -= 1
    return max(1, min(5, estrelas))


def historico(db: Session, cliente_id: uuid.UUID) -> HistoricoClienteOut:
    cliente = obter(db, cliente_id)
    hoje = datetime.now(UTC).date()

    contratos = db.execute(
        select(Contrato, Veiculo)
        .join(Veiculo, Veiculo.id == Contrato.veiculo_id)
        .where(Contrato.cliente_id == cliente_id)
        .order_by(Contrato.data_inicio.desc())
    ).all()

    pagamentos = (
        db.execute(
            select(Pagamento)
            .join(Contrato, Contrato.id == Pagamento.contrato_id)
            .where(Contrato.cliente_id == cliente_id)
        )
        .scalars()
        .all()
    )

    total_pago = sum(
        (p.valor for p in pagamentos if p.status == STATUS_PAGAMENTO_PAGO), Decimal("0")
    )
    total_pendente = sum(
        (p.valor for p in pagamentos if p.status == STATUS_PAGAMENTO_PENDENTE), Decimal("0")
    )
    total_estornado = sum(
        (p.valor for p in pagamentos if p.status == STATUS_PAGAMENTO_ESTORNADO), Decimal("0")
    )

    locacoes_realizadas = sum(
        1 for contrato, _ in contratos if contrato.status in (STATUS_ATIVO, STATUS_ENCERRADO)
    )
    contrato_atual = next((c for c, _ in contratos if c.status == STATUS_ATIVO), None)
    veiculo_atual = next((v for c, v in contratos if c.status == STATUS_ATIVO), None)

    teve_atraso_devolucao = any(
        contrato.status == STATUS_ENCERRADO
        and contrato.data_fim_real is not None
        and contrato.data_fim_real > contrato.data_fim_prevista
        for contrato, _ in contratos
    )

    alertas: list[AlertaClienteOut] = []
    if cliente.cnh_vencimento is not None:
        dias = (cliente.cnh_vencimento - hoje).days
        if dias < 0:
            alertas.append(AlertaClienteOut(tipo="cnh_vencida", mensagem="CNH está vencida."))
        elif dias <= JANELA_CNH_DIAS:
            prazo = "amanhã" if dias == 1 else ("hoje" if dias == 0 else f"em {dias} dias")
            alertas.append(
                AlertaClienteOut(tipo="cnh_vencendo", mensagem=f"CNH vence {prazo}.")
            )
    if total_pendente > 0:
        alertas.append(
            AlertaClienteOut(
                tipo="pendencia_financeira",
                mensagem=f"Cliente possui {total_pendente} em pagamentos pendentes.",
            )
        )
    if contrato_atual is not None and contrato_atual.data_fim_prevista.date() < hoje:
        alertas.append(
            AlertaClienteOut(tipo="contrato_em_atraso", mensagem="Devolução está em atraso.")
        )

    multas = (
        db.execute(
            select(Multa)
            .where(Multa.cliente_id == cliente_id, Multa.deleted_at.is_(None))
            .order_by(Multa.data.desc())
        )
        .scalars()
        .all()
    )
    sinistros = (
        db.execute(
            select(Sinistro)
            .where(Sinistro.cliente_id == cliente_id, Sinistro.deleted_at.is_(None))
            .order_by(Sinistro.data.desc())
        )
        .scalars()
        .all()
    )
    danos = (
        db.execute(
            select(Dano)
            .where(Dano.cliente_id == cliente_id, Dano.deleted_at.is_(None))
            .order_by(Dano.data.desc())
        )
        .scalars()
        .all()
    )

    multas_pendentes = [m for m in multas if m.status == STATUS_MULTA_PENDENTE]
    if multas_pendentes:
        alertas.append(
            AlertaClienteOut(
                tipo="multas_pendentes",
                mensagem=f"Cliente possui {len(multas_pendentes)} multa(s) pendente(s).",
            )
        )

    ficha = FichaClienteOut(
        status=cliente.status,
        cnh_categoria=cliente.cnh_categoria,
        cnh_vencimento=cliente.cnh_vencimento,
        locacoes_realizadas=locacoes_realizadas,
        locacao_atual=contrato_atual is not None,
        veiculo_atual_placa=veiculo_atual.placa if veiculo_atual else None,
        veiculo_atual_modelo=veiculo_atual.modelo if veiculo_atual else None,
        valor_total_gasto=total_pago,
        pendencias=total_pendente,
        avaliacao_estrelas=_calcular_avaliacao(
            locacoes_realizadas,
            teve_atraso_devolucao,
            total_pendente > 0,
            len(multas) > 0,
            len(sinistros) > 0,
        ),
    )

    return HistoricoClienteOut(
        ficha=ficha,
        locacoes=[
            HistoricoLocacaoClienteOut(
                id=contrato.id,
                veiculo_id=veiculo.id,
                veiculo_placa=veiculo.placa,
                veiculo_modelo=veiculo.modelo,
                data_inicio=contrato.data_inicio,
                data_fim_prevista=contrato.data_fim_prevista,
                data_fim_real=contrato.data_fim_real,
                status=contrato.status,
                valor_diaria=contrato.valor_diaria,
                km_inicio=contrato.km_inicio,
                km_final=contrato.km_final,
            )
            for contrato, veiculo in contratos
        ],
        financeiro=ResumoFinanceiroClienteOut(
            total_pago=total_pago,
            total_pendente=total_pendente,
            total_estornado=total_estornado,
        ),
        alertas=alertas,
        multas=[MultaOut.model_validate(m) for m in multas],
        sinistros=[SinistroOut.model_validate(s) for s in sinistros],
        danos=[DanoOut.model_validate(d) for d in danos],
    )
