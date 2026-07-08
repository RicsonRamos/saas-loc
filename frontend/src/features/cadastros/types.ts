export type StatusCliente = "ativo" | "bloqueado" | "inadimplente" | "em_analise" | "inativo";

export interface Cliente {
  id: string;
  nome: string;
  documento: string;
  rg: string | null;
  rg_orgao_emissor: string | null;
  data_nascimento: string | null;

  email: string | null;
  telefone: string | null;
  celular_secundario: string | null;
  whatsapp: string | null;

  cep: string | null;
  logradouro: string | null;
  numero: string | null;
  complemento: string | null;
  bairro: string | null;
  cidade: string | null;
  estado: string | null;

  cnh_numero: string | null;
  cnh_categoria: string | null;
  cnh_emissao: string | null;
  cnh_vencimento: string | null;
  cnh_orgao_emissor: string | null;
  cnh_primeira_habilitacao: string | null;
  cnh_ear: boolean;

  limite_credito: string | null;
  forma_pagamento_preferida: string | null;
  banco: string | null;
  agencia: string | null;
  conta: string | null;
  pix: string | null;
  caucao_padrao: string | null;

  contato_emergencia_nome: string | null;
  contato_emergencia_parentesco: string | null;
  contato_emergencia_telefone: string | null;
  contato_emergencia_whatsapp: string | null;

  status: StatusCliente;
  observacoes: string | null;
  created_at: string;
  updated_at: string;
}
