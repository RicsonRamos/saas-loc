export interface AuditLog {
  id: string;
  usuario_id: string | null;
  acao: string;
  entidade: string;
  entidade_id: string;
  dados_anteriores: Record<string, unknown> | null;
  dados_novos: Record<string, unknown> | null;
  data_hora: string;
  ip: string | null;
  descricao: string | null;
}
