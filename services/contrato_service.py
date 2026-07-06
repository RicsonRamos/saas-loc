from sqlalchemy.orm import Session
from models.schemas import ContratoCreateSchema, ContratoCheckoutSchema
from repositories.contrato_repository import ContratoRepository
from repositories.veiculo_repository import VeiculoRepository
from datetime import datetime

class ContratoService:
    def __init__(self, db: Session):
        self.repo = ContratoRepository(db)
        self.veiculo_repo = VeiculoRepository(db)

    def abrir_contrato(self, data: ContratoCreateSchema):
        # 1. Verifica se veiculo ta disponivel
        veiculo = self.veiculo_repo.get_by_id(data.veiculo_id)
        if not veiculo or veiculo.status != "DISPONIVEL":
            raise ValueError("Veículo não está disponível para locação.")
        
        # 2. Cria o contrato
        contrato = self.repo.create({
            "cliente_id": data.cliente_id,
            "veiculo_id": data.veiculo_id,
            "usuario_id": data.usuario_id,
            "data_inicio": data.data_inicio,
            "data_fim_prevista": data.data_fim_prevista,
            "valor_diaria": data.valor_diaria,
            "valor_total": data.valor_total,
            "desconto": data.desconto,
            "caucao": data.caucao,
            "forma_pagamento": data.forma_pagamento,
            "km_inicial": data.km_inicial,
            "motorista_adicional": data.motorista_adicional,
            "checklist_json": data.checklist_json,
            "status": "ATIVO"
        })
        
        # 3. Muda status do veiculo
        self.veiculo_repo.update(veiculo, {"status": "LOCADO"})
        
        return contrato

    def encerrar_contrato(self, contrato_id: str, data: ContratoCheckoutSchema):
        contrato = self.repo.get_by_id(contrato_id)
        if not contrato or contrato.status != "ATIVO":
            raise ValueError("Contrato inválido ou não está ativo.")
            
        if data.km_final < contrato.km_inicial:
            raise ValueError("KM Final não pode ser menor que o KM Inicial.")
            
        self.repo.update(contrato, {
            "status": "ENCERRADO",
            "data_devolucao": data.data_devolucao,
            "km_final": data.km_final,
            "diarias_extras": data.diarias_extras,
            "multas_adicionais": data.multas_adicionais,
            "avarias": data.avarias,
            "observacoes": data.observacoes
        })
        
        # Libera veiculo
        veiculo = self.veiculo_repo.get_by_id(contrato.veiculo_id)
        if veiculo:
            self.veiculo_repo.update(veiculo, {
                "status": "DISPONIVEL",
                "quilometragem": data.km_final
            })
            
        return contrato

    def listar_todos(self):
        return self.repo.get_all()
