import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

TIPO_SINISTRO_BATIDA = "batida"
TIPO_SINISTRO_ROUBO = "roubo"
TIPO_SINISTRO_FURTO = "furto"
TIPO_SINISTRO_ENCHENTE = "enchente"
TIPO_SINISTRO_INCENDIO = "incendio"

TIPOS_SINISTRO_VALIDOS = {
    TIPO_SINISTRO_BATIDA,
    TIPO_SINISTRO_ROUBO,
    TIPO_SINISTRO_FURTO,
    TIPO_SINISTRO_ENCHENTE,
    TIPO_SINISTRO_INCENDIO,
}

STATUS_SINISTRO_ABERTO = "aberto"
STATUS_SINISTRO_EM_ANDAMENTO = "em_andamento"
STATUS_SINISTRO_FINALIZADO = "finalizado"

STATUS_SINISTRO_VALIDOS = {
    STATUS_SINISTRO_ABERTO,
    STATUS_SINISTRO_EM_ANDAMENTO,
    STATUS_SINISTRO_FINALIZADO,
}


class Sinistro(TimestampedBase):
    __tablename__ = "sinistros"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    cliente_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=True, index=True
    )
    contrato_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=True
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    valor_prejuizo: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    seguradora_acionada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=STATUS_SINISTRO_ABERTO
    )
