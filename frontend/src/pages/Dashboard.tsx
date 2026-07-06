import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { dashboardService } from '../services/dashboardService';
import { DashboardResponse } from '../interfaces/dashboard';
import { LayoutDashboard, TrendingUp, TrendingDown, Car } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Cell } from 'recharts';

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

  const chartData = [
    { name: 'Disponíveis', valor: data.ocupacaoFrota.veiculosDisponiveis, color: '#34d399' },
    { name: 'Locados', valor: data.ocupacaoFrota.veiculosLocados, color: '#818cf8' },
    { name: 'Manutenção', valor: data.ocupacaoFrota.veiculosEmManutencao, color: '#fbbf24' }
  ];

  return (
    <div>
      <h1 style={{ fontSize: '2rem', marginBottom: '24px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '12px' }}>
        <LayoutDashboard size={32} color="var(--primary-light)" />
        Dashboard
      </h1>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px', marginBottom: '32px' }}>
        
        <Card title="Ocupação da Frota" className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '16px', background: 'rgba(99, 102, 241, 0.1)', borderRadius: '12px' }}>
              <Car size={32} color="var(--primary-light)" />
            </div>
            <div>
              <div style={{ fontSize: '2.5rem', fontWeight: 700, color: 'var(--primary-light)' }}>
                {(data.ocupacaoFrota.taxaOcupacao * 100).toFixed(1)}%
              </div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                {data.ocupacaoFrota.veiculosLocados} de {data.ocupacaoFrota.totalVeiculos} locados
              </div>
            </div>
          </div>
        </Card>

        <Card title="Balanço Mensal" className="glass-card">
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '16px', background: data.balancoMensal.saldoLiquido >= 0 ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)', borderRadius: '12px' }}>
              {data.balancoMensal.saldoLiquido >= 0 ? <TrendingUp size={32} color="var(--success)" /> : <TrendingDown size={32} color="var(--error)" />}
            </div>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: data.balancoMensal.saldoLiquido >= 0 ? 'var(--success)' : 'var(--error)' }}>
                R$ {data.balancoMensal.saldoLiquido.toFixed(2)}
              </div>
              <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                Entradas: R$ {data.balancoMensal.totalReceitas.toFixed(2)}<br/>
                Saídas: R$ {data.balancoMensal.totalDespesas.toFixed(2)}
              </div>
            </div>
          </div>
        </Card>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        
        <Card title="Status da Frota" className="glass-card">
          <div style={{ height: '300px', width: '100%', marginTop: '16px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                <XAxis dataKey="name" stroke="var(--text-muted)" />
                <YAxis stroke="var(--text-muted)" allowDecimals={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: 'var(--bg-app)', border: '1px solid var(--border-color)', borderRadius: '8px' }}
                  itemStyle={{ color: 'var(--text-main)' }}
                />
                <Bar dataKey="valor" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <Card title="Top Veículos Rentáveis" className="glass-card">
            {data.topVeiculosRentaveis.length === 0 ? (
              <p style={{ color: 'var(--text-muted)' }}>Sem dados suficientes.</p>
            ) : (
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {data.topVeiculosRentaveis.map((v) => (
                  <li key={v.veiculoId} style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 0', borderBottom: '1px solid var(--border-color)' }}>
                    <span>{v.modelo} ({v.placa})</span>
                    <span style={{ color: 'var(--success)', fontWeight: 600 }}>+ R$ {v.saldoLiquido.toFixed(2)}</span>
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
    </div>
  );
}
