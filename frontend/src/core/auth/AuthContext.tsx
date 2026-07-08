import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";

import { ACCESS_TOKEN_KEY, apiClient } from "@/core/api/client";
import { temPermissao } from "@/core/auth/permissions";

export interface Usuario {
  id: string;
  nome: string;
  email: string;
  role: string;
  ativo: boolean;
}

interface AuthContextValue {
  usuario: Usuario | null;
  carregando: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  hasPermission: (permissao: string) => boolean;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(null);
  const [carregando, setCarregando] = useState(true);

  const carregarUsuario = useCallback(async () => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    if (!token) {
      setUsuario(null);
      setCarregando(false);
      return;
    }
    try {
      const { data } = await apiClient.get<Usuario>("/auth/me");
      setUsuario(data);
    } catch {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      setUsuario(null);
    } finally {
      setCarregando(false);
    }
  }, []);

  useEffect(() => {
    void carregarUsuario();
  }, [carregarUsuario]);

  const login = useCallback(async (email: string, password: string) => {
    const { data } = await apiClient.post<{ access_token: string }>("/auth/login", {
      email,
      password,
    });
    localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
    await carregarUsuario();
  }, [carregarUsuario]);

  const logout = useCallback(() => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setUsuario(null);
  }, []);

  const hasPermission = useCallback(
    (permissao: string) => temPermissao(usuario?.role, permissao),
    [usuario]
  );

  return (
    <AuthContext.Provider value={{ usuario, carregando, login, logout, hasPermission }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth deve ser usado dentro de um AuthProvider.");
  }
  return context;
}
