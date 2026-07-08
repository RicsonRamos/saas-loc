import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.contrato import Contrato
from app.models.financeiro import (
    STATUS_PAGAMENTO_ESTORNADO,
    STATUS_PAGAMENTO_PAGO,
    Despesa,
    Pagamento,
)
from app.models.veiculo import Veiculo
from app.schemas.financeiro import DespesaCreate, PagamentoCreate, RentabilidadeVeiculoOut
from app.services.common import paginar


def lancar_pagamento(db: Session, payload: PagamentoCreate) -> Pagamento:
    contrato = db.get(Contrato, payload.contrato_id)
    if contrato is None:
        raise NotFoundError("Contrato não encontrado.")

    pagamento = Pagamento(
        contrato_id=payload.contrato_id,
        valor=payload.valor,
        data=payload.data,
        metodo=payload.metodo,
        status=STATUS_PAGAMENTO_PAGO,
    )
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento


def estornar_pagamento(db: Session, pagamento_id: uuid.UUID) -> Pagamento:
    pagamento = db.get(Pagamento, pagamento_id)
    if pagamento is None:
        raise NotFoundError("Pagamento não encontrado.")
    if pagamento.status == STATUS_PAGAMENTO_ESTORNADO:
        raise ConflictError("Este pagamento já foi estornado.")

    pagamento.status = STATUS_PAGAMENTO_ESTORNADO
    db.commit()
    db.refresh(pagamento)
    return pagamento


def listar_pagamentos(
    db: Session, page: int, limit: int, contrato_id: uuid.UUID | None = None
) -> tuple[list[Pagamento], int]:
    stmt = select(Pagamento).order_by(Pagamento.data.desc())
    if contrato_id:
        stmt = stmt.where(Pagamento.contrato_id == contrato_id)
    return paginar(db, stmt, page, limit)


def registrar_despesa(db: Session, payload: DespesaCreate) -> Despesa:
    despesa = Despesa(**payload.model_dump())
    db.add(despesa)
    db.commit()
    db.refresh(despesa)
    return despesa


def listar_despesas(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[Despesa], int]:
    stmt = select(Despesa).order_by(Despesa.data.desc())
    if veiculo_id:
        stmt = stmt.where(Despesa.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)


def rentabilidade_por_veiculo(db: Session) -> list[RentabilidadeVeiculoOut]:
    veiculos = db.execute(select(Veiculo).where(Veiculo.deleted_at.is_(None))).scalars().all()

    resultado = []
    for veiculo in veiculos:
        receita = (
            db.scalar(
                select(func.coalesce(func.sum(Pagamento.valor), 0))
                .join(Contrato, Contrato.id == Pagamento.contrato_id)
                .where(
                    Contrato.veiculo_id == veiculo.id,
                    Pagamento.status == STATUS_PAGAMENTO_PAGO,
                )
            )
            or Decimal("0")
        )
        despesa = (
            db.scalar(
                select(func.coalesce(func.sum(Despesa.valor), 0)).where(
                    Despesa.veiculo_id == veiculo.id
                )
            )
            or Decimal("0")
        )
        resultado.append(
            RentabilidadeVeiculoOut(
                veiculo_id=veiculo.id,
                placa=veiculo.placa,
                receita_total=receita,
                despesa_total=despesa,
                resultado=receita - despesa,
            )
        )
    return resultado
