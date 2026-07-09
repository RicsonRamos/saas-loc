from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.plano_manutencao import TIPOS_PLANO_MANUTENCAO_VALIDOS


class PlanoManutencaoCreate(BaseModel):
    veiculo_id: UUID
    tipo: str
    descricao: str | None = Field(default=None, max_length=150)
    intervalo_km: int | None = Field(default=None, gt=0)
    intervalo_dias: int | None = Field(default=None, gt=0)
    ultima_execucao_km: int | None = Field(default=None, ge=0)
    ultima_execucao_data: date | None = None
    ativo: bool = True

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_PLANO_MANUTENCAO_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_PLANO_MANUTENCAO_VALIDOS)}")
        return v

    @model_validator(mode="after")
    def valida_intervalo_informado(self) -> "PlanoManutencaoCreate":
        if self.intervalo_km is None and self.intervalo_dias is None:
            raise ValueError("Informe ao menos um intervalo (km ou dias).")
        return self


class PlanoManutencaoUpdate(BaseModel):
    descricao: str | None = Field(default=None, max_length=150)
    intervalo_km: int | None = Field(default=None, gt=0)
    intervalo_dias: int | None = Field(default=None, gt=0)
    ultima_execucao_km: int | None = Field(default=None, ge=0)
    ultima_execucao_data: date | None = None
    ativo: bool | None = None


class PlanoManutencaoOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    tipo: str
    descricao: str | None
    intervalo_km: int | None
    intervalo_dias: int | None
    ultima_execucao_km: int | None
    ultima_execucao_data: date | None
    ativo: bool
    prioridade: str = "normal"
    faltam_km: int | None = None
    faltam_dias: int | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
