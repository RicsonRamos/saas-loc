from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class VencimentosResumoOut(BaseModel):
    seguro_30_dias: int
    licenciamento_30_dias: int


class FinanceiroMesOut(BaseModel):
    receita: Decimal
    despesas: Decimal
    lucro: Decimal


class AlertaOut(BaseModel):
    tipo: str
    mensagem: str
    prioridade: str
    veiculo_id: UUID | None = None
    veiculo_placa: str | None = None


class DashboardResumoOut(BaseModel):
    veiculos_por_status: dict[str, int]
    vencimentos: VencimentosResumoOut
    financeiro_mes: FinanceiroMesOut | None
    alertas: list[AlertaOut]
