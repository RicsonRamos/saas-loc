export interface VencimentosResumo {
  seguro_30_dias: number;
  licenciamento_30_dias: number;
}

export interface FinanceiroMes {
  receita: string;
  despesas: string;
  lucro: string;
}

export interface Alerta {
  tipo: string;
  mensagem: string;
  veiculo_id: string | null;
  veiculo_placa: string | null;
}

export interface DashboardResumo {
  veiculos_por_status: Record<string, number>;
  vencimentos: VencimentosResumo;
  financeiro_mes: FinanceiroMes | null;
  alertas: Alerta[];
}
