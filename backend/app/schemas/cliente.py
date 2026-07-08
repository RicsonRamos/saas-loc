from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    documento: str = Field(min_length=11, max_length=20)
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None


class ClienteUpdate(BaseModel):
    nome: str | None = Field(default=None, max_length=150)
    email: str | None = None
    telefone: str | None = None
    endereco: str | None = None


class ClienteOut(BaseModel):
    id: UUID
    nome: str
    documento: str
    email: str | None
    telefone: str | None
    endereco: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
