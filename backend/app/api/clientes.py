from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.cliente import ClienteCreate, ClienteOut, ClienteUpdate
from app.schemas.common import Page, PageMeta
from app.services import cliente_service

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=Page[ClienteOut])
def listar_clientes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("clientes:visualizar")),
) -> Page[ClienteOut]:
    itens, total = cliente_service.listar(db, page, limit)
    data = [ClienteOut.model_validate(c) for c in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=ClienteOut, status_code=status.HTTP_201_CREATED)
def criar_cliente(
    payload: ClienteCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("clientes:editar")),
) -> ClienteOut:
    return cliente_service.criar(db, payload)


@router.get("/{cliente_id}", response_model=ClienteOut)
def obter_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("clientes:visualizar")),
) -> ClienteOut:
    return cliente_service.obter(db, cliente_id)


@router.patch("/{cliente_id}", response_model=ClienteOut)
def atualizar_cliente(
    cliente_id: UUID,
    payload: ClienteUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("clientes:editar")),
) -> ClienteOut:
    return cliente_service.atualizar(db, cliente_id, payload)


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_cliente(
    cliente_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("clientes:editar")),
) -> None:
    cliente_service.remover(db, cliente_id)
