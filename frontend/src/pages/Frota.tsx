import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { veiculoService } from '../services/veiculoService';
import { Veiculo, VeiculoRequest } from '../interfaces/veiculo';
import { VeiculoModal } from './frota/VeiculoModal';
import { Car, Plus, Trash2, Wrench } from 'lucide-react';
import { Badge } from '../components/ui/Badge';

export default function Frota() {
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

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

  const handleSave = async (data: VeiculoRequest) => {
    await veiculoService.criar(data);
    loadVeiculos();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este veículo?')) {
      await veiculoService.excluir(id);
      loadVeiculos();
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'DISPONIVEL': return <Badge variant="success">Disponível</Badge>;
      case 'LOCADO': return <Badge variant="info">Locado</Badge>;
      case 'MANUTENCAO': return <Badge variant="warning">Manutenção</Badge>;
      case 'RESERVADO': return <Badge variant="default">Reservado</Badge>;
      default: return <Badge variant="error">{status}</Badge>;
    }
  };

  const columns = [
    { header: 'Placa', accessor: 'placa' as keyof Veiculo },
    { header: 'Marca', accessor: 'marca' as keyof Veiculo },
    { header: 'Modelo', accessor: 'modelo' as keyof Veiculo },
    { header: 'Ano', accessor: (row: Veiculo) => `${row.anoFabricacao}/${row.anoModelo}` },
    { 
      header: 'Status', 
      accessor: (row: Veiculo) => getStatusBadge(row.status)
    },
    { 
      header: 'Ações', 
      accessor: (row: Veiculo) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          <Button variant="ghost" onClick={() => alert(`Manutenção ${row.placa}`)} title="Manutenção">
            <Wrench size={16} color="var(--text-muted)" />
          </Button>
          <Button variant="ghost" onClick={() => handleDelete(row.id)}>
            <Trash2 size={16} color="var(--error)" />
          </Button>
        </div>
      ) 
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Car size={32} color="var(--primary-light)" />
          Frota
        </h1>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={20} />
          Novo Veículo
        </Button>
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

      <VeiculoModal 
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSave}
      />
    </div>
  );
}
