import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase


class Abastecimento(TimestampedBase):
    __tablename__ = "abastecimentos"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    contrato_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=True
    )
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    posto: Mapped[str | None] = mapped_column(String(150), nullable=True)
    litros: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    km: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo_combustivel: Mapped[str | None] = mapped_column(String(30), nullable=True)
