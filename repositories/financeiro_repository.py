from sqlalchemy.orm import Session
from models.financeiro import LancamentoFinanceiro
from repositories.base_repository import BaseRepository
from typing import List
from datetime import datetime

class FinanceiroRepository(BaseRepository[LancamentoFinanceiro]):
    def __init__(self, db: Session):
        super().__init__(db, LancamentoFinanceiro)

    def get_by_period(self, start_date: datetime, end_date: datetime) -> List[LancamentoFinanceiro]:
        return self.db.query(self.model).filter(
            self.model.data_vencimento >= start_date,
            self.model.data_vencimento <= end_date
        ).all()
        
    def get_pendentes(self) -> List[LancamentoFinanceiro]:
        return self.db.query(self.model).filter(self.model.status == "PENDENTE").all()
