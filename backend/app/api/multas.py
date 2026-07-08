from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.multa import MultaCreate, MultaOut, MultaUpdate
from app.services import multa_service

router = APIRouter(prefix="/multas", tags=["multas"])


@router.get("", response_model=Page[MultaOut])
def listar_multas(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    cliente_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("multas:visualizar")),
) -> Page[MultaOut]:
    itens, total = multa_service.listar(db, page, limit, veiculo_id, cliente_id)
    data = [MultaOut.model_validate(m) for m in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=MultaOut, status_code=status.HTTP_201_CREATED)
def registrar_multa(
    payload: MultaCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("multas:registrar")),
) -> MultaOut:
    return multa_service.criar(db, payload)


@router.get("/{multa_id}", response_model=MultaOut)
def obter_multa(
    multa_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("multas:visualizar")),
) -> MultaOut:
    return multa_service.obter(db, multa_id)


@router.patch("/{multa_id}", response_model=MultaOut)
def atualizar_multa(
    multa_id: UUID,
    payload: MultaUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("multas:registrar")),
) -> MultaOut:
    return multa_service.atualizar(db, multa_id, payload)


@router.delete("/{multa_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_multa(
    multa_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("multas:registrar")),
) -> None:
    multa_service.remover(db, multa_id)
