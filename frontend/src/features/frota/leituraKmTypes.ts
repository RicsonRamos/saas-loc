export interface LeituraKm {
  id: string;
  veiculo_id: string;
  usuario_id: string;
  km: number;
  data_leitura: string;
  observacao: string | null;
  created_at: string;
}
