from sqlalchemy.orm import Session
from models.cliente import Cliente
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ClienteRepository(BaseRepository[Cliente]):
    def __init__(self, db: Session):
        super().__init__(db, Cliente)

    def get_by_document(self, documento: str) -> Optional[Cliente]:
        return self.db.query(self.model).filter(self.model.documento == documento).first()
    
    def search_by_name(self, name: str) -> List[Cliente]:
        return self.db.query(self.model).filter(self.model.nome.ilike(f"%{name}%")).all()
