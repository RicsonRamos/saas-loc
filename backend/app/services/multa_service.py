import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.multa import Multa
from app.schemas.multa import MultaCreate, MultaUpdate
from app.services.common import paginar


def criar(db: Session, payload: MultaCreate) -> Multa:
    multa = Multa(**payload.model_dump())
    db.add(multa)
    db.commit()
    db.refresh(multa)
    return multa


def listar(
    db: Session,
    page: int,
    limit: int,
    veiculo_id: uuid.UUID | None = None,
    cliente_id: uuid.UUID | None = None,
) -> tuple[list[Multa], int]:
    stmt = select(Multa).where(Multa.deleted_at.is_(None)).order_by(Multa.data.desc())
    if veiculo_id:
        stmt = stmt.where(Multa.veiculo_id == veiculo_id)
    if cliente_id:
        stmt = stmt.where(Multa.cliente_id == cliente_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, multa_id: uuid.UUID) -> Multa:
    multa = db.get(Multa, multa_id)
    if multa is None or multa.deleted_at is not None:
        raise NotFoundError("Multa não encontrada.")
    return multa


def atualizar(db: Session, multa_id: uuid.UUID, payload: MultaUpdate) -> Multa:
    multa = obter(db, multa_id)
    for campo, valor in payload.model_dump(exclude_unset=True).items():
        setattr(multa, campo, valor)
    db.commit()
    db.refresh(multa)
    return multa


def remover(db: Session, multa_id: uuid.UUID) -> None:
    multa = obter(db, multa_id)
    multa.deleted_at = datetime.now(UTC)
    db.commit()
