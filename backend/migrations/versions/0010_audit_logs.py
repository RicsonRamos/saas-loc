"""audit_logs: infraestrutura de auditoria e timeline de alteracoes

Revision ID: 0010
Revises: 0009
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


revision: str = "0010"
down_revision: str | None = "0009"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        *_metadados_padrao(),
        sa.Column(
            "usuario_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("usuarios.id"),
            nullable=True,
        ),
        sa.Column("acao", sa.String(30), nullable=False),
        sa.Column("entidade", sa.String(50), nullable=False),
        sa.Column("entidade_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dados_anteriores", postgresql.JSONB(), nullable=True),
        sa.Column("dados_novos", postgresql.JSONB(), nullable=True),
        sa.Column(
            "data_hora", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("ip", sa.String(45), nullable=True),
        sa.Column("descricao", sa.Text(), nullable=True),
    )
    op.create_index("ix_audit_logs_usuario_id", "audit_logs", ["usuario_id"])
    op.create_index("ix_audit_logs_data_hora", "audit_logs", ["data_hora"])
    op.create_index(
        "ix_audit_logs_entidade_entidade_id", "audit_logs", ["entidade", "entidade_id"]
    )


def downgrade() -> None:
    op.drop_table("audit_logs")
