from sqlalchemy import Column, String, DateTime, Text, Boolean
from core.database import Base
from datetime import datetime
from models.usuario import generate_uuid

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(String, primary_key=True, default=generate_uuid)
    tipo_pessoa = Column(String(20), nullable=False) # FISICA, JURIDICA
    nome = Column(String(150), nullable=False)
    documento = Column(String(20), unique=True, nullable=False, index=True) # CPF ou CNPJ
    cnh = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    
    # Endereco
    cep = Column(String(10), nullable=True)
    logradouro = Column(String(150), nullable=True)
    numero = Column(String(20), nullable=True)
    complemento = Column(String(100), nullable=True)
    bairro = Column(String(100), nullable=True)
    cidade = Column(String(100), nullable=True)
    uf = Column(String(2), nullable=True)
    
    observacoes = Column(Text, nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
