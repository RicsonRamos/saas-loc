"""cria tabela planos_manutencao: planos configuraveis de manutencao preventiva por tipo

Revision ID: 0017
Revises: 0016
Create Date: 2026-07-09

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0017"
down_revision: str | None = "0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


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


def upgrade() -> None:
    op.create_table(
        "planos_manutencao",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        sa.Column("tipo", sa.String(30), nullable=False),
        sa.Column("descricao", sa.String(150), nullable=True),
        sa.Column("intervalo_km", sa.Integer(), nullable=True),
        sa.Column("intervalo_dias", sa.Integer(), nullable=True),
        sa.Column("ultima_execucao_km", sa.Integer(), nullable=True),
        sa.Column("ultima_execucao_data", sa.Date(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_planos_manutencao_veiculo_id", "planos_manutencao", ["veiculo_id"])


def downgrade() -> None:
    op.drop_index("ix_planos_manutencao_veiculo_id", table_name="planos_manutencao")
    op.drop_table("planos_manutencao")
