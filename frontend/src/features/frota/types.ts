export type StatusVeiculo =
  | "disponivel"
  | "alugado"
  | "reservado"
  | "em_manutencao"
  | "sinistrado"
  | "em_limpeza"
  | "licenciamento_vencido"
  | "seguro_vencido"
  | "inativo";

export interface Veiculo {
  id: string;
  placa: string;
  codigo_publico: string;
  modelo: string;
  ano: number;
  status: StatusVeiculo;
  km_atual: number;
  filial_id: string | null;
  marca: string | null;
  cor: string | null;
  categoria: string | null;
  chassi: string | null;
  renavam: string | null;
  combustivel: string | null;
  cambio: string | null;
  vencimento_licenciamento: string | null;
  vencimento_seguro: string | null;

  versao: string | null;
  ano_fabricacao: number | null;
  portas: number | null;
  capacidade_passageiros: number | null;
  motor: string | null;
  potencia: string | null;

  data_aquisicao: string | null;
  valor_compra: string | null;
  fornecedor: string | null;
  forma_aquisicao: string | null;
  km_inicial: number | null;
  proprietario: string | null;
  data_entrada_frota: string | null;
  garantia_fabrica_ate: string | null;
  garantia_concessionaria_ate: string | null;

  crlv_numero: string | null;
  ipva_vencimento: string | null;
  alienado: boolean;
  alienante: string | null;

  seguradora: string | null;
  apolice_numero: string | null;
  seguro_franquia: string | null;
  seguro_cobertura: string | null;
  seguro_contato: string | null;

  created_at: string;
  updated_at: string;
}
