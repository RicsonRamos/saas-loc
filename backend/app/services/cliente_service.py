import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.services.common import paginar


def criar(db: Session, payload: ClienteCreate) -> Cliente:
    cliente = Cliente(**payload.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


def listar(db: Session, page: int, limit: int) -> tuple[list[Cliente], int]:
    stmt = select(Cliente).where(Cliente.deleted_at.is_(None)).order_by(Cliente.created_at.desc())
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
