from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, Query, Request, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_permission
from app.models.attachment import ENTIDADES_VALIDAS
from app.models.usuario import Usuario
from app.schemas.attachment import AttachmentDownloadOut, AttachmentOut
from app.schemas.common import Page, PageMeta
from app.services import attachment_service

router = APIRouter(prefix="/attachments", tags=["anexos"])


def _ip_do_cliente(request: Request) -> str | None:
    return request.client.host if request.client else None


@router.get("", response_model=Page[AttachmentOut])
def listar_attachments(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    entidade_tipo: str | None = None,
    entidade_id: UUID | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("anexos:visualizar")),
) -> Page[AttachmentOut]:
    itens, total = attachment_service.listar(db, page, limit, entidade_tipo, entidade_id)
    data = [AttachmentOut.model_validate(item) for item in itens]
    return Page(data=data, meta=PageMeta(page=page, limit=limit, total=total))


@router.post("", response_model=AttachmentOut, status_code=status.HTTP_201_CREATED)
async def enviar_attachment(
    request: Request,
    arquivo: UploadFile = File(...),
    entidade_tipo: str = Form(..., description=f"Um de: {sorted(ENTIDADES_VALIDAS)}"),
    entidade_id: UUID = Form(...),
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("anexos:enviar")),
) -> AttachmentOut:
    conteudo = await arquivo.read()
    attachment = attachment_service.criar(
        db,
        entidade_tipo=entidade_tipo,
        entidade_id=entidade_id,
        nome_original=arquivo.filename or "arquivo",
        conteudo=conteudo,
        usuario_id=usuario.id,
        ip=_ip_do_cliente(request),
    )
    return AttachmentOut.model_validate(attachment)


@router.get("/{attachment_id}/download", response_model=AttachmentDownloadOut)
def baixar_attachment(
    attachment_id: UUID,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("anexos:visualizar")),
) -> AttachmentDownloadOut:
    url = attachment_service.gerar_url_download(db, attachment_id)
    return AttachmentDownloadOut(url=url)


@router.delete("/{attachment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_attachment(
    attachment_id: UUID,
    request: Request,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_permission("anexos:excluir")),
) -> None:
    attachment_service.remover(
        db, attachment_id, usuario_id=usuario.id, ip=_ip_do_cliente(request)
    )
