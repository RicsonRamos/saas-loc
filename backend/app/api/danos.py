from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.dano import DanoCreate, DanoOut, DanoUpdate
from app.services import dano_service

router = APIRouter(prefix="/danos", tags=["danos"])


@router.get("", response_model=Page[DanoOut])
def listar_danos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    cliente_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("danos:visualizar")),
) -> Page[DanoOut]:
    itens, total = dano_service.listar(db, page, limit, veiculo_id, cliente_id)
    data = [DanoOut.model_validate(d) for d in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=DanoOut, status_code=status.HTTP_201_CREATED)
def registrar_dano(
    payload: DanoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("danos:registrar")),
) -> DanoOut:
    return dano_service.criar(db, payload)


@router.get("/{dano_id}", response_model=DanoOut)
def obter_dano(
    dano_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("danos:visualizar")),
) -> DanoOut:
    return dano_service.obter(db, dano_id)


@router.patch("/{dano_id}", response_model=DanoOut)
def atualizar_dano(
    dano_id: UUID,
    payload: DanoUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("danos:registrar")),
) -> DanoOut:
    return dano_service.atualizar(db, dano_id, payload)


@router.delete("/{dano_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_dano(
    dano_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("danos:registrar")),
) -> None:
    dano_service.remover(db, dano_id)
