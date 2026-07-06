from sqlalchemy.orm import Session
from models.schemas import LancamentoSchema
from repositories.financeiro_repository import FinanceiroRepository

class FinanceiroService:
    def __init__(self, db: Session):
        self.repo = FinanceiroRepository(db)

    def registrar_lancamento(self, data: LancamentoSchema):
        return self.repo.create(data.model_dump(exclude_unset=True))
        
    def listar_pendentes(self):
        return self.repo.get_pendentes()
        
    def baixar_lancamento(self, id: str, data_pagamento):
        lanc = self.repo.get_by_id(id)
        if not lanc:
            raise ValueError("Lançamento não encontrado.")
        if lanc.status != "PENDENTE":
            raise ValueError("Apenas lançamentos PENDENTES podem ser baixados.")
            
        self.repo.update(lanc, {
            "status": "PAGO",
            "data_pagamento": data_pagamento
        })
        return lanc
