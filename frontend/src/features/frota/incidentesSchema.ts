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

export const multaSchema = z.object({
  data: z.string().min(1, "Informe a data."),
  infracao: z.string().min(1, "Informe a infração."),
  local: optionalTexto(),
  valor: z.coerce.number().gt(0, "Informe um valor maior que zero."),
  pontos: optionalNumero(),
  status: z.enum(["pendente", "paga", "recorrida", "cancelada"]),
  observacoes: optionalTexto(),
});
export type MultaFormInput = z.input<typeof multaSchema>;
export type MultaFormValues = z.output<typeof multaSchema>;

export const sinistroSchema = z.object({
  tipo: z.enum(["batida", "roubo", "furto", "enchente", "incendio"]),
  data: z.string().min(1, "Informe a data."),
  descricao: optionalTexto(),
  valor_prejuizo: optionalNumero(),
  seguradora_acionada: z.boolean(),
  status: z.enum(["aberto", "em_andamento", "finalizado"]),
});
export type SinistroFormInput = z.input<typeof sinistroSchema>;
export type SinistroFormValues = z.output<typeof sinistroSchema>;

export const danoSchema = z.object({
  tipo: z.enum(["arranhao", "amassado", "quebra_vidro", "dano_interno", "outro"]),
  descricao: optionalTexto(),
  data: z.string().min(1, "Informe a data."),
  valor_reparo: optionalNumero(),
  status: z.enum(["pendente", "reparado"]),
});
export type DanoFormInput = z.input<typeof danoSchema>;
export type DanoFormValues = z.output<typeof danoSchema>;
