export type TipoCliente = 'PESSOA_FISICA' | 'PESSOA_JURIDICA';

export interface Cliente {
  id: string;
  nome: string;
  tipo: TipoCliente;
  documento: string;
  email?: string;
  telefone?: string;
  cnh?: string;
  cnhValidade?: string;
  
  cep?: string;
  logradouro?: string;
  numero?: string;
  complemento?: string;
  bairro?: string;
  cidade?: string;
  uf?: string;

  cnhUrl?: string;
  comprovanteResidenciaUrl?: string;
}

export interface ClienteRequest extends Omit<Cliente, 'id'> {}
