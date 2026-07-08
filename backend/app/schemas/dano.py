from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.dano import STATUS_DANO_VALIDOS, TIPOS_DANO_VALIDOS


class DanoCreate(BaseModel):
    veiculo_id: UUID
    cliente_id: UUID | None = None
    contrato_id: UUID | None = None
    tipo: str
    descricao: str | None = None
    data: date
    valor_reparo: Decimal | None = Field(default=None, ge=0)
    status: str = "pendente"

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_DANO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_DANO_VALIDOS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in STATUS_DANO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_DANO_VALIDOS)}")
        return v


class DanoUpdate(BaseModel):
    tipo: str | None = None
    descricao: str | None = None
    data: date | None = None
    valor_reparo: Decimal | None = Field(default=None, ge=0)
    status: str | None = None

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in TIPOS_DANO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_DANO_VALIDOS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_DANO_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_DANO_VALIDOS)}")
        return v


class DanoOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    cliente_id: UUID | None
    contrato_id: UUID | None
    tipo: str
    descricao: str | None
    data: date
    valor_reparo: Decimal | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
