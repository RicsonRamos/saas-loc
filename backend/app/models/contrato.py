import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_RESERVADO = "reservado"
STATUS_ATIVO = "ativo"
STATUS_ENCERRADO = "encerrado"
STATUS_CANCELADO = "cancelado"

STATUS_CONTRATO_OCUPA_VEICULO = {STATUS_RESERVADO, STATUS_ATIVO}

# Reaproveitado pela migração inicial (migrations/versions/0001_initial.py) e pelos
# testes de concorrência, para não duplicar a definição da regra crítica do domínio.
SQL_HABILITAR_BTREE_GIST = "CREATE EXTENSION IF NOT EXISTS btree_gist"
SQL_CONSTRAINT_SEM_OVERLAP = """
ALTER TABLE contratos ADD CONSTRAINT contratos_sem_overlap
EXCLUDE USING gist (
    veiculo_id WITH =,
    tstzrange(data_inicio, data_fim_prevista) WITH &&
) WHERE (status IN ('reservado', 'ativo'))
"""


class Contrato(TimestampedBase):
    """Fluxo único reserva -> ativo -> encerrado (ou cancelado). Ver docs/00-VISAO-GERAL.md.

    A prevenção de dupla alocação de veículo é garantida por uma constraint de
    exclusão no PostgreSQL (`contratos_sem_overlap`), criada na migração inicial —
    não apenas por validação em Python. Ver docs/02-MODELO-DE-DADOS.md.
    """

    __tablename__ = "contratos"

    cliente_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clientes.id"), nullable=False, index=True
    )
    veiculo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("veiculos.id"), nullable=False, index=True
    )
    data_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_fim_prevista: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    data_fim_real: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_RESERVADO)
    valor_diaria: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    km_inicio: Mapped[int | None] = mapped_column(Integer, nullable=True)
    km_final: Mapped[int | None] = mapped_column(Integer, nullable=True)
    km_contratado_mensal: Mapped[int | None] = mapped_column(Integer, nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    __mapper_args__ = {"version_id_col": version}


class ContratoEvento(TimestampedBase):
    """Histórico de mudança de status de um contrato."""

    __tablename__ = "contrato_eventos"

    contrato_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contratos.id"), nullable=False, index=True
    )
    status_anterior: Mapped[str | None] = mapped_column(String(20), nullable=True)
    status_novo: Mapped[str] = mapped_column(String(20), nullable=False)
    observacao: Mapped[str | None] = mapped_column(Text, nullable=True)
