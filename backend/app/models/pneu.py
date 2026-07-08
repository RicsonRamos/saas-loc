import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

POSICAO_DIANTEIRO_ESQUERDO = "dianteiro_esquerdo"
POSICAO_DIANTEIRO_DIREITO = "dianteiro_direito"
POSICAO_TRASEIRO_ESQUERDO = "traseiro_esquerdo"
POSICAO_TRASEIRO_DIREITO = "traseiro_direito"
POSICAO_ESTEPE = "estepe"

POSICOES_PNEU_VALIDAS = {
    POSICAO_DIANTEIRO_ESQUERDO,
    POSICAO_DIANTEIRO_DIREITO,
    POSICAO_TRASEIRO_ESQUERDO,
    POSICAO_TRASEIRO_DIREITO,
    POSICAO_ESTEPE,
}

STATUS_PNEU_ATIVO = "ativo"
STATUS_PNEU_TROCADO = "trocado"

STATUS_PNEU_VALIDOS = {STATUS_PNEU_ATIVO, STATUS_PNEU_TROCADO}


class Pneu(TimestampedBase):
    __tablename__ = "pneus"

    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    marca: Mapped[str] = mapped_column(String(60), nullable=False)
    modelo: Mapped[str | None] = mapped_column(String(60), nullable=True)
    numero_serie: Mapped[str | None] = mapped_column(String(60), nullable=True)
    posicao: Mapped[str] = mapped_column(String(30), nullable=False)
    data_instalacao: Mapped[date] = mapped_column(Date, nullable=False)
    km_instalacao: Mapped[int] = mapped_column(Integer, nullable=False)
    vida_util_km: Mapped[int | None] = mapped_column(Integer, nullable=True)
    data_troca: Mapped[date | None] = mapped_column(Date, nullable=True)
    km_troca: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_PNEU_ATIVO)
