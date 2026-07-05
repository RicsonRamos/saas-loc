import api from './api';
import { DashboardResponse } from '../interfaces/dashboard';

interface ApiResponse<T> {
  data: T;
  message?: string;
}

export const dashboardService = {
  obterResumoMensal: async (): Promise<DashboardResponse> => {
    const response = await api.get<ApiResponse<DashboardResponse>>('/dashboard/resumo-mensal');
    return response.data.data;
  }
};
