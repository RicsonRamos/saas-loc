import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

TIPO_PREVENTIVA = "preventiva"
TIPO_CORRETIVA = "corretiva"

TIPOS_MANUTENCAO_VALIDOS = {TIPO_PREVENTIVA, TIPO_CORRETIVA}


class Manutencao(TimestampedBase):
    __tablename__ = "manutencoes"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    km: Mapped[int] = mapped_column(Integer, nullable=False)
    custo: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    oficina: Mapped[str | None] = mapped_column(String(150), nullable=True)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    proxima_manutencao_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proxima_manutencao_data: Mapped[date | None] = mapped_column(Date, nullable=True)
