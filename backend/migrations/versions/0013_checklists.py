"""checklists: vistoria de entrega/devolucao com itens e assinatura digital

Revision ID: 0013
Revises: 0012
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


def _fk_uuid(nome: str, tabela_referenciada: str, nullable: bool = False) -> sa.Column:
    return sa.Column(
        nome,
        postgresql.UUID(as_uuid=True),
        sa.ForeignKey(f"{tabela_referenciada}.id"),
        nullable=nullable,
    )


revision: str = "0013"
down_revision: str | None = "0012"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "checklists",
        *_metadados_padrao(),
        _fk_uuid("contrato_id", "contratos"),
        sa.Column("tipo", sa.String(15), nullable=False),
        sa.Column("data", sa.DateTime(timezone=True), nullable=False),
        _fk_uuid("usuario_id", "usuarios"),
        sa.Column("km", sa.Integer(), nullable=False),
        sa.Column("combustivel", sa.String(20), nullable=True),
        sa.Column("observacoes_gerais", sa.Text(), nullable=True),
        sa.Column("status", sa.String(15), nullable=False, server_default="concluido"),
    )
    op.create_index("ix_checklists_contrato_id", "checklists", ["contrato_id"])
    op.create_index(
        "uq_checklists_contrato_tipo_ativo",
        "checklists",
        ["contrato_id", "tipo"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
    )

    op.create_table(
        "checklist_itens",
        *_metadados_padrao(),
        _fk_uuid("checklist_id", "checklists"),
        sa.Column("item", sa.String(30), nullable=False),
        sa.Column("situacao", sa.String(15), nullable=False),
        sa.Column("observacao", sa.Text(), nullable=True),
        _fk_uuid("foto_attachment_id", "attachments", nullable=True),
    )
    op.create_index("ix_checklist_itens_checklist_id", "checklist_itens", ["checklist_id"])

    op.create_table(
        "assinaturas",
        *_metadados_padrao(),
        _fk_uuid("checklist_id", "checklists"),
        _fk_uuid("attachment_id", "attachments"),
        _fk_uuid("usuario_id", "usuarios"),
        sa.Column("responsavel_nome", sa.String(150), nullable=False),
        sa.Column(
            "data_hora", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.create_index("ix_assinaturas_checklist_id", "assinaturas", ["checklist_id"])


def downgrade() -> None:
    op.drop_table("assinaturas")
    op.drop_table("checklist_itens")
    op.drop_index("uq_checklists_contrato_tipo_ativo", table_name="checklists")
    op.drop_table("checklists")
