export type StatusContrato = "reservado" | "ativo" | "encerrado" | "cancelado";

export interface Contrato {
  id: string;
  cliente_id: string;
  veiculo_id: string;
  motorista_id: string | null;
  data_inicio: string;
  data_fim_prevista: string;
  data_fim_real: string | null;
  status: StatusContrato;
  valor_diaria: string;
  version: number;
  created_at: string;
  updated_at: string;
}
