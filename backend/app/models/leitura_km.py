import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase


class LeituraKm(TimestampedBase):
    """Registro periódico de atualização de odômetro, com autor e histórico completo."""

    __tablename__ = "leituras_km"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False
    )
    km: Mapped[int] = mapped_column(Integer, nullable=False)
    data_leitura: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
