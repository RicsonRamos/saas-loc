import { z } from "zod";

export const pagamentoSchema = z.object({
  contrato_id: z.string().min(1, "Selecione um contrato."),
  valor: z.coerce.number().gt(0, "Informe um valor maior que zero."),
  data: z.string().min(1, "Informe a data."),
  metodo: z.string().optional().or(z.literal("")),
});
export type PagamentoFormInput = z.input<typeof pagamentoSchema>;
export type PagamentoFormValues = z.output<typeof pagamentoSchema>;

export const despesaSchema = z.object({
  veiculo_id: z.string().optional().or(z.literal("")),
  categoria: z.string().min(1, "Informe a categoria."),
  valor: z.coerce.number().gt(0, "Informe um valor maior que zero."),
  data: z.string().min(1, "Informe a data."),
  descricao: z.string().optional().or(z.literal("")),
});
export type DespesaFormInput = z.input<typeof despesaSchema>;
export type DespesaFormValues = z.output<typeof despesaSchema>;
