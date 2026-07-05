import api from './api';
import { Contrato, ContratoRequest, EncerramentoContratoRequest } from '../interfaces/contrato';

/**
 * Padrão de paginação do Spring.
 */
interface PagedResponse<T> {
  data: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}

/**
 * Padrão de resposta envoltória da API.
 */
interface ApiResponse<T> {
  data: T;
  message?: string;
}

/**
 * Serviço responsável pelas chamadas HTTP referentes a contratos e locações.
 */
export const contratoService = {
  
  /**
   * Lista todos os contratos vigentes e históricos com paginação.
   */
  listar: async (page = 0, size = 20): Promise<PagedResponse<Contrato>> => {
    const response = await api.get<PagedResponse<Contrato>>(`/contratos?page=${page}&size=${size}`);
    return response.data;
  },

  /**
   * Busca um contrato específico pelo seu UUID.
   */
  buscarPorId: async (id: string): Promise<Contrato> => {
    const response = await api.get<ApiResponse<Contrato>>(`/contratos/${id}`);
    return response.data.data;
  },

  /**
   * Inicia a locação, gerando um novo contrato e bloqueando o veículo (Status LOCADO).
   */
  criar: async (contrato: ContratoRequest): Promise<Contrato> => {
    const response = await api.post<ApiResponse<Contrato>>('/contratos', contrato);
    return response.data.data;
  },

  /**
   * Efetua a devolução do veículo (Checkout), liberando o carro pro pátio e validando o KM final.
   */
  encerrar: async (id: string, payload: EncerramentoContratoRequest): Promise<Contrato> => {
    const response = await api.put<ApiResponse<Contrato>>(`/contratos/${id}/encerrar`, payload);
    return response.data.data;
  }
};
