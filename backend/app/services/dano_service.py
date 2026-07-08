import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.dano import Dano
from app.schemas.dano import DanoCreate, DanoUpdate
from app.services.common import paginar


def criar(db: Session, payload: DanoCreate) -> Dano:
    dano = Dano(**payload.model_dump())
    db.add(dano)
    db.commit()
    db.refresh(dano)
    return dano


def listar(
    db: Session,
    page: int,
    limit: int,
    veiculo_id: uuid.UUID | None = None,
    cliente_id: uuid.UUID | None = None,
) -> tuple[list[Dano], int]:
    stmt = select(Dano).where(Dano.deleted_at.is_(None)).order_by(Dano.data.desc())
    if veiculo_id:
        stmt = stmt.where(Dano.veiculo_id == veiculo_id)
    if cliente_id:
        stmt = stmt.where(Dano.cliente_id == cliente_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, dano_id: uuid.UUID) -> Dano:
    dano = db.get(Dano, dano_id)
    if dano is None or dano.deleted_at is not None:
        raise NotFoundError("Dano não encontrado.")
    return dano


def atualizar(db: Session, dano_id: uuid.UUID, payload: DanoUpdate) -> Dano:
    dano = obter(db, dano_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(dano, campo, valor)
    db.commit()
    db.refresh(dano)
    return dano


def remover(db: Session, dano_id: uuid.UUID) -> None:
    dano = obter(db, dano_id)
    dano.deleted_at = datetime.now(UTC)
    db.commit()
