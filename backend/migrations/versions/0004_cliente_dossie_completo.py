"""clientes: dossie completo (pessoal, contatos, endereco, cnh, financeiro, emergencia, status)

Revision ID: 0004
Revises: 0003
Create Date: 2026-07-08

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("clientes", sa.Column("rg", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("rg_orgao_emissor", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("data_nascimento", sa.Date(), nullable=True))

    op.add_column("clientes", sa.Column("celular_secundario", sa.String(30), nullable=True))
    op.add_column("clientes", sa.Column("whatsapp", sa.String(30), nullable=True))

    op.add_column("clientes", sa.Column("cep", sa.String(10), nullable=True))
    op.add_column("clientes", sa.Column("logradouro", sa.String(150), nullable=True))
    op.add_column("clientes", sa.Column("numero", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("complemento", sa.String(60), nullable=True))
    op.add_column("clientes", sa.Column("bairro", sa.String(100), nullable=True))
    op.add_column("clientes", sa.Column("cidade", sa.String(100), nullable=True))
    op.add_column("clientes", sa.Column("estado", sa.String(2), nullable=True))
    op.drop_column("clientes", "endereco")

    op.add_column("clientes", sa.Column("cnh_numero", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("cnh_categoria", sa.String(5), nullable=True))
    op.add_column("clientes", sa.Column("cnh_emissao", sa.Date(), nullable=True))
    op.add_column("clientes", sa.Column("cnh_vencimento", sa.Date(), nullable=True))
    op.add_column("clientes", sa.Column("cnh_orgao_emissor", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("cnh_primeira_habilitacao", sa.Date(), nullable=True))
    op.add_column(
        "clientes",
        sa.Column("cnh_ear", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )

    op.add_column("clientes", sa.Column("limite_credito", sa.Numeric(12, 2), nullable=True))
    op.add_column("clientes", sa.Column("forma_pagamento_preferida", sa.String(30), nullable=True))
    op.add_column("clientes", sa.Column("banco", sa.String(60), nullable=True))
    op.add_column("clientes", sa.Column("agencia", sa.String(20), nullable=True))
    op.add_column("clientes", sa.Column("conta", sa.String(30), nullable=True))
    op.add_column("clientes", sa.Column("pix", sa.String(100), nullable=True))
    op.add_column("clientes", sa.Column("caucao_padrao", sa.Numeric(12, 2), nullable=True))

    op.add_column("clientes", sa.Column("contato_emergencia_nome", sa.String(150), nullable=True))
    op.add_column(
        "clientes", sa.Column("contato_emergencia_parentesco", sa.String(60), nullable=True)
    )
    op.add_column(
        "clientes", sa.Column("contato_emergencia_telefone", sa.String(30), nullable=True)
    )
    op.add_column(
        "clientes", sa.Column("contato_emergencia_whatsapp", sa.String(30), nullable=True)
    )

    op.add_column(
        "clientes",
        sa.Column("status", sa.String(20), nullable=False, server_default="ativo"),
    )
    op.add_column("clientes", sa.Column("observacoes", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("clientes", "observacoes")
    op.drop_column("clientes", "status")

    op.drop_column("clientes", "contato_emergencia_whatsapp")
    op.drop_column("clientes", "contato_emergencia_telefone")
    op.drop_column("clientes", "contato_emergencia_parentesco")
    op.drop_column("clientes", "contato_emergencia_nome")

    op.drop_column("clientes", "caucao_padrao")
    op.drop_column("clientes", "pix")
    op.drop_column("clientes", "conta")
    op.drop_column("clientes", "agencia")
    op.drop_column("clientes", "banco")
    op.drop_column("clientes", "forma_pagamento_preferida")
    op.drop_column("clientes", "limite_credito")

    op.drop_column("clientes", "cnh_ear")
    op.drop_column("clientes", "cnh_primeira_habilitacao")
    op.drop_column("clientes", "cnh_orgao_emissor")
    op.drop_column("clientes", "cnh_vencimento")
    op.drop_column("clientes", "cnh_emissao")
    op.drop_column("clientes", "cnh_categoria")
    op.drop_column("clientes", "cnh_numero")

    op.add_column("clientes", sa.Column("endereco", sa.String(255), nullable=True))
    op.drop_column("clientes", "estado")
    op.drop_column("clientes", "cidade")
    op.drop_column("clientes", "bairro")
    op.drop_column("clientes", "complemento")
    op.drop_column("clientes", "numero")
    op.drop_column("clientes", "logradouro")
    op.drop_column("clientes", "cep")

    op.drop_column("clientes", "whatsapp")
    op.drop_column("clientes", "celular_secundario")

    op.drop_column("clientes", "data_nascimento")
    op.drop_column("clientes", "rg_orgao_emissor")
    op.drop_column("clientes", "rg")
