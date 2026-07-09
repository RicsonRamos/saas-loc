from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.schemas.common import Page, PageMeta
from app.schemas.plano_manutencao import (
    PlanoManutencaoCreate,
    PlanoManutencaoOut,
    PlanoManutencaoUpdate,
)
from app.services import plano_manutencao_service

router = APIRouter(prefix="/planos-manutencao", tags=["planos_manutencao"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


def _para_saida(db: Session, plano) -> PlanoManutencaoOut:
    veiculo = db.get(Veiculo, plano.veiculo_id)
    return plano_manutencao_service.para_saida_com_status(plano, veiculo)


@router.get("", response_model=Page[PlanoManutencaoOut])
def listar_planos_manutencao(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("manutencoes:visualizar")),
) -> Page[PlanoManutencaoOut]:
    itens, total = plano_manutencao_service.listar(db, page, limit, veiculo_id)
    data = [_para_saida(db, item) for item in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=PlanoManutencaoOut, status_code=status.HTTP_201_CREATED)
def criar_plano_manutencao(
    payload: PlanoManutencaoCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("manutencoes:registrar")),
) -> PlanoManutencaoOut:
    plano = plano_manutencao_service.criar(
        db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(db, plano)


@router.patch("/{plano_id}", response_model=PlanoManutencaoOut)
def atualizar_plano_manutencao(
    plano_id: UUID,
    payload: PlanoManutencaoUpdate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("manutencoes:registrar")),
) -> PlanoManutencaoOut:
    plano = plano_manutencao_service.atualizar(
        db, plano_id, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(db, plano)


@router.delete("/{plano_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_plano_manutencao(
    plano_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("manutencoes:registrar")),
) -> None:
    plano_manutencao_service.remover(
        db, plano_id, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
