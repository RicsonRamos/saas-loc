import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { financeiroService } from '../services/financeiroService';
import { LancamentoFinanceiro } from '../interfaces/financeiro';

export default function Financeiro() {
  const [lancamentos, setLancamentos] = useState<LancamentoFinanceiro[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLancamentos();
  }, []);

  async function loadLancamentos() {
    setLoading(true);
    try {
      const res = await financeiroService.listar(0, 50);
      setLancamentos(res.data);
    } catch (error) {
      console.error('Erro ao carregar lançamentos:', error);
    } finally {
      setLoading(false);
    }
  }

  const columns = [
    { 
      header: 'Tipo', 
      accessor: (row: LancamentoFinanceiro) => (
        <span style={{ 
          color: row.tipo === 'RECEITA' ? 'var(--success)' : 'var(--error)',
          fontWeight: 600,
          background: row.tipo === 'RECEITA' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
          padding: '4px 8px',
          borderRadius: '4px',
          fontSize: '0.8rem'
        }}>
          {row.tipo}
        </span>
      )
    },
    { header: 'Categoria', accessor: 'categoria' as keyof LancamentoFinanceiro },
    { header: 'Descrição', accessor: 'descricao' as keyof LancamentoFinanceiro },
    { header: 'Valor', accessor: (row: LancamentoFinanceiro) => `R$ ${row.valor.toFixed(2)}` },
    { 
      header: 'Vencimento', 
      accessor: (row: LancamentoFinanceiro) => new Date(row.dataVencimento).toLocaleDateString('pt-BR')
    },
    { 
      header: 'Status', 
      accessor: (row: LancamentoFinanceiro) => {
        let color = 'var(--text-main)';
        if (row.status === 'PAGO') color = 'var(--success)';
        if (row.status === 'CANCELADO') color = 'var(--error)';
        return <span style={{ color, fontWeight: 600 }}>{row.status}</span>;
      }
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Financeiro</h1>
        <Button variant="primary">Novo Lançamento</Button>
      </div>
      
      <Card className="glass-card">
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Carregando fluxo de caixa...</div>
        ) : (
          <Table<LancamentoFinanceiro>
            columns={columns}
            data={lancamentos}
            keyExtractor={(item) => item.id}
            emptyMessage="Nenhum lançamento encontrado."
          />
        )}
      </Card>
    </div>
  );
}
