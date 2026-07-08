from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    password: str
    role: str


class UsuarioOut(BaseModel):
    id: UUID
    nome: str
    email: EmailStr
    role: str
    ativo: bool

    model_config = ConfigDict(from_attributes=True)
