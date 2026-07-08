import { Navigate, Route, BrowserRouter, Routes } from "react-router-dom";

import { ClientesPage } from "@/features/cadastros/ClientesPage";
import { MotoristasPage } from "@/features/cadastros/MotoristasPage";
import { ContratosPage } from "@/features/contratos/ContratosPage";
import { FinanceiroPage } from "@/features/financeiro/FinanceiroPage";
import { LoginPage } from "@/features/auth/LoginPage";
import { VeiculosPage } from "@/features/frota/VeiculosPage";
import { ManutencoesPage } from "@/features/manutencoes/ManutencoesPage";
import { ProtectedRoute } from "@/routes/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route element={<ProtectedRoute />}>
          <Route index element={<Navigate to="/frota" replace />} />
          <Route path="/frota" element={<VeiculosPage />} />
          <Route path="/clientes" element={<ClientesPage />} />
          <Route path="/motoristas" element={<MotoristasPage />} />
          <Route path="/contratos" element={<ContratosPage />} />
          <Route path="/manutencoes" element={<ManutencoesPage />} />
          <Route path="/financeiro" element={<FinanceiroPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/frota" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
