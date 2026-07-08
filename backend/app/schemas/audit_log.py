from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogOut(BaseModel):
    id: UUID
    usuario_id: UUID | None
    acao: str
    entidade: str
    entidade_id: UUID
    dados_anteriores: dict | None
    dados_novos: dict | None
    data_hora: datetime
    ip: str | None
    descricao: str | None

    model_config = ConfigDict(from_attributes=True)
