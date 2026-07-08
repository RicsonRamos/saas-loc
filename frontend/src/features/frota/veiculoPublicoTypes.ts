export interface LocacaoPublica {
  em_uso: boolean;
  data_fim_prevista: string | null;
}

export interface VeiculoPublico {
  placa: string;
  modelo: string;
  marca: string | null;
  ano: number;
  status: string;
  km_atual: number;
  locacao_atual: LocacaoPublica | null;
}
