import type { Dano, Multa, Sinistro } from "@/features/frota/incidentesTypes";

export interface HistoricoLocacaoCliente {
  id: string;
  veiculo_id: string;
  veiculo_placa: string;
  veiculo_modelo: string;
  data_inicio: string;
  data_fim_prevista: string;
  data_fim_real: string | null;
  status: string;
  valor_diaria: string;
  km_inicio: number | null;
  km_final: number | null;
}

export interface ResumoFinanceiroCliente {
  total_pago: string;
  total_pendente: string;
  total_estornado: string;
}

export interface AlertaCliente {
  tipo: string;
  mensagem: string;
}

export interface FichaCliente {
  status: string;
  cnh_categoria: string | null;
  cnh_vencimento: string | null;
  locacoes_realizadas: number;
  locacao_atual: boolean;
  veiculo_atual_placa: string | null;
  veiculo_atual_modelo: string | null;
  valor_total_gasto: string;
  pendencias: string;
  avaliacao_estrelas: number;
}

export interface HistoricoCliente {
  ficha: FichaCliente;
  locacoes: HistoricoLocacaoCliente[];
  financeiro: ResumoFinanceiroCliente;
  alertas: AlertaCliente[];
  multas: Multa[];
  sinistros: Sinistro[];
  danos: Dano[];
}
