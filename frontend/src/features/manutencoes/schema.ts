import { z } from "zod";

export const manutencaoSchema = z.object({
  veiculo_id: z.string().min(1, "Selecione um veículo."),
  tipo: z.enum(["preventiva", "corretiva"]),
  data: z.string().min(1, "Informe a data."),
  km: z.coerce.number().min(0),
  custo: z.coerce.number().min(0),
  oficina: z.string().optional().or(z.literal("")),
  descricao: z.string().optional().or(z.literal("")),
  em_andamento: z.boolean(),
});

export type ManutencaoFormInput = z.input<typeof manutencaoSchema>;
export type ManutencaoFormValues = z.output<typeof manutencaoSchema>;
