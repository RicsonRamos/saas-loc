import api from './api';
import { Cliente, ClienteRequest } from '../interfaces/cliente';

interface PagedResponse<T> {
  data: T[];
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}

interface ApiResponse<T> {
  data: T;
  message?: string;
}

export const clienteService = {
  listar: async (page = 0, size = 20): Promise<PagedResponse<Cliente>> => {
    const response = await api.get<PagedResponse<Cliente>>(`/clientes?page=${page}&size=${size}`);
    return response.data;
  },

  buscarPorId: async (id: string): Promise<Cliente> => {
    const response = await api.get<ApiResponse<Cliente>>(`/clientes/${id}`);
    return response.data.data;
  },

  criar: async (cliente: ClienteRequest): Promise<Cliente> => {
    const response = await api.post<ApiResponse<Cliente>>('/clientes', cliente);
    return response.data.data;
  },

  atualizar: async (id: string, cliente: ClienteRequest): Promise<Cliente> => {
    const response = await api.put<ApiResponse<Cliente>>(`/clientes/${id}`, cliente);
    return response.data.data;
  },

  excluir: async (id: string): Promise<void> => {
    await api.delete(`/clientes/${id}`);
  }
};
