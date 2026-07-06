import bcrypt
from sqlalchemy.orm import Session
from models.schemas import LoginSchema, UsuarioSchema
from repositories.usuario_repository import UsuarioRepository

class AuthService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def login(self, data: LoginSchema) -> UsuarioSchema:
        user = self.repo.get_by_email(data.email)
        if not user:
            raise ValueError("Usuário ou senha inválidos.")
        
        if not bcrypt.checkpw(data.senha.encode("utf-8"), user.senha_hash.encode("utf-8")):
            raise ValueError("Usuário ou senha inválidos.")
            
        if not user.ativo:
            raise ValueError("Usuário inativo.")
            
        return UsuarioSchema(
            id=user.id,
            nome=user.nome,
            email=user.email,
            perfil=user.perfil,
            ativo=user.ativo
        )
