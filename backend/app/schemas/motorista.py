from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class MotoristaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    cnh: str = Field(min_length=5, max_length=20)
    validade_cnh: date
    telefone: str | None = None
    cliente_id: UUID | None = None
    parentesco: str | None = Field(default=None, max_length=60)


class MotoristaUpdate(BaseModel):
    nome: str | None = Field(default=None, max_length=150)
    validade_cnh: date | None = None
    telefone: str | None = None
    cliente_id: UUID | None = None
    parentesco: str | None = Field(default=None, max_length=60)


class MotoristaOut(BaseModel):
    id: UUID
    nome: str
    cnh: str
    validade_cnh: date
    telefone: str | None
    cliente_id: UUID | None
    parentesco: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
