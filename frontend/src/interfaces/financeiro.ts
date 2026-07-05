export type TipoTransacao = 'RECEITA' | 'DESPESA';
export type StatusPagamento = 'PENDENTE' | 'PAGO' | 'CANCELADO';
export type CategoriaFinanceira = 'ALUGUEL' | 'CAUCAO' | 'MANUTENCAO' | 'COMBUSTIVEL' | 'IMPOSTOS_TAXAS' | 'SALARIOS' | 'OUTROS';

export interface LancamentoFinanceiro {
  id: string;
  tipo: TipoTransacao;
  valor: number;
  categoria: CategoriaFinanceira;
  descricao: string;
  status: StatusPagamento;
  dataVencimento: string;
  dataPagamento?: string;
  veiculoId?: string;
  veiculoPlaca?: string;
  contratoId?: string;
}

export interface LancamentoRequest {
  tipo: TipoTransacao;
  valor: number;
  categoria: CategoriaFinanceira;
  descricao: string;
  status: StatusPagamento;
  dataVencimento: string;
  dataPagamento?: string;
  veiculoId?: string;
  contratoId?: string;
}

export interface FluxoCaixaResponse {
  ano: number;
  mes: number;
  totalReceitas: number;
  totalDespesas: number;
  saldoLiquido: number;
}
