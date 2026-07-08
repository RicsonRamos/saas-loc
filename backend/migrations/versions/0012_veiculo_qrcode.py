"""veiculos: codigo publico para QR code / consulta sem autenticacao

Revision ID: 0012
Revises: 0011
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012"
down_revision: str | None = "0011"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("veiculos", sa.Column("codigo_publico", sa.String(40), nullable=True))
    # Backfill: cada veículo existente recebe um código único antes do NOT NULL.
    # md5() é built-in do Postgres, sem depender da extensão pgcrypto.
    op.execute(
        "UPDATE veiculos SET codigo_publico = md5(random()::text || clock_timestamp()::text || id::text) "
        "WHERE codigo_publico IS NULL"
    )
    op.alter_column("veiculos", "codigo_publico", nullable=False)
    op.create_unique_constraint("uq_veiculos_codigo_publico", "veiculos", ["codigo_publico"])


def downgrade() -> None:
    op.drop_constraint("uq_veiculos_codigo_publico", "veiculos", type_="unique")
    op.drop_column("veiculos", "codigo_publico")
