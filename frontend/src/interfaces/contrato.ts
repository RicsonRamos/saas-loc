export type StatusContrato = 'RASCUNHO' | 'ATIVO' | 'ENCERRADO' | 'CANCELADO' | 'INADIMPLENTE';

/**
 * Interface que representa a visualização (Response) de um contrato.
 */
export interface Contrato {
  id: string;
  clienteId: string;
  clienteNome: string;
  veiculoId: string;
  veiculoPlaca: string;
  status: StatusContrato;
  dataInicio: string;
  dataFimPrevista: string;
  dataDevolucao?: string;
  valorTotal: number;
  caucao?: number;
  valorAdicional?: number;
  kmInicial: number;
  kmFinal?: number;
  kmExcedente: number;
}

/**
 * Payload utilizado na criação de uma locação.
 */
export interface ContratoRequest {
  clienteId: string;
  veiculoId: string;
  dataInicio: string;
  dataFimPrevista: string;
  valorTotal: number;
  caucao?: number;
}

/**
 * Payload utilizado ao encerrar o contrato e devolver a chave.
 */
export interface EncerramentoContratoRequest {
  kmFinal: number;
  dataDevolucao: string;
  valorAdicional?: number;
}
