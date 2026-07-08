from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.sinistro import STATUS_SINISTRO_VALIDOS, TIPOS_SINISTRO_VALIDOS


class SinistroCreate(BaseModel):
    veiculo_id: UUID
    cliente_id: UUID | None = None
    contrato_id: UUID | None = None
    tipo: str
    data: datetime
    descricao: str | None = None
    valor_prejuizo: Decimal | None = Field(default=None, ge=0)
    seguradora_acionada: bool = False
    status: str = "aberto"

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_SINISTRO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_SINISTRO_VALIDOS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in STATUS_SINISTRO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_SINISTRO_VALIDOS)}")
        return v


class SinistroUpdate(BaseModel):
    tipo: str | None = None
    data: datetime | None = None
    descricao: str | None = None
    valor_prejuizo: Decimal | None = Field(default=None, ge=0)
    seguradora_acionada: bool | None = None
    status: str | None = None

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in TIPOS_SINISTRO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_SINISTRO_VALIDOS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_SINISTRO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_SINISTRO_VALIDOS)}")
        return v


class SinistroOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    cliente_id: UUID | None
    contrato_id: UUID | None
    tipo: str
    data: datetime
    descricao: str | None
    valor_prejuizo: Decimal | None
    seguradora_acionada: bool
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
