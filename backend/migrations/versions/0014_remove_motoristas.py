"""remove motoristas: unificado em clientes, contratos usa so cliente_id

Revision ID: 0014
Revises: 0013
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


revision: str = "0014"
down_revision: str | None = "0013"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("contratos", "motorista_id")
    op.drop_table("motoristas")


def downgrade() -> None:
    op.create_table(
        "motoristas",
        *_metadados_padrao(),
        sa.Column("nome", sa.String(150), nullable=False),
        sa.Column("cnh", sa.String(20), nullable=False, unique=True),
        sa.Column("validade_cnh", sa.Date(), nullable=False),
        sa.Column("telefone", sa.String(30), nullable=True),
        _fk_uuid("cliente_id", "clientes", nullable=True),
        sa.Column("parentesco", sa.String(60), nullable=True),
    )
    op.create_index("ix_motoristas_cnh", "motoristas", ["cnh"])
    op.create_index("ix_motoristas_cliente_id", "motoristas", ["cliente_id"])
    op.add_column("contratos", _fk_uuid("motorista_id", "motoristas", nullable=True))
