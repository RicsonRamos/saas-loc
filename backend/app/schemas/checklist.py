from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.checklist import (
    ITENS_CHECKLIST_VALIDOS,
    SITUACOES_ITEM_VALIDAS,
    TIPOS_CHECKLIST_VALIDOS,
)


class ChecklistItemCreate(BaseModel):
    item: str
    situacao: str
    observacao: str | None = None
    foto_attachment_id: UUID | None = None

    @field_validator("item")
    @classmethod
    def item_valido(cls, v: str) -> str:
        if v not in ITENS_CHECKLIST_VALIDOS:
            raise ValueError(f"Item inválido. Use um de: {sorted(ITENS_CHECKLIST_VALIDOS)}")
        return v

    @field_validator("situacao")
    @classmethod
    def situacao_valida(cls, v: str) -> str:
        if v not in SITUACOES_ITEM_VALIDAS:
            raise ValueError(f"Situação inválida. Use uma de: {sorted(SITUACOES_ITEM_VALIDAS)}")
        return v


class ChecklistItemFotoUpdate(BaseModel):
    foto_attachment_id: UUID


class ChecklistItemOut(BaseModel):
    id: UUID
    item: str
    situacao: str
    observacao: str | None
    foto_attachment_id: UUID | None

    model_config = ConfigDict(from_attributes=True)


class ChecklistCreate(BaseModel):
    contrato_id: UUID
    tipo: str
    data: datetime
    km: int = Field(ge=0)
    combustivel: str | None = Field(default=None, max_length=20)
    observacoes_gerais: str | None = None
    itens: list[ChecklistItemCreate] = Field(default_factory=list)

    @field_validator("tipo")
    @classmethod
    def tipo_valido(cls, v: str) -> str:
        if v not in TIPOS_CHECKLIST_VALIDOS:
            raise ValueError(f"Tipo inválido. Use um de: {sorted(TIPOS_CHECKLIST_VALIDOS)}")
        return v


class ChecklistOut(BaseModel):
    id: UUID
    contrato_id: UUID
    tipo: str
    data: datetime
    usuario_id: UUID
    km: int
    combustivel: str | None
    observacoes_gerais: str | None
    status: str
    itens: list[ChecklistItemOut]

    model_config = ConfigDict(from_attributes=True)


class AssinaturaCreate(BaseModel):
    attachment_id: UUID
    responsavel_nome: str = Field(min_length=1, max_length=150)


class AssinaturaOut(BaseModel):
    id: UUID
    checklist_id: UUID
    attachment_id: UUID
    usuario_id: UUID
    responsavel_nome: str
    data_hora: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemComparacaoOut(BaseModel):
    item: str
    situacao_entrega: str | None
    situacao_devolucao: str | None
    mudou: bool


class ChecklistComparacaoOut(BaseModel):
    checklist_entrega_id: UUID
    checklist_devolucao_id: UUID
    itens: list[ItemComparacaoOut]
