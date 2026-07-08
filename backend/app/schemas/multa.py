from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.multa import STATUS_MULTA_VALIDOS


class MultaCreate(BaseModel):
    veiculo_id: UUID
    cliente_id: UUID | None = None
    contrato_id: UUID | None = None
    data: datetime
    infracao: str = Field(min_length=1, max_length=255)
    local: str | None = Field(default=None, max_length=255)
    valor: Decimal = Field(gt=0)
    pontos: int | None = Field(default=None, ge=0)
    status: str = "pendente"
    observacoes: str | None = None

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in STATUS_MULTA_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_MULTA_VALIDOS)}")
        return v


class MultaUpdate(BaseModel):
    data: datetime | None = None
    infracao: str | None = Field(default=None, max_length=255)
    local: str | None = Field(default=None, max_length=255)
    valor: Decimal | None = Field(default=None, gt=0)
    pontos: int | None = Field(default=None, ge=0)
    status: str | None = None
    observacoes: str | None = None

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_MULTA_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_MULTA_VALIDOS)}")
        return v


class MultaOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    cliente_id: UUID | None
    contrato_id: UUID | None
    data: datetime
    infracao: str
    local: str | None
    valor: Decimal
    pontos: int | None
    status: str
    observacoes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
