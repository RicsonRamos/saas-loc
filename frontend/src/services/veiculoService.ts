import api from './api';
import { Veiculo, VeiculoRequest } from '../interfaces/veiculo';

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

export const veiculoService = {
  listar: async (page = 0, size = 20): Promise<PagedResponse<Veiculo>> => {
    const response = await api.get<PagedResponse<Veiculo>>(`/veiculos?page=${page}&size=${size}`);
    return response.data;
  },

  buscarPorId: async (id: string): Promise<Veiculo> => {
    const response = await api.get<ApiResponse<Veiculo>>(`/veiculos/${id}`);
    return response.data.data;
  },

  criar: async (veiculo: VeiculoRequest): Promise<Veiculo> => {
    const response = await api.post<ApiResponse<Veiculo>>('/veiculos', veiculo);
    return response.data.data;
  },

  atualizar: async (id: string, veiculo: VeiculoRequest): Promise<Veiculo> => {
    const response = await api.put<ApiResponse<Veiculo>>(`/veiculos/${id}`, veiculo);
    return response.data.data;
  },

  excluir: async (id: string): Promise<void> => {
    await api.delete(`/veiculos/${id}`);
  }
};
