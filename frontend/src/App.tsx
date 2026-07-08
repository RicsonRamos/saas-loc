import { Navigate, Route, BrowserRouter, Routes } from "react-router-dom";

import { ClienteHistoricoPage } from "@/features/cadastros/ClienteHistoricoPage";
import { ClientesPage } from "@/features/cadastros/ClientesPage";
import { ContratosPage } from "@/features/contratos/ContratosPage";
import { DashboardPage } from "@/features/dashboard/DashboardPage";
import { FinanceiroPage } from "@/features/financeiro/FinanceiroPage";
import { LoginPage } from "@/features/auth/LoginPage";
import { VeiculoHistoricoPage } from "@/features/frota/VeiculoHistoricoPage";
import { VeiculoPublicoPage } from "@/features/frota/VeiculoPublicoPage";
import { VeiculosPage } from "@/features/frota/VeiculosPage";
import { ManutencoesPage } from "@/features/manutencoes/ManutencoesPage";
import { ProtectedRoute } from "@/routes/ProtectedRoute";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/veiculo/public/:codigo" element={<VeiculoPublicoPage />} />

        <Route element={<ProtectedRoute />}>
          <Route index element={<DashboardPage />} />
          <Route path="/frota" element={<VeiculosPage />} />
          <Route path="/frota/:id" element={<VeiculoHistoricoPage />} />
          <Route path="/clientes" element={<ClientesPage />} />
          <Route path="/clientes/:id" element={<ClienteHistoricoPage />} />
          <Route path="/contratos" element={<ContratosPage />} />
          <Route path="/manutencoes" element={<ManutencoesPage />} />
          <Route path="/financeiro" element={<FinanceiroPage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
