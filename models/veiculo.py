from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from core.database import Base
from datetime import datetime
from models.usuario import generate_uuid

class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(String, primary_key=True, default=generate_uuid)
    placa = Column(String(10), unique=True, nullable=False, index=True)
    renavam = Column(String(20), unique=True, nullable=True)
    chassi = Column(String(50), unique=True, nullable=False)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(100), nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    ano_modelo = Column(Integer, nullable=False)
    
    # Aba Geral Expandida
    cor = Column(String(30), nullable=True)
    categoria = Column(String(50), nullable=True)
    combustivel = Column(String(30), nullable=True)
    cambio = Column(String(30), nullable=True) # MANUAL, AUTOMATICO
    portas = Column(Integer, nullable=True, default=4)
    capacidade = Column(Integer, nullable=True, default=5) # Passageiros
    
    quilometragem = Column(Integer, nullable=False, default=0)
    status = Column(String(30), nullable=False, default="DISPONIVEL") # DISPONIVEL, LOCADO, MANUTENCAO, RESERVADO, INATIVO, VENDIDO
    
    # Valores
    valor_compra = Column(Float, nullable=True)
    valor_fipe = Column(Float, nullable=True)
    valor_diaria = Column(Float, nullable=True)
    
    # Documentacao e Seguro
    seguradora = Column(String(100), nullable=True)
    apolice = Column(String(100), nullable=True)
    vencimento_seguro = Column(DateTime, nullable=True)
    vencimento_ipva = Column(DateTime, nullable=True)
    
    # Arquivos (JSON Serialized Strings)
    fotos_paths = Column(Text, nullable=True)
    documentos_paths = Column(Text, nullable=True)
    
    observacoes = Column(Text, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
