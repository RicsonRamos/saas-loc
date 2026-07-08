"""motoristas: vinculo opcional a cliente (condutor adicional/dependente)

Revision ID: 0006
Revises: 0005
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006"
down_revision: str | None = "0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "motoristas",
        sa.Column("cliente_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("clientes.id"), nullable=True),
    )
    op.add_column("motoristas", sa.Column("parentesco", sa.String(60), nullable=True))
    op.create_index("ix_motoristas_cliente_id", "motoristas", ["cliente_id"])


def downgrade() -> None:
    op.drop_index("ix_motoristas_cliente_id", table_name="motoristas")
    op.drop_column("motoristas", "parentesco")
    op.drop_column("motoristas", "cliente_id")
