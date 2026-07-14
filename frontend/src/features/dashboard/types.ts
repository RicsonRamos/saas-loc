export interface VencimentosResumo {
  seguro_30_dias: number;
  licenciamento_30_dias: number;
}

export interface FinanceiroMes {
  receita: string;
  despesas: string;
  lucro: string;
}

export interface FinanceiroMensal {
  mes: string;
  receita: string;
  despesas: string;
  lucro: string;
}

export interface PagamentosResumo {
  quantidade: number;
  valor: string;
}

export interface DashboardKpis {
  contratos_ativos: number;
  taxa_ocupacao: number;
  ticket_medio: string | null;
  receita_por_veiculo: string | null;
  pagamentos_pendentes: PagamentosResumo;
  pagamentos_atrasados: PagamentosResumo;
}

export type PrioridadeAlerta = "normal" | "atencao" | "critico";

export interface Alerta {
  tipo: string;
  mensagem: string;
  prioridade: PrioridadeAlerta;
  veiculo_id: string | null;
  veiculo_placa: string | null;
}

export interface DashboardResumo {
  veiculos_por_status: Record<string, number>;
  vencimentos: VencimentosResumo;
  financeiro_mes: FinanceiroMes | null;
  financeiro_historico: FinanceiroMensal[] | null;
  kpis: DashboardKpis;
  alertas: Alerta[];
}
