"""multas, sinistros e danos: novas tabelas compartilhadas entre Frota e Clientes

Revision ID: 0005
Revises: 0004
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


revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "multas",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("cliente_id", "clientes", nullable=True),
        _fk_uuid("contrato_id", "contratos", nullable=True),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("infracao", sa.String(255), nullable=False),
        sa.Column("local", sa.String(255), nullable=True),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("pontos", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pendente"),
        sa.Column("observacoes", sa.Text(), nullable=True),
    )
    op.create_index("ix_multas_veiculo_id", "multas", ["veiculo_id"])
    op.create_index("ix_multas_cliente_id", "multas", ["cliente_id"])

    op.create_table(
        "sinistros",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("cliente_id", "clientes", nullable=True),
        _fk_uuid("contrato_id", "contratos", nullable=True),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("valor_prejuizo", sa.Numeric(12, 2), nullable=True),
        sa.Column(
            "seguradora_acionada",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column("status", sa.String(20), nullable=False, server_default="aberto"),
    )
    op.create_index("ix_sinistros_veiculo_id", "sinistros", ["veiculo_id"])
    op.create_index("ix_sinistros_cliente_id", "sinistros", ["cliente_id"])

    op.create_table(
        "danos",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("cliente_id", "clientes", nullable=True),
        _fk_uuid("contrato_id", "contratos", nullable=True),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("data", sa.Date(), nullable=False),
        sa.Column("valor_reparo", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pendente"),
    )
    op.create_index("ix_danos_veiculo_id", "danos", ["veiculo_id"])
    op.create_index("ix_danos_cliente_id", "danos", ["cliente_id"])


def downgrade() -> None:
    op.drop_table("danos")
    op.drop_table("sinistros")
    op.drop_table("multas")
