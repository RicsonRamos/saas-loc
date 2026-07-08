import { z } from "zod";

export const contratoSchema = z
  .object({
    cliente_id: z.string().min(1, "Selecione um cliente."),
    veiculo_id: z.string().min(1, "Selecione um veículo."),
    data_inicio: z.string().min(1, "Informe a data de início."),
    data_fim_prevista: z.string().min(1, "Informe a data de devolução prevista."),
    valor_diaria: z.coerce.number().gt(0, "Informe um valor de diária maior que zero."),
  })
  .refine((v) => new Date(v.data_fim_prevista) > new Date(v.data_inicio), {
    message: "A data de devolução prevista deve ser posterior à data de início.",
    path: ["data_fim_prevista"],
  });

export type ContratoFormInput = z.input<typeof contratoSchema>;
export type ContratoFormValues = z.output<typeof contratoSchema>;
