"""cria tabela leituras_km: historico persistido de atualizacao de odometro

Revision ID: 0016
Revises: 0015
Create Date: 2026-07-09

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0016"
down_revision: str | None = "0015"
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
        "leituras_km",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("usuario_id", "usuarios"),
        sa.Column("km", sa.Integer(), nullable=False),
        sa.Column("data_leitura", sa.DateTime(timezone=True), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
    )
    op.create_index("ix_leituras_km_veiculo_id", "leituras_km", ["veiculo_id"])


def downgrade() -> None:
    op.drop_index("ix_leituras_km_veiculo_id", table_name="leituras_km")
    op.drop_table("leituras_km")
