import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.services.common import paginar


def listar(
    db: Session,
    page: int,
    limit: int,
    entidade: str | None = None,
    entidade_id: uuid.UUID | None = None,
    usuario_id: uuid.UUID | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
) -> tuple[list[AuditLog], int]:
    stmt = select(AuditLog).order_by(AuditLog.data_hora.desc())
    if entidade:
        stmt = stmt.where(AuditLog.entidade == entidade)
    if entidade_id:
        stmt = stmt.where(AuditLog.entidade_id == entidade_id)
    if usuario_id:
        stmt = stmt.where(AuditLog.usuario_id == usuario_id)
    if data_inicio:
        stmt = stmt.where(AuditLog.data_hora >= data_inicio)
    if data_fim:
        stmt = stmt.where(AuditLog.data_hora <= data_fim)
    return paginar(db, stmt, page, limit)
