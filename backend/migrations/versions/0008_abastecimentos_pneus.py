"""abastecimentos e pneus: novas tabelas do veiculo

Revision ID: 0008
Revises: 0007
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


def _metadados_padrao() -> list[sa.Column]:
    return [
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    ]


def _fk_uuid(nome: str, tabela_referenciada: str, nullable: bool = False) -> sa.Column:
    return sa.Column(
        nome,
        postgresql.UUID(as_uuid=True),
        sa.ForeignKey(f"{tabela_referenciada}.id"),
        nullable=nullable,
    )


revision: str = "0008"
down_revision: str | None = "0007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "abastecimentos",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("contrato_id", "contratos", nullable=True),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("posto", sa.String(150), nullable=True),
        sa.Column("litros", sa.Numeric(10, 3), nullable=False),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("km", sa.Integer(), nullable=False),
        sa.Column("tipo_combustivel", sa.String(30), nullable=True),
    )
    op.create_index("ix_abastecimentos_veiculo_id", "abastecimentos", ["veiculo_id"])

    op.create_table(
        "pneus",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        sa.Column("marca", sa.String(60), nullable=False),
        sa.Column("modelo", sa.String(60), nullable=True),
        sa.Column("numero_serie", sa.String(60), nullable=True),
        sa.Column("posicao", sa.String(30), nullable=False),
        sa.Column("data_instalacao", sa.Date(), nullable=False),
        sa.Column("km_instalacao", sa.Integer(), nullable=False),
        sa.Column("vida_util_km", sa.Integer(), nullable=True),
        sa.Column("data_troca", sa.Date(), nullable=True),
        sa.Column("km_troca", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="ativo"),
    )
    op.create_index("ix_pneus_veiculo_id", "pneus", ["veiculo_id"])


def downgrade() -> None:
    op.drop_table("pneus")
    op.drop_table("abastecimentos")
