export type StatusPagamento = "pendente" | "pago" | "estornado";

export interface Pagamento {
  id: string;
  contrato_id: string;
  valor: string;
  data: string;
  status: StatusPagamento;
  metodo: string | null;
  created_at: string;
}

export interface Despesa {
  id: string;
  veiculo_id: string | null;
  categoria: string;
  valor: string;
  data: string;
  descricao: string | null;
  created_at: string;
}

export interface RentabilidadeVeiculo {
  veiculo_id: string;
  placa: string;
  receita_total: string;
  despesa_total: string;
  resultado: string;
}
