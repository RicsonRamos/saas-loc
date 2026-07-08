from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_DISPONIVEL = "disponivel"
STATUS_ALUGADO = "alugado"
STATUS_RESERVADO = "reservado"
STATUS_EM_MANUTENCAO = "em_manutencao"
STATUS_SINISTRADO = "sinistrado"
STATUS_EM_LIMPEZA = "em_limpeza"
STATUS_LICENCIAMENTO_VENCIDO = "licenciamento_vencido"
STATUS_SEGURO_VENCIDO = "seguro_vencido"
STATUS_INATIVO = "inativo"

STATUS_VEICULO_VALIDOS = {
    STATUS_DISPONIVEL,
    STATUS_ALUGADO,
    STATUS_RESERVADO,
    STATUS_EM_MANUTENCAO,
    STATUS_SINISTRADO,
    STATUS_EM_LIMPEZA,
    STATUS_LICENCIAMENTO_VENCIDO,
    STATUS_SEGURO_VENCIDO,
    STATUS_INATIVO,
}

# Situações calculadas automaticamente a partir de vencimentos, nunca definidas manualmente
# (ver veiculo_service.calcular_status_efetivo). Ver docs/02-MODELO-DE-DADOS.md.
STATUS_VEICULO_AUTOMATICOS = {STATUS_LICENCIAMENTO_VENCIDO, STATUS_SEGURO_VENCIDO}


class Veiculo(TimestampedBase):
    __tablename__ = "veiculos"

    placa: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    modelo: Mapped[str] = mapped_column(String(120), nullable=False)
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default=STATUS_DISPONIVEL)
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
