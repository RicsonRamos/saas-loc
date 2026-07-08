import axios, { AxiosError } from "axios";

export interface ProblemDetails {
  type?: string;
  title: string;
  status: number;
  detail?: string;
  code?: string;
  errors?: { pointer: string; detail: string }[];
}

export const ACCESS_TOKEN_KEY = "locadora.access_token";

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1",
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ProblemDetails>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      if (window.location.pathname !== "/login") {
        window.location.assign("/login");
      }
    }
    return Promise.reject(error);
  }
);

export function extrairMensagemErro(error: unknown): string {
  if (axios.isAxiosError<ProblemDetails>(error)) {
    const problema = error.response?.data;
    if (problema?.errors?.length) {
      return problema.errors.map((e) => e.detail).join(" ");
    }
    if (problema?.detail) {
      return problema.detail;
    }
    if (problema?.title) {
      return problema.title;
    }
  }
  console.error(error);
  return "Ocorreu um erro inesperado. Tente novamente.";
}
