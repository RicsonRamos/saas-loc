from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ContratoCreate(BaseModel):
    cliente_id: UUID
    veiculo_id: UUID
    motorista_id: UUID | None = None
    data_inicio: datetime
    data_fim_prevista: datetime
    valor_diaria: Decimal = Field(gt=0)

    @model_validator(mode="after")
    def valida_periodo(self) -> "ContratoCreate":
        if self.data_fim_prevista <= self.data_inicio:
            raise ValueError("A data final prevista deve ser posterior à data de início.")
        return self


class ContratoDevolucao(BaseModel):
    data_fim_real: datetime | None = None
    km_final: int | None = Field(default=None, ge=0)


class ContratoOut(BaseModel):
    id: UUID
    cliente_id: UUID
    veiculo_id: UUID
    motorista_id: UUID | None
    data_inicio: datetime
    data_fim_prevista: datetime
    data_fim_real: datetime | None
    status: str
    valor_diaria: Decimal
    version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
