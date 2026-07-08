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

  versao: optionalTexto(),
  ano_fabricacao: optionalNumero(),
  portas: optionalNumero(),
  capacidade_passageiros: optionalNumero(),
  motor: optionalTexto(),
  potencia: optionalTexto(),

  data_aquisicao: optionalTexto(),
  valor_compra: optionalNumero(),
  fornecedor: optionalTexto(),
  forma_aquisicao: optionalTexto(),
  km_inicial: optionalNumero(),
  proprietario: optionalTexto(),
  data_entrada_frota: optionalTexto(),
  garantia_fabrica_ate: optionalTexto(),
  garantia_concessionaria_ate: optionalTexto(),

  crlv_numero: optionalTexto(),
  ipva_vencimento: optionalTexto(),
  alienado: z.boolean(),
  alienante: optionalTexto(),

  seguradora: optionalTexto(),
  apolice_numero: optionalTexto(),
  seguro_franquia: optionalNumero(),
  seguro_cobertura: optionalTexto(),
  seguro_contato: optionalTexto(),
});

export type VeiculoFormInput = z.input<typeof veiculoSchema>;
export type VeiculoFormValues = z.output<typeof veiculoSchema>;
