from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from models.usuario import generate_uuid

class Manutencao(Base):
    __tablename__ = "manutencoes"

    id = Column(String, primary_key=True, default=generate_uuid)
    veiculo_id = Column(String, ForeignKey("veiculos.id"), nullable=False, index=True)
    
    tipo = Column(String(30), nullable=False) # PREVENTIVA, CORRETIVA
    descricao = Column(String(255), nullable=False)
    fornecedor = Column(String(150), nullable=True)
    
    valor = Column(Float, nullable=False, default=0.0)
    
    data_servico = Column(DateTime, nullable=False)
    km_servico = Column(Integer, nullable=False)
    
    proxima_revisao_km = Column(Integer, nullable=True)
    proxima_revisao_data = Column(DateTime, nullable=True)
    
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    veiculo = relationship("Veiculo")
