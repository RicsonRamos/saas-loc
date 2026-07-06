from sqlalchemy.orm import Session
from sqlalchemy import func
from models.cliente import Cliente
from models.veiculo import Veiculo
from models.contrato import Contrato
from models.financeiro import LancamentoFinanceiro
from datetime import datetime

class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def obter_resumo(self):
        # Clientes ativos
        total_clientes = self.db.query(func.count(Cliente.id)).filter(Cliente.ativo == True).scalar() or 0
        
        # Contratos ativos
        contratos_ativos = self.db.query(func.count(Contrato.id)).filter(Contrato.status == "ATIVO").scalar() or 0
        
        # Veículos status
        veiculos_totais = self.db.query(func.count(Veiculo.id)).scalar() or 0
        veiculos_disponiveis = self.db.query(func.count(Veiculo.id)).filter(Veiculo.status == "DISPONIVEL").scalar() or 0
        veiculos_alugados = self.db.query(func.count(Veiculo.id)).filter(Veiculo.status == "LOCADO").scalar() or 0
        veiculos_manutencao = self.db.query(func.count(Veiculo.id)).filter(Veiculo.status == "MANUTENCAO").scalar() or 0
        
        # Financeiro do mês atual
        hoje = datetime.now()
        primeiro_dia_mes = datetime(hoje.year, hoje.month, 1)
        
        receitas = self.db.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == "RECEITA",
            LancamentoFinanceiro.status == "PAGO",
            LancamentoFinanceiro.data_pagamento >= primeiro_dia_mes
        ).scalar() or 0.0
        
        despesas = self.db.query(func.sum(LancamentoFinanceiro.valor)).filter(
            LancamentoFinanceiro.tipo == "DESPESA",
            LancamentoFinanceiro.status == "PAGO",
            LancamentoFinanceiro.data_pagamento >= primeiro_dia_mes
        ).scalar() or 0.0
        
        lucro = receitas - despesas
        
        return {
            "total_clientes": total_clientes,
            "contratos_ativos": contratos_ativos,
            "veiculos_totais": veiculos_totais,
            "veiculos_disponiveis": veiculos_disponiveis,
            "veiculos_alugados": veiculos_alugados,
            "veiculos_manutencao": veiculos_manutencao,
            "receitas_mes": receitas,
            "despesas_mes": despesas,
            "lucro_mes": lucro
        }
