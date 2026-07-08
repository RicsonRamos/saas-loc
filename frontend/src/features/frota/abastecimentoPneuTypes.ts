export interface Abastecimento {
  id: string;
  veiculo_id: string;
  contrato_id: string | null;
  data: string;
  posto: string | null;
  litros: string;
  valor: string;
  km: number;
  tipo_combustivel: string | null;
  valor_por_litro: string;
  created_at: string;
  updated_at: string;
}

export type PosicaoPneu =
  | "dianteiro_esquerdo"
  | "dianteiro_direito"
  | "traseiro_esquerdo"
  | "traseiro_direito"
  | "estepe";

export type StatusPneu = "ativo" | "trocado";

export interface Pneu {
  id: string;
  veiculo_id: string;
  marca: string;
  modelo: string | null;
  numero_serie: string | null;
  posicao: PosicaoPneu;
  data_instalacao: string;
  km_instalacao: number;
  vida_util_km: number | null;
  data_troca: string | null;
  km_troca: number | null;
  status: StatusPneu;
  created_at: string;
  updated_at: string;
}
