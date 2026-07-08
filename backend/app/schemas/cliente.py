from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.cliente import STATUS_CLIENTE_VALIDOS
from app.schemas.dano import DanoOut
from app.schemas.multa import MultaOut
from app.schemas.sinistro import SinistroOut


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    documento: str = Field(min_length=11, max_length=20)
    rg: str | None = Field(default=None, max_length=20)
    rg_orgao_emissor: str | None = Field(default=None, max_length=20)
    data_nascimento: date | None = None

    email: str | None = None
    telefone: str | None = None
    celular_secundario: str | None = None
    whatsapp: str | None = None

    cep: str | None = Field(default=None, max_length=10)
    logradouro: str | None = Field(default=None, max_length=150)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=60)
    bairro: str | None = Field(default=None, max_length=100)
    cidade: str | None = Field(default=None, max_length=100)
    estado: str | None = Field(default=None, max_length=2)

    cnh_numero: str | None = Field(default=None, max_length=20)
    cnh_categoria: str | None = Field(default=None, max_length=5)
    cnh_emissao: date | None = None
    cnh_vencimento: date | None = None
    cnh_orgao_emissor: str | None = Field(default=None, max_length=20)
    cnh_primeira_habilitacao: date | None = None
    cnh_ear: bool = False

    limite_credito: Decimal | None = Field(default=None, ge=0)
    forma_pagamento_preferida: str | None = Field(default=None, max_length=30)
    banco: str | None = Field(default=None, max_length=60)
    agencia: str | None = Field(default=None, max_length=20)
    conta: str | None = Field(default=None, max_length=30)
    pix: str | None = Field(default=None, max_length=100)
    caucao_padrao: Decimal | None = Field(default=None, ge=0)

    contato_emergencia_nome: str | None = Field(default=None, max_length=150)
    contato_emergencia_parentesco: str | None = Field(default=None, max_length=60)
    contato_emergencia_telefone: str | None = None
    contato_emergencia_whatsapp: str | None = None

    observacoes: str | None = None


class ClienteUpdate(BaseModel):
    nome: str | None = Field(default=None, max_length=150)
    rg: str | None = Field(default=None, max_length=20)
    rg_orgao_emissor: str | None = Field(default=None, max_length=20)
    data_nascimento: date | None = None

    email: str | None = None
    telefone: str | None = None
    celular_secundario: str | None = None
    whatsapp: str | None = None

    cep: str | None = Field(default=None, max_length=10)
    logradouro: str | None = Field(default=None, max_length=150)
    numero: str | None = Field(default=None, max_length=20)
    complemento: str | None = Field(default=None, max_length=60)
    bairro: str | None = Field(default=None, max_length=100)
    cidade: str | None = Field(default=None, max_length=100)
    estado: str | None = Field(default=None, max_length=2)

    cnh_numero: str | None = Field(default=None, max_length=20)
    cnh_categoria: str | None = Field(default=None, max_length=5)
    cnh_emissao: date | None = None
    cnh_vencimento: date | None = None
    cnh_orgao_emissor: str | None = Field(default=None, max_length=20)
    cnh_primeira_habilitacao: date | None = None
    cnh_ear: bool | None = None

    limite_credito: Decimal | None = Field(default=None, ge=0)
    forma_pagamento_preferida: str | None = Field(default=None, max_length=30)
    banco: str | None = Field(default=None, max_length=60)
    agencia: str | None = Field(default=None, max_length=20)
    conta: str | None = Field(default=None, max_length=30)
    pix: str | None = Field(default=None, max_length=100)
    caucao_padrao: Decimal | None = Field(default=None, ge=0)

    contato_emergencia_nome: str | None = Field(default=None, max_length=150)
    contato_emergencia_parentesco: str | None = Field(default=None, max_length=60)
    contato_emergencia_telefone: str | None = None
    contato_emergencia_whatsapp: str | None = None

    status: str | None = None
    observacoes: str | None = None

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_CLIENTE_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_CLIENTE_VALIDOS)}")
        return v


class ClienteOut(BaseModel):
    id: UUID
    nome: str
    documento: str
    rg: str | None
    rg_orgao_emissor: str | None
    data_nascimento: date | None

    email: str | None
    telefone: str | None
    celular_secundario: str | None
    whatsapp: str | None

    cep: str | None
    logradouro: str | None
    numero: str | None
    complemento: str | None
    bairro: str | None
    cidade: str | None
    estado: str | None

    cnh_numero: str | None
    cnh_categoria: str | None
    cnh_emissao: date | None
    cnh_vencimento: date | None
    cnh_orgao_emissor: str | None
    cnh_primeira_habilitacao: date | None
    cnh_ear: bool

    limite_credito: Decimal | None
    forma_pagamento_preferida: str | None
    banco: str | None
    agencia: str | None
    conta: str | None
    pix: str | None
    caucao_padrao: Decimal | None

    contato_emergencia_nome: str | None
    contato_emergencia_parentesco: str | None
    contato_emergencia_telefone: str | None
    contato_emergencia_whatsapp: str | None

    status: str
    observacoes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoricoLocacaoClienteOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    veiculo_placa: str
    veiculo_modelo: str
    data_inicio: datetime
    data_fim_prevista: datetime
    data_fim_real: datetime | None
    status: str
    valor_diaria: Decimal
    km_inicio: int | None
    km_final: int | None


class ResumoFinanceiroClienteOut(BaseModel):
    total_pago: Decimal
    total_pendente: Decimal
    total_estornado: Decimal


class AlertaClienteOut(BaseModel):
    tipo: str
    mensagem: str


class FichaClienteOut(BaseModel):
    status: str
    cnh_categoria: str | None
    cnh_vencimento: date | None
    locacoes_realizadas: int
    locacao_atual: bool
    veiculo_atual_placa: str | None
    veiculo_atual_modelo: str | None
    valor_total_gasto: Decimal
    pendencias: Decimal
    avaliacao_estrelas: int


class HistoricoClienteOut(BaseModel):
    ficha: FichaClienteOut
    locacoes: list[HistoricoLocacaoClienteOut]
    financeiro: ResumoFinanceiroClienteOut
    alertas: list[AlertaClienteOut]
    multas: list[MultaOut]
    sinistros: list[SinistroOut]
    danos: list[DanoOut]
