"""veiculos: informacoes gerais, aquisicao, documentacao e seguro detalhado

Revision ID: 0007
Revises: 0006
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("veiculos", sa.Column("versao", sa.String(60), nullable=True))
    op.add_column("veiculos", sa.Column("ano_fabricacao", sa.Integer(), nullable=True))
    op.add_column("veiculos", sa.Column("portas", sa.Integer(), nullable=True))
    op.add_column("veiculos", sa.Column("capacidade_passageiros", sa.Integer(), nullable=True))
    op.add_column("veiculos", sa.Column("motor", sa.String(60), nullable=True))
    op.add_column("veiculos", sa.Column("potencia", sa.String(30), nullable=True))

    op.add_column("veiculos", sa.Column("data_aquisicao", sa.Date(), nullable=True))
    op.add_column("veiculos", sa.Column("valor_compra", sa.Numeric(12, 2), nullable=True))
    op.add_column("veiculos", sa.Column("fornecedor", sa.String(150), nullable=True))
    op.add_column("veiculos", sa.Column("forma_aquisicao", sa.String(30), nullable=True))
    op.add_column("veiculos", sa.Column("km_inicial", sa.Integer(), nullable=True))
    op.add_column("veiculos", sa.Column("proprietario", sa.String(150), nullable=True))
    op.add_column("veiculos", sa.Column("data_entrada_frota", sa.Date(), nullable=True))
    op.add_column("veiculos", sa.Column("garantia_fabrica_ate", sa.Date(), nullable=True))
    op.add_column("veiculos", sa.Column("garantia_concessionaria_ate", sa.Date(), nullable=True))

    op.add_column("veiculos", sa.Column("crlv_numero", sa.String(30), nullable=True))
    op.add_column("veiculos", sa.Column("ipva_vencimento", sa.Date(), nullable=True))
    op.add_column(
        "veiculos",
        sa.Column("alienado", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.add_column("veiculos", sa.Column("alienante", sa.String(150), nullable=True))

    op.add_column("veiculos", sa.Column("seguradora", sa.String(100), nullable=True))
    op.add_column("veiculos", sa.Column("apolice_numero", sa.String(40), nullable=True))
    op.add_column("veiculos", sa.Column("seguro_franquia", sa.Numeric(12, 2), nullable=True))
    op.add_column("veiculos", sa.Column("seguro_cobertura", sa.Text(), nullable=True))
    op.add_column("veiculos", sa.Column("seguro_contato", sa.String(100), nullable=True))


def downgrade() -> None:
    op.drop_column("veiculos", "seguro_contato")
    op.drop_column("veiculos", "seguro_cobertura")
    op.drop_column("veiculos", "seguro_franquia")
    op.drop_column("veiculos", "apolice_numero")
    op.drop_column("veiculos", "seguradora")

    op.drop_column("veiculos", "alienante")
    op.drop_column("veiculos", "alienado")
    op.drop_column("veiculos", "ipva_vencimento")
    op.drop_column("veiculos", "crlv_numero")

    op.drop_column("veiculos", "garantia_concessionaria_ate")
    op.drop_column("veiculos", "garantia_fabrica_ate")
    op.drop_column("veiculos", "data_entrada_frota")
    op.drop_column("veiculos", "proprietario")
    op.drop_column("veiculos", "km_inicial")
    op.drop_column("veiculos", "forma_aquisicao")
    op.drop_column("veiculos", "fornecedor")
    op.drop_column("veiculos", "valor_compra")
    op.drop_column("veiculos", "data_aquisicao")

    op.drop_column("veiculos", "potencia")
    op.drop_column("veiculos", "motor")
    op.drop_column("veiculos", "capacidade_passageiros")
    op.drop_column("veiculos", "portas")
    op.drop_column("veiculos", "ano_fabricacao")
    op.drop_column("veiculos", "versao")
