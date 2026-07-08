export interface HistoricoContrato {
  id: string;
  cliente_id: string;
  cliente_nome: string;
  data_inicio: string;
  data_fim_prevista: string;
  data_fim_real: string | null;
  status: string;
  valor_diaria: string;
  km_inicio: number | null;
  km_final: number | null;
}

export interface HistoricoManutencao {
  id: string;
  tipo: string;
  data: string;
  km: number;
  custo: string;
  oficina: string | null;
}

export interface HistoricoDespesa {
  id: string;
  categoria: string;
  valor: string;
  data: string;
  descricao: string | null;
}

export interface HistoricoVeiculo {
  contratos: HistoricoContrato[];
  manutencoes: HistoricoManutencao[];
  despesas: HistoricoDespesa[];
}
