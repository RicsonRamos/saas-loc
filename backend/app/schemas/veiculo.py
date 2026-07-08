from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.veiculo import STATUS_VEICULO_VALIDOS
from app.schemas.dano import DanoOut
from app.schemas.multa import MultaOut
from app.schemas.sinistro import SinistroOut


class VeiculoCreate(BaseModel):
    placa: str = Field(min_length=7, max_length=10)
    modelo: str = Field(min_length=1, max_length=120)
    ano: int = Field(ge=1950, le=2100)
    km_atual: int = Field(default=0, ge=0)
    filial_id: str | None = None
    marca: str | None = Field(default=None, max_length=60)
    cor: str | None = Field(default=None, max_length=40)
    categoria: str | None = Field(default=None, max_length=60)
    chassi: str | None = Field(default=None, max_length=30)
    renavam: str | None = Field(default=None, max_length=20)
    combustivel: str | None = Field(default=None, max_length=30)
    cambio: str | None = Field(default=None, max_length=30)
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None

    @field_validator("placa")
    @classmethod
    def placa_maiuscula(cls, v: str) -> str:
        return v.strip().upper()


class VeiculoUpdate(BaseModel):
    modelo: str | None = Field(default=None, max_length=120)
    ano: int | None = Field(default=None, ge=1950, le=2100)
    km_atual: int | None = Field(default=None, ge=0)
    status: str | None = None
    filial_id: str | None = None
    marca: str | None = Field(default=None, max_length=60)
    cor: str | None = Field(default=None, max_length=40)
    categoria: str | None = Field(default=None, max_length=60)
    chassi: str | None = Field(default=None, max_length=30)
    renavam: str | None = Field(default=None, max_length=20)
    combustivel: str | None = Field(default=None, max_length=30)
    cambio: str | None = Field(default=None, max_length=30)
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_VEICULO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_VEICULO_VALIDOS)}")
        return v


class VeiculoOut(BaseModel):
    id: UUID
    placa: str
    modelo: str
    ano: int
    status: str
    km_atual: int
    filial_id: str | None
    marca: str | None
    cor: str | None
    categoria: str | None
    chassi: str | None
    renavam: str | None
    combustivel: str | None
    cambio: str | None
    vencimento_licenciamento: date | None
    vencimento_seguro: date | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HistoricoContratoOut(BaseModel):
    id: UUID
    cliente_id: UUID
    cliente_nome: str
    data_inicio: datetime
    data_fim_prevista: datetime
    data_fim_real: datetime | None
    status: str
    valor_diaria: Decimal
    km_inicio: int | None
    km_final: int | None


class HistoricoManutencaoOut(BaseModel):
    id: UUID
    tipo: str
    data: datetime
    km: int
    custo: Decimal
    oficina: str | None

    model_config = ConfigDict(from_attributes=True)


class HistoricoDespesaOut(BaseModel):
    id: UUID
    categoria: str
    valor: Decimal
    data: datetime
    descricao: str | None

    model_config = ConfigDict(from_attributes=True)


class HistoricoVeiculoOut(BaseModel):
    contratos: list[HistoricoContratoOut]
    manutencoes: list[HistoricoManutencaoOut]
    despesas: list[HistoricoDespesaOut]
    multas: list[MultaOut]
    sinistros: list[SinistroOut]
    danos: list[DanoOut]
