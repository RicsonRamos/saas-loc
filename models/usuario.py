from sqlalchemy import Column, String, Boolean, DateTime
from core.database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(50), nullable=False, default="OPERADOR") # ADMIN, GERENTE, FINANCEIRO, OPERADOR, MECANICO
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
