from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.schemas.common import Page, PageMeta
from app.schemas.manutencao import ManutencaoCreate, ManutencaoOut
from app.services import manutencao_service

router = APIRouter(prefix="/manutencoes", tags=["manutencoes"])


@router.get("", response_model=Page[ManutencaoOut])
def listar_manutencoes(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("manutencoes:visualizar")),
) -> Page[ManutencaoOut]:
    itens, total = manutencao_service.listar(db, page, limit, veiculo_id)
    data = [ManutencaoOut.model_validate(m) for m in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=ManutencaoOut, status_code=status.HTTP_201_CREATED)
def registrar_manutencao(
    payload: ManutencaoCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("manutencoes:registrar")),
) -> ManutencaoOut:
    return manutencao_service.registrar(db, payload)


@router.get("/{manutencao_id}", response_model=ManutencaoOut)
def obter_manutencao(
    manutencao_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("manutencoes:visualizar")),
) -> ManutencaoOut:
    return manutencao_service.obter(db, manutencao_id)
