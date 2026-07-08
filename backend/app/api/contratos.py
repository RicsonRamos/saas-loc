from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.contrato import ContratoCreate, ContratoDevolucao, ContratoOut
from app.services import contrato_service

router = APIRouter(prefix="/contratos", tags=["contratos"])


@router.get("", response_model=Page[ContratoOut])
def listar_contratos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filtro: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:visualizar")),
) -> Page[ContratoOut]:
    itens, total = contrato_service.listar(db, page, limit, status_filtro)
    data = [ContratoOut.model_validate(c) for c in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=ContratoOut, status_code=status.HTTP_201_CREATED)
def criar_contrato(
    payload: ContratoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:emitir")),
) -> ContratoOut:
    return contrato_service.criar_locacao(db, payload)


@router.get("/{contrato_id}", response_model=ContratoOut)
def obter_contrato(
    contrato_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:visualizar")),
) -> ContratoOut:
    return contrato_service.obter(db, contrato_id)


@router.patch("/{contrato_id}/devolucao", response_model=ContratoOut)
def devolver_contrato(
    contrato_id: UUID,
    payload: ContratoDevolucao,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:emitir")),
) -> ContratoOut:
    return contrato_service.devolver(db, contrato_id, payload)


@router.patch("/{contrato_id}/cancelamento", response_model=ContratoOut)
def cancelar_contrato(
    contrato_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:cancelar")),
) -> ContratoOut:
    return contrato_service.cancelar(db, contrato_id)
