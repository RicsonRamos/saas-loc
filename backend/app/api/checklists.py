from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.checklist import Checklist, ChecklistItem
from app.models.usuario import Usuario
from app.schemas.checklist import (
    AssinaturaCreate,
    AssinaturaOut,
    ChecklistComparacaoOut,
    ChecklistCreate,
    ChecklistItemFotoUpdate,
    ChecklistItemOut,
    ChecklistOut,
)
from app.schemas.common import Page, PageMeta
from app.services import checklist_service

router = APIRouter(tags=["checklists"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


def _para_saida(checklist: Checklist, itens: list[ChecklistItem]) -> ChecklistOut:
    return ChecklistOut(
        id=checklist.id,
        contrato_id=checklist.contrato_id,
        tipo=checklist.tipo,
        data=checklist.data,
        usuario_id=checklist.usuario_id,
        km=checklist.km,
        combustivel=checklist.combustivel,
        observacoes_gerais=checklist.observacoes_gerais,
        status=checklist.status,
        itens=[ChecklistItemOut.model_validate(item) for item in itens],
    )


@router.get("/checklists", response_model=Page[ChecklistOut])
def listar_checklists(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    contrato_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("checklists:visualizar")),
) -> Page[ChecklistOut]:
    itens_paginados, total = checklist_service.listar(db, page, limit, contrato_id)
    data = [
        _para_saida(checklist, checklist_service.itens_do_checklist(db, checklist.id))
        for checklist in itens_paginados
    ]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("/checklists", response_model=ChecklistOut, status_code=status.HTTP_201_CREATED)
def registrar_checklist(
    payload: ChecklistCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("checklists:registrar")),
) -> ChecklistOut:
    checklist, itens = checklist_service.criar(
        db, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return _para_saida(checklist, itens)


@router.get("/checklists/{checklist_id}", response_model=ChecklistOut)
def obter_checklist(
    checklist_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("checklists:visualizar")),
) -> ChecklistOut:
    checklist, itens = checklist_service.obter(db, checklist_id)
    return _para_saida(checklist, itens)


@router.delete("/checklists/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_checklist(
    checklist_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("checklists:registrar")),
) -> None:
    checklist_service.remover(db, checklist_id, usuario_id=usuario.id, ip=_ip_do_cliente(request))


@router.patch("/checklists/{checklist_id}/itens/{item_id}", response_model=ChecklistItemOut)
def atualizar_foto_item_checklist(
    checklist_id: UUID,
    item_id: UUID,
    payload: ChecklistItemFotoUpdate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("checklists:registrar")),
) -> ChecklistItemOut:
    item = checklist_service.atualizar_foto_item(
        db,
        checklist_id,
        item_id,
        payload.foto_attachment_id,
        usuario_id=usuario.id,
        ip=_ip_do_cliente(request),
    )
    return ChecklistItemOut.model_validate(item)


@router.post(
    "/checklists/{checklist_id}/assinaturas",
    response_model=AssinaturaOut,
    status_code=status.HTTP_201_CREATED,
)
def registrar_assinatura(
    checklist_id: UUID,
    payload: AssinaturaCreate,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("checklists:registrar")),
) -> AssinaturaOut:
    assinatura = checklist_service.criar_assinatura(
        db, checklist_id, payload, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
    return AssinaturaOut.model_validate(assinatura)


@router.get(
    "/contratos/{contrato_id}/checklists/comparacao", response_model=ChecklistComparacaoOut
)
def comparar_checklists(
    contrato_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("checklists:visualizar")),
) -> ChecklistComparacaoOut:
    return ChecklistComparacaoOut(**checklist_service.comparacao(db, contrato_id))
