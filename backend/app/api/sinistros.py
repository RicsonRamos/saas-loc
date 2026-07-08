from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.sinistro import SinistroCreate, SinistroOut, SinistroUpdate
from app.services import sinistro_service

router = APIRouter(prefix="/sinistros", tags=["sinistros"])


@router.get("", response_model=Page[SinistroOut])
def listar_sinistros(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    cliente_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("sinistros:visualizar")),
) -> Page[SinistroOut]:
    itens, total = sinistro_service.listar(db, page, limit, veiculo_id, cliente_id)
    data = [SinistroOut.model_validate(s) for s in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=SinistroOut, status_code=status.HTTP_201_CREATED)
def registrar_sinistro(
    payload: SinistroCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("sinistros:registrar")),
) -> SinistroOut:
    return sinistro_service.criar(db, payload)


@router.get("/{sinistro_id}", response_model=SinistroOut)
def obter_sinistro(
    sinistro_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("sinistros:visualizar")),
) -> SinistroOut:
    return sinistro_service.obter(db, sinistro_id)


@router.patch("/{sinistro_id}", response_model=SinistroOut)
def atualizar_sinistro(
    sinistro_id: UUID,
    payload: SinistroUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("sinistros:registrar")),
) -> SinistroOut:
    return sinistro_service.atualizar(db, sinistro_id, payload)


@router.delete("/{sinistro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_sinistro(
    sinistro_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("sinistros:registrar")),
) -> None:
    sinistro_service.remover(db, sinistro_id)
