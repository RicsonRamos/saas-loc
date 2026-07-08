from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PagamentoCreate(BaseModel):
    contrato_id: UUID
    valor: Decimal = Field(gt=0)
    data: datetime
    metodo: str | None = None


class PagamentoOut(BaseModel):
    id: UUID
    contrato_id: UUID
    valor: Decimal
    data: datetime
    status: str
    metodo: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DespesaCreate(BaseModel):
    veiculo_id: UUID | None = None
    categoria: str = Field(min_length=1, max_length=60)
    valor: Decimal = Field(gt=0)
    data: datetime
    descricao: str | None = None


class DespesaOut(BaseModel):
    id: UUID
    veiculo_id: UUID | None
    categoria: str
    valor: Decimal
    data: datetime
    descricao: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DespesaUpdate(BaseModel):
    veiculo_id: UUID | None = None
    categoria: str | None = Field(default=None, min_length=1, max_length=60)
    valor: Decimal | None = Field(default=None, gt=0)
    data: datetime | None = None
    descricao: str | None = None


class RentabilidadeVeiculoOut(BaseModel):
    veiculo_id: UUID
    placa: str
    receita_total: Decimal
    despesa_total: Decimal
    resultado: Decimal
