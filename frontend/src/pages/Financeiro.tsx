import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { financeiroService } from '../services/financeiroService';
import { LancamentoFinanceiro, LancamentoRequest } from '../interfaces/financeiro';
import { LancamentoModal } from './financeiro/LancamentoModal';
import { DollarSign, Plus, ArrowUpCircle, ArrowDownCircle } from 'lucide-react';
import { Badge } from '../components/ui/Badge';

export default function Financeiro() {
  const [lancamentos, setLancamentos] = useState<LancamentoFinanceiro[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadLancamentos();
  }, []);

  async function loadLancamentos() {
    setLoading(true);
    try {
      const res = await financeiroService.listar(0, 50);
      setLancamentos(res.data);
    } catch (error) {
      console.error('Erro ao carregar finanças:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSave = async (data: LancamentoRequest) => {
    await financeiroService.criar(data);
    loadLancamentos();
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'PAGO': return <Badge variant="success">Pago</Badge>;
      case 'PENDENTE': return <Badge variant="warning">Pendente</Badge>;
      case 'CANCELADO': return <Badge variant="error">Cancelado</Badge>;
      default: return <Badge variant="default">{status}</Badge>;
    }
  };

  const columns = [
    { 
      header: 'Tipo', 
      accessor: (row: LancamentoFinanceiro) => (
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: row.tipo === 'RECEITA' ? 'var(--success)' : 'var(--error)' }}>
          {row.tipo === 'RECEITA' ? <ArrowUpCircle size={18} /> : <ArrowDownCircle size={18} />}
          <span style={{ fontWeight: 600 }}>{row.tipo}</span>
        </div>
      )
    },
    { header: 'Descrição', accessor: 'descricao' as keyof LancamentoFinanceiro },
    { header: 'Categoria', accessor: 'categoria' as keyof LancamentoFinanceiro },
    { header: 'Vencimento', accessor: (row: LancamentoFinanceiro) => new Date(row.dataVencimento).toLocaleDateString() },
    { 
      header: 'Valor', 
      accessor: (row: LancamentoFinanceiro) => (
        <span style={{ fontWeight: 600 }}>R$ {row.valor.toFixed(2)}</span>
      )
    },
    { 
      header: 'Status', 
      accessor: (row: LancamentoFinanceiro) => getStatusBadge(row.status)
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '12px' }}>
          <DollarSign size={32} color="var(--primary-light)" />
          Financeiro
        </h1>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={20} />
          Novo Lançamento
        </Button>
      </div>
      
      <Card className="glass-card">
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Carregando lançamentos...</div>
        ) : (
          <Table<LancamentoFinanceiro>
            columns={columns}
            data={lancamentos}
            keyExtractor={(item) => item.id}
            emptyMessage="Nenhum lançamento financeiro."
          />
        )}
      </Card>

      <LancamentoModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSave}
      />
    </div>
  );
}
