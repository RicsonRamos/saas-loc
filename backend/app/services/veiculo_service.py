import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.exceptions import NotFoundError
from app.models.veiculo import Veiculo
from app.schemas.veiculo import VeiculoCreate, VeiculoUpdate
from app.services.common import paginar


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
