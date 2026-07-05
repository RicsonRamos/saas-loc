import api from './api';
import { LancamentoFinanceiro, LancamentoRequest, FluxoCaixaResponse } from '../interfaces/financeiro';

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

export const financeiroService = {
  listar: async (page = 0, size = 30): Promise<PagedResponse<LancamentoFinanceiro>> => {
    const response = await api.get<PagedResponse<LancamentoFinanceiro>>(`/financeiro/lancamentos?page=${page}&size=${size}`);
    return response.data;
  },

  criar: async (lancamento: LancamentoRequest): Promise<LancamentoFinanceiro> => {
    const response = await api.post<ApiResponse<LancamentoFinanceiro>>('/financeiro/lancamentos', lancamento);
    return response.data.data;
  },

  obterFluxoMensal: async (ano?: number, mes?: number): Promise<FluxoCaixaResponse> => {
    let url = '/financeiro/fluxo-caixa';
    if (ano && mes) {
      url += `?ano=${ano}&mes=${mes}`;
    }
    const response = await api.get<ApiResponse<FluxoCaixaResponse>>(url);
    return response.data.data;
  }
};
