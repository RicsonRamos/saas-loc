from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase


class Motorista(TimestampedBase):
    __tablename__ = "motoristas"

    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    cnh: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    validade_cnh: Mapped[date] = mapped_column(Date, nullable=False)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
