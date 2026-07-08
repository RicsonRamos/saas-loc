import re
import uuid
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.audit import registrar_auditoria
from app.core.storage import gerar_url_assinada, upload_arquivo
from app.exceptions import NotFoundError, PayloadInvalidoError
from app.models.attachment import (
    ENTIDADES_VALIDAS,
    TIPO_DOCUMENTO,
    TIPO_IMAGEM,
    Attachment,
)
from app.models.checklist import Checklist, ChecklistItem
from app.models.contrato import Contrato
from app.models.veiculo import Veiculo
from app.services.common import paginar

TAMANHO_MAXIMO_BYTES = 10 * 1024 * 1024

_CONTENT_TYPE_POR_CATEGORIA = {
    "image/jpeg": TIPO_IMAGEM,
    "image/png": TIPO_IMAGEM,
    "image/webp": TIPO_IMAGEM,
    "application/pdf": TIPO_DOCUMENTO,
}

# Modelos usados para validar que a entidade referenciada realmente existe.
# "assinatura" referencia o checklist ao qual a assinatura pertence (o anexo em
# si é a imagem PNG capturada no canvas), por isso aponta para Checklist também.
_MODELOS_POR_ENTIDADE: dict[str, type] = {
    "veiculo": Veiculo,
    "contrato": Contrato,
    "checklist": Checklist,
    "checklist_item": ChecklistItem,
    "assinatura": Checklist,
}


def _detectar_content_type(conteudo: bytes) -> str | None:
    """Detecta o tipo real do arquivo pelos magic bytes, não confiando na extensão."""
    if conteudo.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if conteudo.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if conteudo[:4] == b"RIFF" and conteudo[8:12] == b"WEBP":
        return "image/webp"
    if conteudo.startswith(b"%PDF-"):
        return "application/pdf"
    return None


def _sanitizar_nome(nome_original: str) -> str:
    nome_base = nome_original.replace("\\", "/").rsplit("/", 1)[-1]
    return re.sub(r"[^A-Za-z0-9_.-]", "_", nome_base)[:255]


def _validar_entidade(db: Session, entidade_tipo: str, entidade_id: uuid.UUID) -> None:
    if entidade_tipo not in ENTIDADES_VALIDAS:
        raise PayloadInvalidoError(
            f"Tipo de entidade inválido. Use um de: {sorted(ENTIDADES_VALIDAS)}"
        )
    modelo = _MODELOS_POR_ENTIDADE.get(entidade_tipo)
    if modelo is None:
        return
    registro = db.get(modelo, entidade_id)
    if registro is None or getattr(registro, "deleted_at", None) is not None:
        raise NotFoundError(f"{entidade_tipo.capitalize()} não encontrado(a).")


def criar(
    db: Session,
    *,
    entidade_tipo: str,
    entidade_id: uuid.UUID,
    nome_original: str,
    conteudo: bytes,
    usuario_id: uuid.UUID,
    ip: str | None = None,
) -> Attachment:
    _validar_entidade(db, entidade_tipo, entidade_id)

    if len(conteudo) > TAMANHO_MAXIMO_BYTES:
        raise PayloadInvalidoError("Arquivo excede o tamanho máximo permitido de 10MB.")

    content_type = _detectar_content_type(conteudo)
    if content_type is None:
        raise PayloadInvalidoError(
            "Tipo de arquivo não suportado. Envie imagens (JPEG/PNG/WEBP) ou PDF."
        )

    bucket = "anexos"
    chave = f"{entidade_tipo}/{entidade_id}/{uuid.uuid4()}-{_sanitizar_nome(nome_original)}"

    # Ordem deliberada: upload no MinIO primeiro, registro no banco depois.
    # Se o upload falhar, nada é escrito no banco. Se o commit falhar após o
    # upload ter sido concluído, sobra um objeto órfão no storage — aceitável,
    # pois nunca deixa uma referência quebrada visível ao usuário.
    upload_arquivo(bucket, chave, conteudo, content_type)

    attachment = Attachment(
        entidade_tipo=entidade_tipo,
        entidade_id=entidade_id,
        tipo=_CONTENT_TYPE_POR_CATEGORIA[content_type],
        nome_original=nome_original,
        content_type=content_type,
        tamanho_bytes=len(conteudo),
        bucket=bucket,
        caminho_storage=chave,
        usuario_upload_id=usuario_id,
    )
    db.add(attachment)
    db.flush()
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="upload",
        entidade="attachment",
        entidade_id=attachment.id,
        dados_novos={
            "entidade_tipo": entidade_tipo,
            "entidade_id": str(entidade_id),
            "nome_original": nome_original,
        },
        ip=ip,
    )
    db.commit()
    db.refresh(attachment)
    return attachment


def listar(
    db: Session,
    page: int,
    limit: int,
    entidade_tipo: str | None = None,
    entidade_id: uuid.UUID | None = None,
) -> tuple[list[Attachment], int]:
    stmt = (
        select(Attachment)
        .where(Attachment.deleted_at.is_(None))
        .order_by(Attachment.data_upload.desc())
    )
    if entidade_tipo:
        stmt = stmt.where(Attachment.entidade_tipo == entidade_tipo)
    if entidade_id:
        stmt = stmt.where(Attachment.entidade_id == entidade_id)
    return paginar(db, stmt, page, limit)


def obter(db: Session, attachment_id: uuid.UUID) -> Attachment:
    attachment = db.get(Attachment, attachment_id)
    if attachment is None or attachment.deleted_at is not None:
        raise NotFoundError("Anexo não encontrado.")
    return attachment


def gerar_url_download(db: Session, attachment_id: uuid.UUID) -> str:
    attachment = obter(db, attachment_id)
    return gerar_url_assinada(attachment.bucket, attachment.caminho_storage)


def remover(
    db: Session,
    attachment_id: uuid.UUID,
    usuario_id: uuid.UUID | None = None,
    ip: str | None = None,
) -> None:
    """Soft delete no banco. Não remove o objeto físico do MinIO nesta chamada
    (evita apagar do storage e o commit do soft-delete falhar depois, deixando
    o registro "vivo" apontando para um objeto já removido). A limpeza física
    de objetos órfãos/soft-deletados é um job assíncrono fora de escopo desta
    fase — pode comparar `Attachment.deleted_at` antigo contra o bucket.
    """
    attachment = obter(db, attachment_id)
    attachment.deleted_at = datetime.now(UTC)
    registrar_auditoria(
        db,
        usuario_id=usuario_id,
        acao="excluir",
        entidade="attachment",
        entidade_id=attachment.id,
        ip=ip,
    )
    db.commit()
