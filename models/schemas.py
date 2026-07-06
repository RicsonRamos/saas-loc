from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- USUARIO ---
class UsuarioSchema(BaseModel):
    id: Optional[str] = None
    nome: str
    email: EmailStr
    perfil: str = "OPERADOR"
    ativo: bool = True

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

# --- CLIENTE ---
class ClienteSchema(BaseModel):
    id: Optional[str] = None
    tipo_pessoa: str
    nome: str
    documento: str
    cnh: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    cep: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    observacoes: Optional[str] = None
    ativo: bool = True

# --- VEICULO ---
class VeiculoSchema(BaseModel):
    id: Optional[str] = None
    placa: str = Field(..., max_length=10)
    renavam: Optional[str] = None
    chassi: str
    marca: str
    modelo: str
    ano_fabricacao: int
    ano_modelo: int
    cor: Optional[str] = None
    categoria: Optional[str] = None
    combustivel: Optional[str] = None
    cambio: Optional[str] = None
    portas: Optional[int] = 4
    capacidade: Optional[int] = 5
    quilometragem: int = 0
    status: str = "DISPONIVEL"
    valor_compra: Optional[float] = 0.0
    valor_fipe: Optional[float] = 0.0
    valor_diaria: Optional[float] = 0.0
    seguradora: Optional[str] = None
    apolice: Optional[str] = None
    vencimento_seguro: Optional[datetime] = None
    vencimento_ipva: Optional[datetime] = None
    fotos_paths: Optional[str] = None # JSON dump
    documentos_paths: Optional[str] = None # JSON dump
    observacoes: Optional[str] = None

# --- CONTRATO ---
class ContratoCreateSchema(BaseModel):
    cliente_id: str
    veiculo_id: str
    usuario_id: Optional[str] = None
    data_inicio: datetime
    data_fim_prevista: datetime
    valor_diaria: float
    valor_total: float
    desconto: Optional[float] = 0.0
    caucao: Optional[float] = 0.0
    forma_pagamento: Optional[str] = None
    seguro_incluso: bool = False
    km_inicial: int
    motorista_adicional: Optional[str] = None
    checklist_json: Optional[str] = None
    fotos_paths: Optional[str] = None

class ContratoCheckoutSchema(BaseModel):
    km_final: int
    data_devolucao: datetime
    diarias_extras: Optional[int] = 0
    multas_adicionais: Optional[float] = 0.0
    avarias: Optional[str] = None
    observacoes: Optional[str] = None

# --- FINANCEIRO ---
class LancamentoSchema(BaseModel):
    tipo: str # RECEITA, DESPESA
    valor: float
    categoria: str
    descricao: str
    status: str = "PENDENTE"
    data_vencimento: datetime
    data_pagamento: Optional[datetime] = None
    contrato_id: Optional[str] = None
    veiculo_id: Optional[str] = None

# --- MANUTENCAO ---
class ManutencaoSchema(BaseModel):
    veiculo_id: str
    tipo: str # PREVENTIVA, CORRETIVA
    descricao: str
    fornecedor: Optional[str] = None
    valor: float = 0.0
    data_servico: datetime
    km_servico: int
    proxima_revisao_km: Optional[int] = None
    proxima_revisao_data: Optional[datetime] = None
    observacoes: Optional[str] = None
