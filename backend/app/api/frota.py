from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.veiculo import VeiculoCreate, VeiculoOut, VeiculoUpdate
from app.services import veiculo_service

router = APIRouter(prefix="/veiculos", tags=["frota"])


@router.get("", response_model=Page[VeiculoOut])
def listar_veiculos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filtro: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> Page[VeiculoOut]:
    itens, total = veiculo_service.listar(db, page, limit, status_filtro)
    data = [VeiculoOut.model_validate(v) for v in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=VeiculoOut, status_code=status.HTTP_201_CREATED)
def criar_veiculo(
    payload: VeiculoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return veiculo_service.criar(db, payload)


@router.get("/{veiculo_id}", response_model=VeiculoOut)
def obter_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:visualizar")),
) -> VeiculoOut:
    return veiculo_service.obter(db, veiculo_id)


@router.patch("/{veiculo_id}", response_model=VeiculoOut)
def atualizar_veiculo(
    veiculo_id: UUID,
    payload: VeiculoUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> VeiculoOut:
    return veiculo_service.atualizar(db, veiculo_id, payload)


@router.delete("/{veiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_veiculo(
    veiculo_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("frota:editar")),
) -> None:
    veiculo_service.remover(db, veiculo_id)
