import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { contratoService } from '../services/contratoService';
import { Contrato } from '../interfaces/contrato';

export default function Contratos() {
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadContratos();
  }, []);

  async function loadContratos() {
    setLoading(true);
    try {
      const res = await contratoService.listar(0, 50);
      setContratos(res.data);
    } catch (error) {
      console.error('Erro ao carregar contratos:', error);
    } finally {
      setLoading(false);
    }
  }

  const columns = [
    { header: 'Cliente', accessor: 'clienteNome' as keyof Contrato },
    { header: 'Veículo', accessor: 'veiculoPlaca' as keyof Contrato },
    { 
      header: 'Período', 
      accessor: (row: Contrato) => {
        const inicio = new Date(row.dataInicio).toLocaleDateString('pt-BR');
        const fim = new Date(row.dataFimPrevista).toLocaleDateString('pt-BR');
        return `${inicio} até ${fim}`;
      }
    },
    { header: 'Valor Total', accessor: (row: Contrato) => `R$ ${row.valorTotal.toFixed(2)}` },
    { 
      header: 'Status', 
      accessor: (row: Contrato) => {
        let color = 'var(--text-main)';
        if (row.status === 'ATIVO') color = 'var(--success)';
        if (row.status === 'CANCELADO' || row.status === 'INADIMPLENTE') color = 'var(--error)';
        return (
          <span style={{ color, fontWeight: 600 }}>{row.status}</span>
        );
      }
    },
    { 
      header: 'Ações', 
      accessor: (row: Contrato) => (
        <Button variant="ghost" onClick={() => alert(`Visualizar contrato de ${row.clienteNome}`)}>Ver Detalhes</Button>
      ) 
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Contratos e Locações</h1>
        <Button variant="primary">Nova Locação</Button>
      </div>
      
      <Card className="glass-card">
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Carregando contratos...</div>
        ) : (
          <Table<Contrato>
            columns={columns}
            data={contratos}
            keyExtractor={(item) => item.id}
            emptyMessage="Nenhum contrato ativo ou histórico encontrado."
          />
        )}
      </Card>
    </div>
  );
}
