import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

TIPO_DANO_ARRANHAO = "arranhao"
TIPO_DANO_AMASSADO = "amassado"
TIPO_DANO_QUEBRA_VIDRO = "quebra_vidro"
TIPO_DANO_INTERNO = "dano_interno"
TIPO_DANO_OUTRO = "outro"

TIPOS_DANO_VALIDOS = {
    TIPO_DANO_ARRANHAO,
    TIPO_DANO_AMASSADO,
    TIPO_DANO_QUEBRA_VIDRO,
    TIPO_DANO_INTERNO,
    TIPO_DANO_OUTRO,
}

STATUS_DANO_PENDENTE = "pendente"
STATUS_DANO_REPARADO = "reparado"

STATUS_DANO_VALIDOS = {STATUS_DANO_PENDENTE, STATUS_DANO_REPARADO}


class Dano(TimestampedBase):
    __tablename__ = "danos"

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
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    valor_reparo: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_DANO_PENDENTE)
