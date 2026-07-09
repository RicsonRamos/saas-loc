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

export const planoManutencaoSchema = z
  .object({
    tipo: z.enum([
      "troca_oleo",
      "troca_filtros",
      "pastilhas_freio",
      "pneus",
      "revisao",
      "alinhamento_balanceamento",
      "licenciamento",
      "seguro",
      "outro",
    ]),
    descricao: optionalTexto(),
    intervalo_km: optionalNumero(),
    intervalo_dias: optionalNumero(),
    ultima_execucao_km: optionalNumero(),
    ultima_execucao_data: optionalTexto(),
  })
  .refine((v) => v.intervalo_km !== undefined || v.intervalo_dias !== undefined, {
    message: "Informe ao menos um intervalo (km ou dias).",
    path: ["intervalo_km"],
  });

export type PlanoManutencaoFormInput = z.input<typeof planoManutencaoSchema>;
export type PlanoManutencaoFormValues = z.output<typeof planoManutencaoSchema>;
