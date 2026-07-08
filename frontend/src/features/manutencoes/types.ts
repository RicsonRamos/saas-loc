export type TipoManutencao = "preventiva" | "corretiva";

export interface Manutencao {
  id: string;
  veiculo_id: string;
  tipo: TipoManutencao;
  data: string;
  km: number;
  custo: string;
  oficina: string | null;
  descricao: string | null;
  proxima_manutencao_km: number | null;
  proxima_manutencao_data: string | null;
  created_at: string;
}
