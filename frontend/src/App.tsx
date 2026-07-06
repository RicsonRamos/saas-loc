import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Frota from './pages/Frota';
import Contratos from './pages/Contratos';
import Financeiro from './pages/Financeiro';
import { MainLayout } from './components/layout/MainLayout';
import { useAuth, AuthProvider } from './hooks/useAuth';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          {/* Protected Routes */}
          <Route path="/" element={<ProtectedRoute><MainLayout><Dashboard /></MainLayout></ProtectedRoute>} />
          <Route path="/clientes" element={<ProtectedRoute><MainLayout><Clientes /></MainLayout></ProtectedRoute>} />
          <Route path="/frota" element={<ProtectedRoute><MainLayout><Frota /></MainLayout></ProtectedRoute>} />
          <Route path="/contratos" element={<ProtectedRoute><MainLayout><Contratos /></MainLayout></ProtectedRoute>} />
          <Route path="/financeiro" element={<ProtectedRoute><MainLayout><Financeiro /></MainLayout></ProtectedRoute>} />
          
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>Verificando sessão...</div>;
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>;
}

export default App;
