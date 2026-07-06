from sqlalchemy.orm import Session
from models.usuario import Usuario
from repositories.base_repository import BaseRepository
from typing import Optional

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, db: Session):
        super().__init__(db, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(self.model).filter(self.model.email == email).first()
