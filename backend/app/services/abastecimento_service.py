import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoUpdate
from app.services.common import paginar


def criar(db: Session, payload: AbastecimentoCreate) -> Abastecimento:
    abastecimento = Abastecimento(**payload.model_dump())
    db.add(abastecimento)
    db.commit()
    db.refresh(abastecimento)
    return abastecimento


def listar(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[Abastecimento], int]:
    stmt = (
        select(Abastecimento)
        .where(Abastecimento.deleted_at.is_(None))
        .order_by(Abastecimento.data.desc())
    )
    if veiculo_id:
        stmt = stmt.where(Abastecimento.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, abastecimento_id: uuid.UUID) -> Abastecimento:
    abastecimento = db.get(Abastecimento, abastecimento_id)
    if abastecimento is None or abastecimento.deleted_at is not None:
        raise NotFoundError("Abastecimento não encontrado.")
    return abastecimento


def atualizar(
    db: Session, abastecimento_id: uuid.UUID, payload: AbastecimentoUpdate
) -> Abastecimento:
    abastecimento = obter(db, abastecimento_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(abastecimento, campo, valor)
    db.commit()
    db.refresh(abastecimento)
    return abastecimento


def remover(db: Session, abastecimento_id: uuid.UUID) -> None:
    abastecimento = obter(db, abastecimento_id)
    abastecimento.deleted_at = datetime.now(UTC)
    db.commit()
