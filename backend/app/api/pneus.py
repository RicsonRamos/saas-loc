from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.pneu import PneuCreate, PneuOut, PneuUpdate
from app.services import pneu_service

router = APIRouter(prefix="/pneus", tags=["pneus"])


@router.get("", response_model=Page[PneuOut])
def listar_pneus(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pneus:visualizar")),
) -> Page[PneuOut]:
    itens, total = pneu_service.listar(db, page, limit, veiculo_id)
    data = [PneuOut.model_validate(p) for p in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=PneuOut, status_code=status.HTTP_201_CREATED)
def registrar_pneu(
    payload: PneuCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pneus:registrar")),
) -> PneuOut:
    return pneu_service.criar(db, payload)


@router.get("/{pneu_id}", response_model=PneuOut)
def obter_pneu(
    pneu_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pneus:visualizar")),
) -> PneuOut:
    return pneu_service.obter(db, pneu_id)


@router.patch("/{pneu_id}", response_model=PneuOut)
def atualizar_pneu(
    pneu_id: UUID,
    payload: PneuUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pneus:registrar")),
) -> PneuOut:
    return pneu_service.atualizar(db, pneu_id, payload)


@router.delete("/{pneu_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_pneu(
    pneu_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("pneus:registrar")),
) -> None:
    pneu_service.remover(db, pneu_id)
