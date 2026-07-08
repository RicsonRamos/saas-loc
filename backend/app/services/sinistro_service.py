import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.sinistro import Sinistro
from app.schemas.sinistro import SinistroCreate, SinistroUpdate
from app.services.common import paginar


def criar(db: Session, payload: SinistroCreate) -> Sinistro:
    sinistro = Sinistro(**payload.model_dump())
    db.add(sinistro)
    db.commit()
    db.refresh(sinistro)
    return sinistro


def listar(
    db: Session,
    page: int,
    limit: int,
    veiculo_id: uuid.UUID | None = None,
    cliente_id: uuid.UUID | None = None,
) -> tuple[list[Sinistro], int]:
    stmt = select(Sinistro).where(Sinistro.deleted_at.is_(None)).order_by(Sinistro.data.desc())
    if veiculo_id:
        stmt = stmt.where(Sinistro.veiculo_id == veiculo_id)
    if cliente_id:
        stmt = stmt.where(Sinistro.cliente_id == cliente_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, sinistro_id: uuid.UUID) -> Sinistro:
    sinistro = db.get(Sinistro, sinistro_id)
    if sinistro is None or sinistro.deleted_at is not None:
        raise NotFoundError("Sinistro não encontrado.")
    return sinistro


def atualizar(db: Session, sinistro_id: uuid.UUID, payload: SinistroUpdate) -> Sinistro:
    sinistro = obter(db, sinistro_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(sinistro, campo, valor)
    db.commit()
    db.refresh(sinistro)
    return sinistro


def remover(db: Session, sinistro_id: uuid.UUID) -> None:
    sinistro = obter(db, sinistro_id)
    sinistro.deleted_at = datetime.now(UTC)
    db.commit()
