import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { veiculoService } from '../services/veiculoService';
import { Veiculo } from '../interfaces/veiculo';

export default function Frota() {
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadVeiculos();
  }, []);

  async function loadVeiculos() {
    setLoading(true);
    try {
      const res = await veiculoService.listar(0, 50);
      setVeiculos(res.data);
    } catch (error) {
      console.error('Erro ao carregar veículos:', error);
    } finally {
      setLoading(false);
    }
  }

  const columns = [
    { header: 'Placa', accessor: 'placa' as keyof Veiculo },
    { header: 'Marca', accessor: 'marca' as keyof Veiculo },
    { header: 'Modelo', accessor: 'modelo' as keyof Veiculo },
    { header: 'Ano', accessor: (row: Veiculo) => `${row.anoFabricacao}/${row.anoModelo}` },
    { 
      header: 'Status', 
      accessor: (row: Veiculo) => (
        <span style={{
          padding: '4px 8px',
          borderRadius: '12px',
          fontSize: '0.8rem',
          fontWeight: 600,
          background: row.status === 'DISPONIVEL' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(239, 68, 68, 0.2)',
          color: row.status === 'DISPONIVEL' ? 'var(--success)' : 'var(--error)'
        }}>
          {row.status}
        </span>
      ) 
    },
    { 
      header: 'Ações', 
      accessor: (row: Veiculo) => (
        <Button variant="ghost" onClick={() => alert(`Editar ${row.placa}`)}>Editar</Button>
      ) 
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Frota (Veículos)</h1>
        <Button variant="primary">Novo Veículo</Button>
      </div>
      
      <Card className="glass-card">
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Carregando frota...</div>
        ) : (
          <Table<Veiculo>
            columns={columns}
            data={veiculos}
            keyExtractor={(item) => item.id}
            emptyMessage="Nenhum veículo cadastrado na frota."
          />
        )}
      </Card>
    </div>
  );
}
