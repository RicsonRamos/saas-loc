import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase


class VehicleTracking(TimestampedBase):
    """Estrutura preparatória para integração futura com GPS/rastreadores.

    Sem service/router/tela nesta fase — apenas o schema de banco, para que uma
    migration futura de integração não precise criar a tabela do zero.
    """

    __tablename__ = "vehicle_tracking"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    latitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    registrado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fonte: Mapped[str | None] = mapped_column(String(30), nullable=True)
