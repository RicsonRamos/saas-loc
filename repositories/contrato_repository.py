from sqlalchemy.orm import Session
from models.contrato import Contrato
from repositories.base_repository import BaseRepository
from typing import Optional, List

class ContratoRepository(BaseRepository[Contrato]):
    def __init__(self, db: Session):
        super().__init__(db, Contrato)

    def get_ativos_por_veiculo(self, veiculo_id: str) -> List[Contrato]:
        return self.db.query(self.model).filter(
            self.model.veiculo_id == veiculo_id,
            self.model.status == "ATIVO"
        ).all()
        
    def get_with_relations(self, id: str) -> Optional[Contrato]:
        # Como as relationships lazy loading ja trazem, podemos usar isso se necessario,
        # ou usar joinedload() do sqlalchemy se quisermos otimizar as queries.
        return self.db.query(self.model).filter(self.model.id == id).first()
