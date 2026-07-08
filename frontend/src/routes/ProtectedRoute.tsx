import { Navigate } from "react-router-dom";

import { useAuth } from "@/core/auth/AuthContext";
import { LoadingState } from "@/components/ui/States";
import { Layout } from "@/components/shared/Layout";

export function ProtectedRoute() {
  const { usuario, carregando } = useAuth();

  if (carregando) {
    return <LoadingState />;
  }

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  return <Layout />;
}
