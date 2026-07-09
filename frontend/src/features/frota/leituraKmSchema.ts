import { z } from "zod";

export const leituraKmSchema = z.object({
  data_leitura: z.string().min(1, "Informe a data da leitura."),
  km: z.coerce.number().min(0, "Informe uma quilometragem válida."),
  observacao: z
    .string()
    .optional()
    .or(z.literal(""))
    .transform((v) => (v ? v : undefined)),
});

export type LeituraKmFormInput = z.input<typeof leituraKmSchema>;
export type LeituraKmFormValues = z.output<typeof leituraKmSchema>;
