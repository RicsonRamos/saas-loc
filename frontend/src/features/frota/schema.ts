import { z } from "zod";

const optionalTexto = () =>
  z
    .string()
    .optional()
    .or(z.literal(""))
    .transform((v) => (v ? v : undefined));

export const veiculoSchema = z.object({
  placa: z.string().min(7, "Informe a placa completa.").max(10),
  modelo: z.string().min(1, "Informe o modelo."),
  ano: z.coerce.number().min(1950).max(2100),
  km_atual: z.coerce.number().min(0),
  marca: optionalTexto(),
  cor: optionalTexto(),
  categoria: optionalTexto(),
  chassi: optionalTexto(),
  renavam: optionalTexto(),
  combustivel: optionalTexto(),
  cambio: optionalTexto(),
  vencimento_licenciamento: optionalTexto(),
  vencimento_seguro: optionalTexto(),
  status: optionalTexto(),
});

export type VeiculoFormInput = z.input<typeof veiculoSchema>;
export type VeiculoFormValues = z.output<typeof veiculoSchema>;
