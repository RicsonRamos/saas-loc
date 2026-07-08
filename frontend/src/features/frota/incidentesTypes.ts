export type StatusMulta = "pendente" | "paga" | "recorrida" | "cancelada";

export interface Multa {
  id: string;
  veiculo_id: string;
  cliente_id: string | null;
  contrato_id: string | null;
  data: string;
  infracao: string;
  local: string | null;
  valor: string;
  pontos: number | null;
  status: StatusMulta;
  observacoes: string | null;
  created_at: string;
  updated_at: string;
}

export type TipoSinistro = "batida" | "roubo" | "furto" | "enchente" | "incendio";
export type StatusSinistro = "aberto" | "em_andamento" | "finalizado";

export interface Sinistro {
  id: string;
  veiculo_id: string;
  cliente_id: string | null;
  contrato_id: string | null;
  tipo: TipoSinistro;
  data: string;
  descricao: string | null;
  valor_prejuizo: string | null;
  seguradora_acionada: boolean;
  status: StatusSinistro;
  created_at: string;
  updated_at: string;
}

export type TipoDano = "arranhao" | "amassado" | "quebra_vidro" | "dano_interno" | "outro";
export type StatusDano = "pendente" | "reparado";

export interface Dano {
  id: string;
  veiculo_id: string;
  cliente_id: string | null;
  contrato_id: string | null;
  tipo: TipoDano;
  descricao: string | null;
  data: string;
  valor_reparo: string | null;
  status: StatusDano;
  created_at: string;
  updated_at: string;
}
