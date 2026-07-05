import api from './api';
import { Manutencao, ManutencaoRequest, ConclusaoManutencaoRequest } from '../interfaces/manutencao';

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

export const manutencaoService = {
  listar: async (page = 0, size = 20): Promise<PagedResponse<Manutencao>> => {
    const response = await api.get<PagedResponse<Manutencao>>(`/manutencoes?page=${page}&size=${size}`);
    return response.data;
  },

  listarPorVeiculo: async (veiculoId: string, page = 0, size = 20): Promise<PagedResponse<Manutencao>> => {
    const response = await api.get<PagedResponse<Manutencao>>(`/manutencoes/veiculo/${veiculoId}?page=${page}&size=${size}`);
    return response.data;
  },

  iniciar: async (request: ManutencaoRequest): Promise<Manutencao> => {
    const response = await api.post<ApiResponse<Manutencao>>('/manutencoes', request);
    return response.data.data;
  },

  concluir: async (id: string, request: ConclusaoManutencaoRequest): Promise<Manutencao> => {
    const response = await api.put<ApiResponse<Manutencao>>(`/manutencoes/${id}/concluir`, request);
    return response.data.data;
  }
};
