from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.core.permissions import has_permission
from app.models.usuario import Usuario
from app.schemas.dashboard import DashboardResumoOut
from app.services import dashboard_service

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/resumo", response_model=DashboardResumoOut)
def obter_resumo(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("frota:visualizar")),
) -> DashboardResumoOut:
    incluir_financeiro = has_permission(usuario.role, "financeiro:visualizar")
    return dashboard_service.resumo(db, incluir_financeiro)
