export type TipoPlanoManutencao =
  | "troca_oleo"
  | "troca_filtros"
  | "pastilhas_freio"
  | "pneus"
  | "revisao"
  | "alinhamento_balanceamento"
  | "licenciamento"
  | "seguro"
  | "outro";

export type PrioridadePlano = "normal" | "atencao" | "critico";

export interface PlanoManutencao {
  id: string;
  veiculo_id: string;
  tipo: TipoPlanoManutencao;
  descricao: string | null;
  intervalo_km: number | null;
  intervalo_dias: number | null;
  ultima_execucao_km: number | null;
  ultima_execucao_data: string | null;
  ativo: boolean;
  prioridade: PrioridadePlano;
  faltam_km: number | null;
  faltam_dias: number | null;
  created_at: string;
  updated_at: string;
}
