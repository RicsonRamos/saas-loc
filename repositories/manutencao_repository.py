from sqlalchemy.orm import Session
from models.manutencao import Manutencao
from repositories.base_repository import BaseRepository
from typing import List

class ManutencaoRepository(BaseRepository[Manutencao]):
    def __init__(self, db: Session):
        super().__init__(db, Manutencao)

    def get_by_veiculo(self, veiculo_id: str) -> List[Manutencao]:
        return self.db.query(self.model).filter(self.model.veiculo_id == veiculo_id).all()
