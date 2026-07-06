import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { dashboardService } from '../services/dashboardService';
import { DashboardResponse } from '../interfaces/dashboard';

export default function Dashboard() {
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadData() {
      try {
        const res = await dashboardService.obterResumoMensal();
        setData(res);
      } catch (err) {
        setError('Erro ao carregar os dados do dashboard.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div style={{ color: 'var(--text-muted)' }}>Carregando métricas...</div>;
  if (error) return <div style={{ color: 'var(--error)' }}>{error}</div>;
  if (!data) return null;

  return (
    <div>
      <h1 style={{ fontSize: '2rem', marginBottom: '24px', fontWeight: 700 }}>Dashboard</h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginBottom: '32px' }}>
        <Card title="Ocupação da Frota" className="glass-card">
          <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--primary-light)' }}>
            {(data.ocupacaoFrota.taxaOcupacao * 100).toFixed(1)}%
          </div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>
            {data.ocupacaoFrota.veiculosLocados} de {data.ocupacaoFrota.totalVeiculos} veículos locados
          </div>
        </Card>

        <Card title="Balanço Mensal" className="glass-card">
          <div style={{ fontSize: '2.5rem', fontWeight: 700, color: data.balancoMensal.saldoLiquido >= 0 ? 'var(--success)' : 'var(--error)' }}>
            R$ {data.balancoMensal.saldoLiquido.toFixed(2)}
          </div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '8px' }}>
            Receitas: R$ {data.balancoMensal.totalReceitas.toFixed(2)} | Despesas: R$ {data.balancoMensal.totalDespesas.toFixed(2)}
          </div>
        </Card>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        <Card title="Top Veículos Rentáveis" className="glass-card">
          {data.topVeiculosRentaveis.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>Sem dados suficientes.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {data.topVeiculosRentaveis.map((v) => (
                <li key={v.veiculoId} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border-color)' }}>
                  <span>{v.modelo} ({v.placa})</span>
                  <span style={{ color: 'var(--success)', fontWeight: 600 }}>R$ {v.saldoLiquido.toFixed(2)}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>

        <Card title="Veículos em Prejuízo" className="glass-card">
          {data.topVeiculosPrejuizo.length === 0 ? (
            <p style={{ color: 'var(--text-muted)' }}>Sem veículos em prejuízo.</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {data.topVeiculosPrejuizo.map((v) => (
                <li key={v.veiculoId} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border-color)' }}>
                  <span>{v.modelo} ({v.placa})</span>
                  <span style={{ color: 'var(--error)', fontWeight: 600 }}>R$ {v.saldoLiquido.toFixed(2)}</span>
                </li>
              ))}
            </ul>
          )}
        </Card>
      </div>
    </div>
  );
}
