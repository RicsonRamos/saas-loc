import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria, serializar_campos
from app.exceptions import NotFoundError
from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoUpdate
from app.services.common import paginar


def criar(
    db: Session,
    payload: AbastecimentoCreate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Abastecimento:
    abastecimento = Abastecimento(**payload.model_dump())
    db.add(abastecimento)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="criar",
        entidade="abastecimento",
        entidade_id=abastecimento.id,
        dados_novos=serializar_campos(payload.model_dump()),
        ip=ip,
    )
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
    db: Session,
    abastecimento_id: uuid.UUID,
    payload: AbastecimentoUpdate,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> Abastecimento:
    abastecimento = obter(db, abastecimento_id)
    campos_alterados = payload.model_dump(exclude_unset=True)
    dados_anteriores = {campo: getattr(abastecimento, campo) for campo in campos_alterados}
    for campo, valor in campos_alterados.items():
        setattr(abastecimento, campo, valor)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="atualizar",
        entidade="abastecimento",
        entidade_id=abastecimento.id,
        dados_anteriores=serializar_campos(dados_anteriores),
        dados_novos=serializar_campos(campos_alterados),
        ip=ip,
    )
    db.commit()
    db.refresh(abastecimento)
    return abastecimento


def remover(
    db: Session,
    abastecimento_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    abastecimento = obter(db, abastecimento_id)
    abastecimento.deleted_at = datetime.now(UTC)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="excluir",
        entidade="abastecimento",
        entidade_id=abastecimento.id,
        ip=ip,
    )
    db.commit()
