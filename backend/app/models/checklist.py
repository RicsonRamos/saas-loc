import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

TIPO_ENTREGA = "entrega"
TIPO_DEVOLUCAO = "devolucao"
TIPOS_CHECKLIST_VALIDOS = {TIPO_ENTREGA, TIPO_DEVOLUCAO}

STATUS_CHECKLIST_RASCUNHO = "rascunho"
STATUS_CHECKLIST_CONCLUIDO = "concluido"
STATUS_CHECKLIST_VALIDOS = {STATUS_CHECKLIST_RASCUNHO, STATUS_CHECKLIST_CONCLUIDO}

ITEM_LATARIA = "lataria"
ITEM_PNEUS = "pneus"
ITEM_COMBUSTIVEL = "combustivel"
ITEM_KM = "km"
ITEM_DOCUMENTOS = "documentos"
ITEM_ACESSORIOS = "acessorios"
ITENS_CHECKLIST_VALIDOS = {
    ITEM_LATARIA,
    ITEM_PNEUS,
    ITEM_COMBUSTIVEL,
    ITEM_KM,
    ITEM_DOCUMENTOS,
    ITEM_ACESSORIOS,
}

SITUACAO_OK = "ok"
SITUACAO_AVARIA = "avaria"
SITUACAO_FALTANTE = "faltante"
SITUACOES_ITEM_VALIDAS = {SITUACAO_OK, SITUACAO_AVARIA, SITUACAO_FALTANTE}


class Checklist(TimestampedBase):
    __tablename__ = "checklists"
    __table_args__ = (
        Index(
            "uq_checklists_contrato_tipo_ativo",
            "contrato_id",
            "tipo",
            unique=True,
            postgresql_where=text("deleted_at IS NULL"),
        ),
    )

    contrato_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(15), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    km: Mapped[int] = mapped_column(Integer, nullable=False)
    combustivel: Mapped[str | None] = mapped_column(String(20), nullable=True)
    observacoes_gerais: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(15), nullable=False, default=STATUS_CHECKLIST_CONCLUIDO
    )


class ChecklistItem(TimestampedBase):
    __tablename__ = "checklist_itens"

    checklist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checklists.id"), nullable=False, index=True
    )
    item: Mapped[str] = mapped_column(String(30), nullable=False)
    situacao: Mapped[str] = mapped_column(String(15), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
    foto_attachment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("attachments.id"), nullable=True
    )


class Assinatura(TimestampedBase):
    __tablename__ = "assinaturas"

    checklist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("checklists.id"), nullable=False, index=True
    )
    attachment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("attachments.id"), nullable=False
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    responsavel_nome: Mapped[str] = mapped_column(String(150), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
