from datetime import date
from decimal import Decimal

from sqlalchemy import Boolean, Date, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import TimestampedBase

STATUS_ATIVO = "ativo"
STATUS_BLOQUEADO = "bloqueado"
STATUS_INADIMPLENTE = "inadimplente"
STATUS_EM_ANALISE = "em_analise"
STATUS_INATIVO = "inativo"

STATUS_CLIENTE_VALIDOS = {
    STATUS_ATIVO,
    STATUS_BLOQUEADO,
    STATUS_INADIMPLENTE,
    STATUS_EM_ANALISE,
    STATUS_INATIVO,
}


class Cliente(TimestampedBase):
    __tablename__ = "clientes"

    # Dados pessoais
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    documento: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    rg: Mapped[str | None] = mapped_column(String(20), nullable=True)
    rg_orgao_emissor: Mapped[str | None] = mapped_column(String(20), nullable=True)
    data_nascimento: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Contatos
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    celular_secundario: Mapped[str | None] = mapped_column(String(30), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Endereço
    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    logradouro: Mapped[str | None] = mapped_column(String(150), nullable=True)
    numero: Mapped[str | None] = mapped_column(String(20), nullable=True)
    complemento: Mapped[str | None] = mapped_column(String(60), nullable=True)
    bairro: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cidade: Mapped[str | None] = mapped_column(String(100), nullable=True)
    estado: Mapped[str | None] = mapped_column(String(2), nullable=True)

    # CNH
    cnh_numero: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cnh_categoria: Mapped[str | None] = mapped_column(String(5), nullable=True)
    cnh_emissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_vencimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_orgao_emissor: Mapped[str | None] = mapped_column(String(20), nullable=True)
    cnh_primeira_habilitacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_ear: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Dados financeiros
    limite_credito: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    forma_pagamento_preferida: Mapped[str | None] = mapped_column(String(30), nullable=True)
    banco: Mapped[str | None] = mapped_column(String(60), nullable=True)
    agencia: Mapped[str | None] = mapped_column(String(20), nullable=True)
    conta: Mapped[str | None] = mapped_column(String(30), nullable=True)
    pix: Mapped[str | None] = mapped_column(String(100), nullable=True)
    caucao_padrao: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    # Contato de emergência
    contato_emergencia_nome: Mapped[str | None] = mapped_column(String(150), nullable=True)
    contato_emergencia_parentesco: Mapped[str | None] = mapped_column(String(60), nullable=True)
    contato_emergencia_telefone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    contato_emergencia_whatsapp: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Situação e observações
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=STATUS_ATIVO)
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
