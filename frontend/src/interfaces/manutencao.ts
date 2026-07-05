export type TipoManutencao = 'PREVENTIVA' | 'CORRETIVA';

export interface Manutencao {
  id: string;
  veiculoId: string;
  veiculoPlaca: string;
  tipo: TipoManutencao;
  descricao: string;
  kmManutencao: number;
  dataInicio: string;
  dataFim?: string;
  custo: number;
  concluida: boolean;
}

export interface ManutencaoRequest {
  veiculoId: string;
  tipo: TipoManutencao;
  descricao: string;
  dataInicio: string;
}

export interface ConclusaoManutencaoRequest {
  custo: number;
  dataFim: string;
  detalhesAdicionais?: string;
}
