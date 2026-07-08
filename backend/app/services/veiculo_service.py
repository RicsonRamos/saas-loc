import uuid
from datetime import UTC, date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.cliente import Cliente
from app.models.contrato import Contrato
from app.models.financeiro import Despesa
from app.models.manutencao import Manutencao
from app.models.veiculo import (
    STATUS_DISPONIVEL,
    STATUS_LICENCIAMENTO_VENCIDO,
    STATUS_SEGURO_VENCIDO,
    Veiculo,
)
from app.schemas.veiculo import (
    HistoricoContratoOut,
    HistoricoDespesaOut,
    HistoricoManutencaoOut,
    HistoricoVeiculoOut,
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


def criar(db: Session, payload: VeiculoCreate) -> Veiculo:
    veiculo = Veiculo(**payload.model_dump())
    db.add(veiculo)
    db.commit()
    db.refresh(veiculo)
    return veiculo


def listar(
    db: Session, page: int, limit: int, status: str | None = None
) -> tuple[list[Veiculo], int]:
    stmt = select(Veiculo).where(Veiculo.deleted_at.is_(None)).order_by(Veiculo.created_at.desc())
    if status:
        stmt = stmt.where(Veiculo.status == status)
    return paginar(db, stmt, page, limit)


def obter(db: Session, veiculo_id: uuid.UUID) -> Veiculo:
    veiculo = db.get(Veiculo, veiculo_id)
    if veiculo is None or veiculo.deleted_at is not None:
        raise NotFoundError("Veículo não encontrado.")
    return veiculo


def atualizar(db: Session, veiculo_id: uuid.UUID, payload: VeiculoUpdate) -> Veiculo:
    veiculo = obter(db, veiculo_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(veiculo, campo, valor)
    db.commit()
    db.refresh(veiculo)
    return veiculo


def remover(db: Session, veiculo_id: uuid.UUID) -> None:
    veiculo = obter(db, veiculo_id)
    veiculo.deleted_at = datetime.now(UTC)
    db.commit()


def historico(db: Session, veiculo_id: uuid.UUID) -> HistoricoVeiculoOut:
    obter(db, veiculo_id)  # garante 404 se o veículo não existir (ou estiver excluído)

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
    )
