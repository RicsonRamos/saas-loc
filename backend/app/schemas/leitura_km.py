from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class LeituraKmCreate(BaseModel):
    veiculo_id: UUID
    km: int = Field(ge=0)
    data_leitura: datetime
    observacao: str | None = None


class LeituraKmOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    usuario_id: UUID
    km: int
    data_leitura: datetime
    observacao: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
