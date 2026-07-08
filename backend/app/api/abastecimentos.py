from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.usuario import Usuario
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoOut, AbastecimentoUpdate
from app.schemas.common import Page, PageMeta
from app.services import abastecimento_service

router = APIRouter(prefix="/abastecimentos", tags=["abastecimentos"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=Page[AbastecimentoOut])
def listar_abastecimentos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    veiculo_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("abastecimentos:visualizar")),
) -> Page[AbastecimentoOut]:
    itens, total = abastecimento_service.listar(db, page, limit, veiculo_id)
    data = [AbastecimentoOut.model_validate(a) for a in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=AbastecimentoOut, status_code=status.HTTP_201_CREATED)
def registrar_abastecimento(
    payload: AbastecimentoCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("abastecimentos:registrar")),
) -> AbastecimentoOut:
    return abastecimento_service.criar(
        db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )


@router.get("/{abastecimento_id}", response_model=AbastecimentoOut)
def obter_abastecimento(
    abastecimento_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("abastecimentos:visualizar")),
) -> AbastecimentoOut:
    return abastecimento_service.obter(db, abastecimento_id)


@router.patch("/{abastecimento_id}", response_model=AbastecimentoOut)
def atualizar_abastecimento(
    abastecimento_id: UUID,
    payload: AbastecimentoUpdate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("abastecimentos:registrar")),
) -> AbastecimentoOut:
    return abastecimento_service.atualizar(
        db, abastecimento_id, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )


@router.delete("/{abastecimento_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_abastecimento(
    abastecimento_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("abastecimentos:registrar")),
) -> None:
    abastecimento_service.remover(
        db, abastecimento_id, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
