from sqlalchemy.orm import Session
from models.veiculo import Veiculo
from repositories.base_repository import BaseRepository
from typing import Optional, List

class VeiculoRepository(BaseRepository[Veiculo]):
    def __init__(self, db: Session):
        super().__init__(db, Veiculo)

    def get_by_placa(self, placa: str) -> Optional[Veiculo]:
        return self.db.query(self.model).filter(self.model.placa == placa).first()
    
    def get_disponiveis(self) -> List[Veiculo]:
        return self.db.query(self.model).filter(self.model.status == "DISPONIVEL").all()
