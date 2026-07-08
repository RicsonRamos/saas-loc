export type StatusVeiculo = "disponivel" | "alugado" | "em_manutencao" | "baixado";

export interface Veiculo {
  id: string;
  placa: string;
  modelo: string;
  ano: number;
  status: StatusVeiculo;
  km_atual: number;
  filial_id: string | null;
  created_at: string;
  updated_at: string;
}
