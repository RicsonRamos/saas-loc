from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.manutencao import TIPOS_MANUTENCAO_VALIDOS


class ManutencaoCreate(BaseModel):
    veiculo_id: UUID
    tipo: str
    data: datetime
    km: int = Field(ge=0)
    custo: Decimal = Field(ge=0)
    oficina: str | None = None
    descricao: str | None = None
    proxima_manutencao_km: int | None = Field(default=None, ge=0)
    proxima_manutencao_data: date | None = None
    em_andamento: bool = False

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_MANUTENCAO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_MANUTENCAO_VALIDOS)}")
        return v


class ManutencaoUpdate(BaseModel):
    tipo: str | None = None
    data: datetime | None = None
    km: int | None = Field(default=None, ge=0)
    custo: Decimal | None = Field(default=None, ge=0)
    oficina: str | None = None
    descricao: str | None = None
    proxima_manutencao_km: int | None = Field(default=None, ge=0)
    proxima_manutencao_data: date | None = None

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str | None) -> str | None:
        if v is not None and v not in TIPOS_MANUTENCAO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_MANUTENCAO_VALIDOS)}")
        return v


class ManutencaoOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    tipo: str
    data: datetime
    km: int
    custo: Decimal
    oficina: str | None
    descricao: str | None
    proxima_manutencao_km: int | None
    proxima_manutencao_data: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
