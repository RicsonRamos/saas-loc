import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.pneu import Pneu
from app.schemas.pneu import PneuCreate, PneuUpdate
from app.services.common import paginar


def criar(db: Session, payload: PneuCreate) -> Pneu:
    pneu = Pneu(**payload.model_dump())
    db.add(pneu)
    db.commit()
    db.refresh(pneu)
    return pneu


def listar(
    db: Session, page: int, limit: int, veiculo_id: uuid.UUID | None = None
) -> tuple[list[Pneu], int]:
    stmt = (
        select(Pneu)
        .where(Pneu.deleted_at.is_(None))
        .order_by(Pneu.data_instalacao.desc())
    )
    if veiculo_id:
        stmt = stmt.where(Pneu.veiculo_id == veiculo_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, pneu_id: uuid.UUID) -> Pneu:
    pneu = db.get(Pneu, pneu_id)
    if pneu is None or pneu.deleted_at is not None:
        raise NotFoundError("Pneu não encontrado.")
    return pneu


def atualizar(db: Session, pneu_id: uuid.UUID, payload: PneuUpdate) -> Pneu:
    pneu = obter(db, pneu_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(pneu, campo, valor)
    db.commit()
    db.refresh(pneu)
    return pneu


def remover(db: Session, pneu_id: uuid.UUID) -> None:
    pneu = obter(db, pneu_id)
    pneu.deleted_at = datetime.now(UTC)
    db.commit()
