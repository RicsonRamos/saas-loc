import { z } from "zod";

export const clienteSchema = z.object({
  nome: z.string().min(1, "Informe o nome."),
  documento: z.string().min(11, "Informe um CPF/CNPJ válido.").max(20),
  email: z.string().email("E-mail inválido.").optional().or(z.literal("")),
  telefone: z.string().optional().or(z.literal("")),
});
export type ClienteFormValues = z.infer<typeof clienteSchema>;

export const motoristaSchema = z.object({
  nome: z.string().min(1, "Informe o nome."),
  cnh: z.string().min(5, "Informe a CNH.").max(20),
  validade_cnh: z.string().min(1, "Informe a validade da CNH."),
  telefone: z.string().optional().or(z.literal("")),
});
export type MotoristaFormValues = z.infer<typeof motoristaSchema>;
