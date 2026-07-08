import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_MULTA_PENDENTE = "pendente"
STATUS_MULTA_PAGA = "paga"
STATUS_MULTA_RECORRIDA = "recorrida"
STATUS_MULTA_CANCELADA = "cancelada"

STATUS_MULTA_VALIDOS = {
    STATUS_MULTA_PENDENTE,
    STATUS_MULTA_PAGA,
    STATUS_MULTA_RECORRIDA,
    STATUS_MULTA_CANCELADA,
}


class Multa(TimestampedBase):
    __tablename__ = "multas"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    cliente_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=True, index=True
    )
    contrato_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=True
    )
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    infracao: Mapped[str] = mapped_column(String(255), nullable=False)
    local: Mapped[str | None] = mapped_column(String(255), nullable=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    pontos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_MULTA_PENDENTE)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
