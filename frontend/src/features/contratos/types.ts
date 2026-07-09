export type StatusContrato = "reservado" | "ativo" | "encerrado" | "cancelado";

export interface ConsumoKm {
  km_previsto: number;
  km_percorrido: number;
  percentual: number | null;
  nivel: "normal" | "atencao" | "critico";
}

export interface Contrato {
  id: string;
  cliente_id: string;
  veiculo_id: string;
  data_inicio: string;
  data_fim_prevista: string;
  data_fim_real: string | null;
  status: StatusContrato;
  valor_diaria: string;
  km_inicio: number | null;
  km_final: number | null;
  km_contratado_mensal: number | null;
  consumo_km: ConsumoKm | null;
  version: number;
  created_at: string;
  updated_at: string;
}
