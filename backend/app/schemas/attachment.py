from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AttachmentOut(BaseModel):
    id: UUID
    entidade_tipo: str
    entidade_id: UUID
    tipo: str
    nome_original: str
    content_type: str
    tamanho_bytes: int
    usuario_upload_id: UUID
    data_upload: datetime

    model_config = ConfigDict(from_attributes=True)


class AttachmentDownloadOut(BaseModel):
    url: str
