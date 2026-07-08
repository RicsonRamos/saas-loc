export type StatusVeiculo = "disponivel" | "alugado" | "em_manutencao" | "baixado";

export interface Veiculo {
  id: string;
  placa: string;
  modelo: string;
  ano: number;
  status: StatusVeiculo;
  km_atual: number;
  filial_id: string | null;
  marca: string | null;
  cor: string | null;
  categoria: string | null;
  chassi: string | null;
  renavam: string | null;
  combustivel: string | null;
  cambio: string | null;
  vencimento_licenciamento: string | null;
  vencimento_seguro: string | null;
  created_at: string;
  updated_at: string;
}
