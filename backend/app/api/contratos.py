from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.contrato import Contrato
from app.models.usuario import Usuario
from app.models.veiculo import Veiculo
from app.schemas.common import Page, PageMeta
from app.schemas.contrato import ContratoCreate, ContratoDevolucao, ContratoOut
from app.services import contrato_service

router = APIRouter(prefix="/contratos", tags=["contratos"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


def _para_saida(db: Session, contrato: Contrato) -> ContratoOut:
    saida = ContratoOut.model_validate(contrato)
    veiculo = db.get(Veiculo, contrato.veiculo_id)
    if veiculo is not None:
        saida.consumo_km = contrato_service.calcular_consumo_km(contrato, veiculo)
    return saida


@router.get("", response_model=Page[ContratoOut])
def listar_contratos(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filtro: str | None = Query(None, alias="status"),
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:visualizar")),
) -> Page[ContratoOut]:
    itens, total = contrato_service.listar(db, page, limit, status_filtro)
    data = [_para_saida(db, c) for c in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=ContratoOut, status_code=status.HTTP_201_CREATED)
def criar_contrato(
    payload: ContratoCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("contratos:emitir")),
) -> ContratoOut:
    contrato = contrato_service.criar_locacao(
        db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(db, contrato)


@router.get("/{contrato_id}", response_model=ContratoOut)
def obter_contrato(
    contrato_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("contratos:visualizar")),
) -> ContratoOut:
    return _para_saida(db, contrato_service.obter(db, contrato_id))


@router.patch("/{contrato_id}/devolucao", response_model=ContratoOut)
def devolver_contrato(
    contrato_id: UUID,
    payload: ContratoDevolucao,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("contratos:emitir")),
) -> ContratoOut:
    contrato = contrato_service.devolver(
        db, contrato_id, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(db, contrato)


@router.patch("/{contrato_id}/cancelamento", response_model=ContratoOut)
def cancelar_contrato(
    contrato_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("contratos:cancelar")),
) -> ContratoOut:
    contrato = contrato_service.cancelar(
        db, contrato_id, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(db, contrato)
