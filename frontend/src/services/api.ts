import axios from 'axios';
import { supabase } from './supabaseClient';

const API_URL = import.meta.env.VITE_API_URL || '/api/v1';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar Bearer Token do Supabase automaticamente
api.interceptors.request.use(
  async (config) => {
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
      config.headers.Authorization = `Bearer ${session.access_token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor para tratar erros de Auth e Rate Limit
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status;

    if (status === 401) {
      // O Supabase gerencia o refresh automaticamente no client.
      // Se deu 401 do backend, provavelmente a sessão expirou ou o token é inválido.
      await supabase.auth.signOut();
      window.location.href = '/login';
    } else if (status === 429) {
      alert('Muitas requisições (Rate Limit). Por favor, aguarde um instante antes de tentar novamente.');
    } else if (status === 403) {
      alert('Você não tem permissão para acessar este recurso.');
    }

    return Promise.reject(error);
  }
);

export default api;
