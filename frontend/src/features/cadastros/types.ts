export interface Cliente {
  id: string;
  nome: string;
  documento: string;
  email: string | null;
  telefone: string | null;
  endereco: string | null;
}

export interface Motorista {
  id: string;
  nome: string;
  cnh: string;
  validade_cnh: string;
  telefone: string | null;
}
