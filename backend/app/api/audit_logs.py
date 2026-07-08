from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.audit_log import AuditLogOut
from app.schemas.common import Page, PageMeta
from app.services import audit_log_service

router = APIRouter(prefix="/audit-logs", tags=["auditoria"])


@router.get("", response_model=Page[AuditLogOut])
def listar_audit_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    entidade: str | None = None,
    entidade_id: UUID | None = None,
    usuario_id: UUID | None = None,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("auditoria:visualizar")),
) -> Page[AuditLogOut]:
    itens, total = audit_log_service.listar(
        db, page, limit, entidade, entidade_id, usuario_id, data_inicio, data_fim
    )
    data = [AuditLogOut.model_validate(item) for item in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))
