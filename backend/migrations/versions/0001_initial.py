"""schema inicial: usuarios, veiculos, clientes, motoristas, contratos, manutencoes, financeiro

Revision ID: 0001
Revises:
Create Date: 2026-07-07

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

from app.models.contrato import SQL_CONSTRAINT_SEM_OVERLAP, SQL_HABILITAR_BTREE_GIST

revision: str = "0001"
down_revision: str | None = None
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
    # necessário para a constraint de exclusão (igualdade de UUID + overlap de range) em contratos
    op.execute(SQL_HABILITAR_BTREE_GIST)

    op.create_table(
        "usuarios",
        *_metadados_padrao(),
        sa.Column("nome", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(30), nullable=False),
        sa.Column("ativo", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_index("ix_usuarios_email", "usuarios", ["email"])

    op.create_table(
        "veiculos",
        *_metadados_padrao(),
        sa.Column("placa", sa.String(10), nullable=False, unique=True),
        sa.Column("modelo", sa.String(120), nullable=False),
        sa.Column("ano", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="disponivel"),
        sa.Column("km_atual", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("filial_id", sa.String(60), nullable=True),
    )
    op.create_index("ix_veiculos_placa", "veiculos", ["placa"])

    op.create_table(
        "clientes",
        *_metadados_padrao(),
        sa.Column("nome", sa.String(150), nullable=False),
        sa.Column("documento", sa.String(20), nullable=False, unique=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("telefone", sa.String(30), nullable=True),
        sa.Column("endereco", sa.String(255), nullable=True),
    )
    op.create_index("ix_clientes_documento", "clientes", ["documento"])

    op.create_table(
        "motoristas",
        *_metadados_padrao(),
        sa.Column("nome", sa.String(150), nullable=False),
        sa.Column("cnh", sa.String(20), nullable=False, unique=True),
        sa.Column("validade_cnh", sa.Date(), nullable=False),
        sa.Column("telefone", sa.String(30), nullable=True),
    )
    op.create_index("ix_motoristas_cnh", "motoristas", ["cnh"])

    op.create_table(
        "contratos",
        *_metadados_padrao(),
        _fk_uuid("cliente_id", "clientes"),
        _fk_uuid("veiculo_id", "veiculos"),
        _fk_uuid("motorista_id", "motoristas", nullable=True),
        sa.Column("data_inicio", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_fim_prevista", sa.DateTime(timezone=True), nullable=False),
        sa.Column("data_fim_real", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="reservado"),
        sa.Column("valor_diaria", sa.Numeric(12, 2), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
    )
    op.create_index("ix_contratos_cliente_id", "contratos", ["cliente_id"])
    op.create_index("ix_contratos_veiculo_id", "contratos", ["veiculo_id"])

    # Regra crítica do domínio: nenhum veículo pode estar em dois contratos ativos
    # com período sobreposto. Ver docs/02-MODELO-DE-DADOS.md.
    op.execute(SQL_CONSTRAINT_SEM_OVERLAP)

    op.create_table(
        "contrato_eventos",
        *_metadados_padrao(),
        _fk_uuid("contrato_id", "contratos"),
        sa.Column("status_anterior", sa.String(20), nullable=True),
        sa.Column("status_novo", sa.String(20), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
    )
    op.create_index("ix_contrato_eventos_contrato_id", "contrato_eventos", ["contrato_id"])

    op.create_table(
        "manutencoes",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos"),
        sa.Column("tipo", sa.String(20), nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("km", sa.Integer(), nullable=False),
        sa.Column("custo", sa.Numeric(12, 2), nullable=False),
        sa.Column("oficina", sa.String(150), nullable=True),
        sa.Column("descricao", sa.Text(), nullable=True),
        sa.Column("proxima_manutencao_km", sa.Integer(), nullable=True),
        sa.Column("proxima_manutencao_data", sa.Date(), nullable=True),
    )
    op.create_index("ix_manutencoes_veiculo_id", "manutencoes", ["veiculo_id"])

    op.create_table(
        "pagamentos",
        *_metadados_padrao(),
        _fk_uuid("contrato_id", "contratos"),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="pendente"),
        sa.Column("metodo", sa.String(30), nullable=True),
    )
    op.create_index("ix_pagamentos_contrato_id", "pagamentos", ["contrato_id"])

    op.create_table(
        "despesas",
        *_metadados_padrao(),
        _fk_uuid("veiculo_id", "veiculos", nullable=True),
        sa.Column("categoria", sa.String(60), nullable=False),
        sa.Column("valor", sa.Numeric(12, 2), nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        sa.Column("descricao", sa.String(255), nullable=True),
    )
    op.create_index("ix_despesas_veiculo_id", "despesas", ["veiculo_id"])


def downgrade() -> None:
    op.drop_table("despesas")
    op.drop_table("pagamentos")
    op.drop_table("manutencoes")
    op.drop_table("contrato_eventos")
    op.execute("ALTER TABLE contratos DROP CONSTRAINT contratos_sem_overlap")
    op.drop_table("contratos")
    op.drop_table("motoristas")
    op.drop_table("clientes")
    op.drop_table("veiculos")
    op.drop_table("usuarios")
