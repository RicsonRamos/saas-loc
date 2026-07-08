from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.pneu import POSICOES_PNEU_VALIDAS, STATUS_PNEU_VALIDOS


class PneuCreate(BaseModel):
    veiculo_id: UUID
    marca: str = Field(min_length=1, max_length=60)
    modelo: str | None = Field(default=None, max_length=60)
    numero_serie: str | None = Field(default=None, max_length=60)
    posicao: str
    data_instalacao: date
    km_instalacao: int = Field(ge=0)
    vida_util_km: int | None = Field(default=None, ge=0)
    status: str = "ativo"

    @field_validator("posicao")
    @classmethod
    def posicao_valida(cls, v: str) -> str:
        if v not in POSICOES_PNEU_VALIDAS:
            raise ValueError(f"Posição inválida. Use uma de: {sorted(POSICOES_PNEU_VALIDAS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str) -> str:
        if v not in STATUS_PNEU_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_PNEU_VALIDOS)}")
        return v


class PneuUpdate(BaseModel):
    marca: str | None = Field(default=None, max_length=60)
    modelo: str | None = Field(default=None, max_length=60)
    numero_serie: str | None = Field(default=None, max_length=60)
    posicao: str | None = None
    data_instalacao: date | None = None
    km_instalacao: int | None = Field(default=None, ge=0)
    vida_util_km: int | None = Field(default=None, ge=0)
    data_troca: date | None = None
    km_troca: int | None = Field(default=None, ge=0)
    status: str | None = None

    @field_validator("posicao")
    @classmethod
    def posicao_valida(cls, v: str | None) -> str | None:
        if v is not None and v not in POSICOES_PNEU_VALIDAS:
            raise ValueError(f"Posição inválida. Use uma de: {sorted(POSICOES_PNEU_VALIDAS)}")
        return v

    @field_validator("status")
    @classmethod
    def status_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in STATUS_PNEU_VALIDOS:
            raise ValueError(f"Status inválido. Use um de: {sorted(STATUS_PNEU_VALIDOS)}")
        return v


class PneuOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    marca: str
    modelo: str | None
    numero_serie: str | None
    posicao: str
    data_instalacao: date
    km_instalacao: int
    vida_util_km: int | None
    data_troca: date | None
    km_troca: int | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
