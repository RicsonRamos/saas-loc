"""contratos: adiciona km_contratado_mensal (franquia de quilometragem)

Revision ID: 0015
Revises: 0014
Create Date: 2026-07-09

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0015"
down_revision: str | None = "0014"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("contratos", sa.Column("km_contratado_mensal", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("contratos", "km_contratado_mensal")
