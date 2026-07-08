import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_PAGAMENTO_PENDENTE = "pendente"
STATUS_PAGAMENTO_PAGO = "pago"
STATUS_PAGAMENTO_ESTORNADO = "estornado"


class Pagamento(TimestampedBase):
    __tablename__ = "pagamentos"

    contrato_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False, index=True
    )
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=STATUS_PAGAMENTO_PENDENTE
    )
    metodo: Mapped[str | None] = mapped_column(String(30), nullable=True)


class Despesa(TimestampedBase):
    __tablename__ = "despesas"

    veiculo_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=True, index=True
    )
    categoria: Mapped[str] = mapped_column(String(60), nullable=False)
    valor: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255), nullable=True)
