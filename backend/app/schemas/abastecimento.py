from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, computed_field


class AbastecimentoCreate(BaseModel):
    veiculo_id: UUID
    contrato_id: UUID | None = None
    data: datetime
    posto: str | None = Field(default=None, max_length=150)
    litros: Decimal = Field(gt=0)
    valor: Decimal = Field(gt=0)
    km: int = Field(ge=0)
    tipo_combustivel: str | None = Field(default=None, max_length=30)


class AbastecimentoUpdate(BaseModel):
    data: datetime | None = None
    posto: str | None = Field(default=None, max_length=150)
    litros: Decimal | None = Field(default=None, gt=0)
    valor: Decimal | None = Field(default=None, gt=0)
    km: int | None = Field(default=None, ge=0)
    tipo_combustivel: str | None = Field(default=None, max_length=30)


class AbastecimentoOut(BaseModel):
    id: UUID
    veiculo_id: UUID
    contrato_id: UUID | None
    data: datetime
    posto: str | None
    litros: Decimal
    valor: Decimal
    km: int
    tipo_combustivel: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def valor_por_litro(self) -> Decimal:
        return round(self.valor / self.litros, 3)
