from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_DISPONIVEL = "disponivel"
STATUS_ALUGADO = "alugado"
STATUS_EM_MANUTENCAO = "em_manutencao"
STATUS_BAIXADO = "baixado"

STATUS_VEICULO_VALIDOS = {
    STATUS_DISPONIVEL,
    STATUS_ALUGADO,
    STATUS_EM_MANUTENCAO,
    STATUS_BAIXADO,
}


class Veiculo(TimestampedBase):
    __tablename__ = "veiculos"

    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    modelo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_DISPONIVEL)
    km_atual: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    filial_id: Mapped[str | None] = mapped_column(String(60), nullable=True)
