from sqlalchemy import Column, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from models.usuario import generate_uuid

class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos_financeiros"

    id = Column(String, primary_key=True, default=generate_uuid)
    tipo = Column(String(20), nullable=False) # RECEITA, DESPESA
    valor = Column(Float, nullable=False)
    categoria = Column(String(50), nullable=False) # ALUGUEL, MANUTENCAO, SALARIOS, IMPOSTOS, etc
    descricao = Column(String(255), nullable=False)
    
    status = Column(String(30), nullable=False, default="PENDENTE") # PENDENTE, PAGO, CANCELADO
    
    data_vencimento = Column(DateTime, nullable=False)
    data_pagamento = Column(DateTime, nullable=True)
    
    contrato_id = Column(String, ForeignKey("contratos.id"), nullable=True)
    veiculo_id = Column(String, ForeignKey("veiculos.id"), nullable=True)
    
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    contrato = relationship("Contrato")
    veiculo = relationship("Veiculo")
