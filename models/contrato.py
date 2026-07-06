from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime
from models.usuario import generate_uuid

class Contrato(Base):
    __tablename__ = "contratos"

    id = Column(String, primary_key=True, default=generate_uuid)
    
    cliente_id = Column(String, ForeignKey("clientes.id"), nullable=False, index=True)
    veiculo_id = Column(String, ForeignKey("veiculos.id"), nullable=False, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=True) # Operador que abriu
    
    # Datas e Horas (Data/Hora de Retirada e Devolucao Prevista/Real)
    data_inicio = Column(DateTime, nullable=False)
    data_fim_prevista = Column(DateTime, nullable=False)
    data_devolucao = Column(DateTime, nullable=True)
    
    # Valores e Pagamento
    valor_diaria = Column(Float, nullable=False) # Guardar foto do valor na época
    valor_total = Column(Float, nullable=False)
    desconto = Column(Float, default=0.0)
    caucao = Column(Float, nullable=True)
    forma_pagamento = Column(String(50), nullable=True) # BOLETO, PIX, CARTAO, DINHEIRO
    seguro_incluso = Column(Boolean, default=False)
    
    # Check-in e Check-out operacionais
    km_inicial = Column(Integer, nullable=False)
    km_final = Column(Integer, nullable=True)
    motorista_adicional = Column(String(150), nullable=True)
    
    # Estruturas JSON/Arquivos
    checklist_json = Column(Text, nullable=True) # {'lataria': 'ok', 'pneus': 'ok', 'combustivel': '50%'}
    fotos_paths = Column(Text, nullable=True) # JSON Array of paths
    
    status = Column(String(30), nullable=False, default="ATIVO") # ATIVO, ENCERRADO, CANCELADO, INADIMPLENTE
    
    # Extras Check-out
    diarias_extras = Column(Integer, default=0)
    multas_adicionais = Column(Float, default=0.0)
    avarias = Column(Text, nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cliente = relationship("Cliente")
    veiculo = relationship("Veiculo")
    usuario = relationship("Usuario")
