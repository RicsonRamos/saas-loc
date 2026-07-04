import { useState, useEffect, useCallback } from 'react';

interface User {
  email: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  login: (accessToken: string, refreshToken: string, email: string) => void;
  logout: () => void;
}

export function useAuth(): AuthState {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(() => {
    return !!localStorage.getItem('accessToken');
  });

  const [user, setUser] = useState<User | null>(() => {
    const email = localStorage.getItem('userEmail');
    return email ? { email } : null;
  });

  const login = useCallback((accessToken: string, refreshToken: string, email: string) => {
    localStorage.setItem('accessToken', accessToken);
    localStorage.setItem('refreshToken', refreshToken);
    localStorage.setItem('userEmail', email);
    setIsAuthenticated(true);
    setUser({ email });
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('userEmail');
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    const email = localStorage.getItem('userEmail');
    if (token && email) {
      setIsAuthenticated(true);
      setUser({ email });
    }
  }, []);

  return { isAuthenticated, user, login, logout };
}
