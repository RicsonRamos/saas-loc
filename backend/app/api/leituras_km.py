from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.usuario import Usuario
from app.schemas.common import Page, PageMeta
from app.schemas.leitura_km import LeituraKmCreate, LeituraKmOut
from app.services import leitura_km_service

router = APIRouter(prefix="/leituras-km", tags=["leituras_km"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=Page[LeituraKmOut])
def listar_leituras_km(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("leituras_km:visualizar")),
) -> Page[LeituraKmOut]:
    itens, total = leitura_km_service.listar(db, page, limit, veiculo_id)
    data = [LeituraKmOut.model_validate(item) for item in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=LeituraKmOut, status_code=status.HTTP_201_CREATED)
def registrar_leitura_km(
    payload: LeituraKmCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("leituras_km:registrar")),
) -> LeituraKmOut:
    return leitura_km_service.registrar(
        db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
