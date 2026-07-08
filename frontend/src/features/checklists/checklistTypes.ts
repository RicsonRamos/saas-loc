export type TipoChecklist = "entrega" | "devolucao";
export type SituacaoItemChecklist = "ok" | "avaria" | "faltante";
export type ItemChecklist =
  | "lataria"
  | "pneus"
  | "combustivel"
  | "km"
  | "documentos"
  | "acessorios";

export interface ChecklistItemOut {
  id: string;
  item: ItemChecklist;
  situacao: SituacaoItemChecklist;
  observacao: string | null;
  foto_attachment_id: string | null;
}

export interface Checklist {
  id: string;
  contrato_id: string;
  tipo: TipoChecklist;
  data: string;
  usuario_id: string;
  km: number;
  combustivel: string | null;
  observacoes_gerais: string | null;
  status: string;
  itens: ChecklistItemOut[];
}

export interface ItemComparacao {
  item: string;
  situacao_entrega: SituacaoItemChecklist | null;
  situacao_devolucao: SituacaoItemChecklist | null;
  mudou: boolean;
}

export interface ChecklistComparacao {
  checklist_entrega_id: string;
  checklist_devolucao_id: string;
  itens: ItemComparacao[];
}
