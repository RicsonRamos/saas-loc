from datetime import date

from sqlalchemy import Date, Integer, String
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
    marca: Mapped[str | None] = mapped_column(String(60), nullable=True)
    cor: Mapped[str | None] = mapped_column(String(40), nullable=True)
    categoria: Mapped[str | None] = mapped_column(String(60), nullable=True)
    chassi: Mapped[str | None] = mapped_column(String(30), unique=True, nullable=True)
    renavam: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True)
    combustivel: Mapped[str | None] = mapped_column(String(30), nullable=True)
    cambio: Mapped[str | None] = mapped_column(String(30), nullable=True)
    vencimento_licenciamento: Mapped[date | None] = mapped_column(Date, nullable=True)
    vencimento_seguro: Mapped[date | None] = mapped_column(Date, nullable=True)
