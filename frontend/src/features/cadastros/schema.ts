import { z } from "zod";

const optionalTexto = () =>
  z
    .string()
    .optional()
    .or(z.literal(""))
    .transform((v) => (v ? v : undefined));

const optionalNumero = () =>
  z
    .string()
    .optional()
    .or(z.literal(""))
    .transform((v) => (v ? Number(v) : undefined));

export const clienteSchema = z.object({
  nome: z.string().min(1, "Informe o nome."),
  documento: z.string().min(11, "Informe um CPF/CNPJ válido.").max(20),
  rg: optionalTexto(),
  rg_orgao_emissor: optionalTexto(),
  data_nascimento: optionalTexto(),

  email: z.string().email("E-mail inválido.").optional().or(z.literal("")),
  telefone: optionalTexto(),
  celular_secundario: optionalTexto(),
  whatsapp: optionalTexto(),

  cep: optionalTexto(),
  logradouro: optionalTexto(),
  numero: optionalTexto(),
  complemento: optionalTexto(),
  bairro: optionalTexto(),
  cidade: optionalTexto(),
  estado: optionalTexto(),

  cnh_numero: optionalTexto(),
  cnh_categoria: optionalTexto(),
  cnh_emissao: optionalTexto(),
  cnh_vencimento: optionalTexto(),
  cnh_orgao_emissor: optionalTexto(),
  cnh_primeira_habilitacao: optionalTexto(),
  cnh_ear: z.boolean(),

  limite_credito: optionalNumero(),
  forma_pagamento_preferida: optionalTexto(),
  banco: optionalTexto(),
  agencia: optionalTexto(),
  conta: optionalTexto(),
  pix: optionalTexto(),
  caucao_padrao: optionalNumero(),

  contato_emergencia_nome: optionalTexto(),
  contato_emergencia_parentesco: optionalTexto(),
  contato_emergencia_telefone: optionalTexto(),
  contato_emergencia_whatsapp: optionalTexto(),

  status: optionalTexto(),
  observacoes: optionalTexto(),
});
export type ClienteFormInput = z.input<typeof clienteSchema>;
export type ClienteFormValues = z.output<typeof clienteSchema>;

export const motoristaSchema = z.object({
  nome: z.string().min(1, "Informe o nome."),
  cnh: z.string().min(5, "Informe a CNH.").max(20),
  validade_cnh: z.string().min(1, "Informe a validade da CNH."),
  telefone: z.string().optional().or(z.literal("")),
});
export type MotoristaFormValues = z.infer<typeof motoristaSchema>;

export const condutorSchema = z.object({
  nome: z.string().min(1, "Informe o nome."),
  cnh: z.string().min(5, "Informe a CNH.").max(20),
  validade_cnh: z.string().min(1, "Informe a validade da CNH."),
  telefone: optionalTexto(),
  parentesco: optionalTexto(),
});
export type CondutorFormInput = z.input<typeof condutorSchema>;
export type CondutorFormValues = z.output<typeof condutorSchema>;
