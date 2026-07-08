"""veiculos: campos adicionais de cadastro (marca, cor, categoria, documentacao)

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("veiculos", sa.Column("marca", sa.String(60), nullable=True))
    op.add_column("veiculos", sa.Column("cor", sa.String(40), nullable=True))
    op.add_column("veiculos", sa.Column("categoria", sa.String(60), nullable=True))
    op.add_column("veiculos", sa.Column("chassi", sa.String(30), nullable=True))
    op.add_column("veiculos", sa.Column("renavam", sa.String(20), nullable=True))
    op.add_column("veiculos", sa.Column("combustivel", sa.String(30), nullable=True))
    op.add_column("veiculos", sa.Column("cambio", sa.String(30), nullable=True))
    op.add_column("veiculos", sa.Column("vencimento_licenciamento", sa.Date(), nullable=True))
    op.add_column("veiculos", sa.Column("vencimento_seguro", sa.Date(), nullable=True))
    op.create_unique_constraint("uq_veiculos_chassi", "veiculos", ["chassi"])
    op.create_unique_constraint("uq_veiculos_renavam", "veiculos", ["renavam"])


def downgrade() -> None:
    op.drop_constraint("uq_veiculos_renavam", "veiculos", type_="unique")
    op.drop_constraint("uq_veiculos_chassi", "veiculos", type_="unique")
    op.drop_column("veiculos", "vencimento_seguro")
    op.drop_column("veiculos", "vencimento_licenciamento")
    op.drop_column("veiculos", "cambio")
    op.drop_column("veiculos", "combustivel")
    op.drop_column("veiculos", "renavam")
    op.drop_column("veiculos", "chassi")
    op.drop_column("veiculos", "categoria")
    op.drop_column("veiculos", "cor")
    op.drop_column("veiculos", "marca")
