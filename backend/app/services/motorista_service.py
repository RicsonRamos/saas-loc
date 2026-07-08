import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.motorista import Motorista
from app.schemas.motorista import MotoristaCreate, MotoristaUpdate
from app.services.common import paginar


def criar(db: Session, payload: MotoristaCreate) -> Motorista:
    motorista = Motorista(**payload.model_dump())
    db.add(motorista)
    db.commit()
    db.refresh(motorista)
    return motorista


def listar(
    db: Session, page: int, limit: int, cliente_id: uuid.UUID | None = None
) -> tuple[list[Motorista], int]:
    stmt = (
        select(Motorista)
        .where(Motorista.deleted_at.is_(None))
        .order_by(Motorista.created_at.desc())
    )
    if cliente_id:
        stmt = stmt.where(Motorista.cliente_id == cliente_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, motorista_id: uuid.UUID) -> Motorista:
    motorista = db.get(Motorista, motorista_id)
    if motorista is None or motorista.deleted_at is not None:
        raise NotFoundError("Motorista não encontrado.")
    return motorista


def atualizar(db: Session, motorista_id: uuid.UUID, payload: MotoristaUpdate) -> Motorista:
    motorista = obter(db, motorista_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(motorista, campo, valor)
    db.commit()
    db.refresh(motorista)
    return motorista


def remover(db: Session, motorista_id: uuid.UUID) -> None:
    motorista = obter(db, motorista_id)
    motorista.deleted_at = datetime.now(UTC)
    db.commit()
