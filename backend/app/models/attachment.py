import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

ENTIDADE_VEICULO = "veiculo"
ENTIDADE_CONTRATO = "contrato"
ENTIDADE_CHECKLIST = "checklist"
ENTIDADE_CHECKLIST_ITEM = "checklist_item"
ENTIDADE_ASSINATURA = "assinatura"

ENTIDADES_VALIDAS = {
    ENTIDADE_VEICULO,
    ENTIDADE_CONTRATO,
    ENTIDADE_CHECKLIST,
    ENTIDADE_CHECKLIST_ITEM,
    ENTIDADE_ASSINATURA,
}

TIPO_IMAGEM = "imagem"
TIPO_DOCUMENTO = "documento"

TIPOS_VALIDOS = {TIPO_IMAGEM, TIPO_DOCUMENTO}


class Attachment(TimestampedBase):
    __tablename__ = "attachments"

    entidade_tipo: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    entidade_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    nome_original: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    tamanho_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    bucket: Mapped[str] = mapped_column(String(60), nullable=False)
    caminho_storage: Mapped[str] = mapped_column(String(500), nullable=False)
    usuario_upload_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False, index=True
    )
    data_upload: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
