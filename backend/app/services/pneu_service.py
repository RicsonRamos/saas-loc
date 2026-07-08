import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria, serializar_campos
from app.exceptions import NotFoundError
from app.models.pneu import Pneu
from app.schemas.pneu import PneuCreate, PneuUpdate
from app.services.common import paginar


def criar(
    db: Session,
    payload: PneuCreate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Pneu:
    pneu = Pneu(**payload.model_dump())
    db.add(pneu)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="pneu",
        entidade_id=pneu.id,
        dados_novos=serializar_campos(payload.model_dump()),
        ip=ip,
    )
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


def atualizar(
    db: Session,
    pneu_id: uuid.UUID,
    payload: PneuUpdate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Pneu:
    pneu = obter(db, pneu_id)
    campos_alterados = payload.model_dump(exclude_unset=True)
    dados_anteriores = {campo: getattr(pneu, campo) for campo in campos_alterados}
    for campo, valor in campos_alterados.items():
        setattr(pneu, campo, valor)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="pneu",
        entidade_id=pneu.id,
        dados_anteriores=serializar_campos(dados_anteriores),
        dados_novos=serializar_campos(campos_alterados),
        ip=ip,
    )
    db.commit()
    db.refresh(pneu)
    return pneu


def remover(
    db: Session,
    pneu_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    pneu = obter(db, pneu_id)
    pneu.deleted_at = datetime.now(UTC)
    registrar_auditoria(
        db, usuario_id=usuario_id, acao="excluir", entidade="pneu", entidade_id=pneu.id, ip=ip
    )
    db.commit()
