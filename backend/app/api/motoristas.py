from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.motorista import MotoristaCreate, MotoristaOut, MotoristaUpdate
from app.services import motorista_service

router = APIRouter(prefix="/motoristas", tags=["motoristas"])


@router.get("", response_model=Page[MotoristaOut])
def listar_motoristas(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    cliente_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("motoristas:visualizar")),
) -> Page[MotoristaOut]:
    itens, total = motorista_service.listar(db, page, limit, cliente_id)
    data = [MotoristaOut.model_validate(m) for m in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=MotoristaOut, status_code=status.HTTP_201_CREATED)
def criar_motorista(
    payload: MotoristaCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("motoristas:editar")),
) -> MotoristaOut:
    return motorista_service.criar(db, payload)


@router.get("/{motorista_id}", response_model=MotoristaOut)
def obter_motorista(
    motorista_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("motoristas:visualizar")),
) -> MotoristaOut:
    return motorista_service.obter(db, motorista_id)


@router.patch("/{motorista_id}", response_model=MotoristaOut)
def atualizar_motorista(
    motorista_id: UUID,
    payload: MotoristaUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("motoristas:editar")),
) -> MotoristaOut:
    return motorista_service.atualizar(db, motorista_id, payload)


@router.delete("/{motorista_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_motorista(
    motorista_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("motoristas:editar")),
) -> None:
    motorista_service.remover(db, motorista_id)
