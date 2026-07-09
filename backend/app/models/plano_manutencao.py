import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

TIPO_TROCA_OLEO = "troca_oleo"
TIPO_TROCA_FILTROS = "troca_filtros"
TIPO_PASTILHAS_FREIO = "pastilhas_freio"
TIPO_PNEUS = "pneus"
TIPO_REVISAO = "revisao"
TIPO_ALINHAMENTO_BALANCEAMENTO = "alinhamento_balanceamento"
TIPO_LICENCIAMENTO = "licenciamento"
TIPO_SEGURO = "seguro"
TIPO_OUTRO = "outro"

TIPOS_PLANO_MANUTENCAO_VALIDOS = {
    TIPO_TROCA_OLEO,
    TIPO_TROCA_FILTROS,
    TIPO_PASTILHAS_FREIO,
    TIPO_PNEUS,
    TIPO_REVISAO,
    TIPO_ALINHAMENTO_BALANCEAMENTO,
    TIPO_LICENCIAMENTO,
    TIPO_SEGURO,
    TIPO_OUTRO,
}


class PlanoManutencao(TimestampedBase):
    """Plano configurável de manutenção preventiva por tipo, acompanhado em paralelo por veículo."""

    __tablename__ = "planos_manutencao"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(150), nullable=True)
    intervalo_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    intervalo_dias: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ultima_execucao_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ultima_execucao_data: Mapped[date | None] = mapped_column(Date, nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
