"""veiculos: expande situacoes de status; contratos: km_inicio/km_final

Revision ID: 0003
Revises: 0002
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("veiculos", "status", type_=sa.String(30), existing_type=sa.String(20))
    op.execute("UPDATE veiculos SET status = 'inativo' WHERE status = 'baixado'")

    op.add_column("contratos", sa.Column("km_inicio", sa.Integer(), nullable=True))
    op.add_column("contratos", sa.Column("km_final", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("contratos", "km_final")
    op.drop_column("contratos", "km_inicio")

    op.execute("UPDATE veiculos SET status = 'baixado' WHERE status = 'inativo'")
    op.alter_column("veiculos", "status", type_=sa.String(20), existing_type=sa.String(30))
