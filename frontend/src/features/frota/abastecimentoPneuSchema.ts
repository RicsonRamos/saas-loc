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

export const abastecimentoSchema = z.object({
  data: z.string().min(1, "Informe a data."),
  posto: optionalTexto(),
  litros: z.coerce.number().gt(0, "Informe os litros abastecidos."),
  valor: z.coerce.number().gt(0, "Informe um valor maior que zero."),
  km: z.coerce.number().min(0),
  tipo_combustivel: optionalTexto(),
});
export type AbastecimentoFormInput = z.input<typeof abastecimentoSchema>;
export type AbastecimentoFormValues = z.output<typeof abastecimentoSchema>;

export const pneuSchema = z.object({
  marca: z.string().min(1, "Informe a marca."),
  modelo: optionalTexto(),
  numero_serie: optionalTexto(),
  posicao: z.enum([
    "dianteiro_esquerdo",
    "dianteiro_direito",
    "traseiro_esquerdo",
    "traseiro_direito",
    "estepe",
  ]),
  data_instalacao: z.string().min(1, "Informe a data de instalação."),
  km_instalacao: z.coerce.number().min(0),
  vida_util_km: optionalNumero(),
  data_troca: optionalTexto(),
  km_troca: optionalNumero(),
  status: z.enum(["ativo", "trocado"]),
});
export type PneuFormInput = z.input<typeof pneuSchema>;
export type PneuFormValues = z.output<typeof pneuSchema>;
