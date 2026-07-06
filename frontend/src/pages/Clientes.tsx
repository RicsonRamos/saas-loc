import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { clienteService } from '../services/clienteService';
import { Cliente, ClienteRequest } from '../interfaces/cliente';
import { ClienteModal } from './clientes/ClienteModal';
import { Users, Plus, Trash2 } from 'lucide-react';

export default function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    loadClientes();
  }, []);

  async function loadClientes() {
    setLoading(true);
    try {
      const res = await clienteService.listar(0, 50);
      setClientes(res.data);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    } finally {
      setLoading(false);
    }
  }

  const handleSave = async (data: ClienteRequest) => {
    await clienteService.criar(data);
    loadClientes();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Tem certeza que deseja excluir este cliente?')) {
      await clienteService.excluir(id);
      loadClientes();
    }
  };

  const columns = [
    { header: 'Nome', accessor: 'nome' as keyof Cliente },
    { header: 'Documento', accessor: 'documento' as keyof Cliente },
    { header: 'E-mail', accessor: 'email' as keyof Cliente },
    { header: 'Telefone', accessor: 'telefone' as keyof Cliente },
    { 
      header: 'Ações', 
      accessor: (row: Cliente) => (
        <div style={{ display: 'flex', gap: '8px' }}>
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
          <Users size={32} color="var(--primary-light)" />
          Clientes
        </h1>
        <Button variant="primary" onClick={() => setIsModalOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={20} />
          Novo Cliente
        </Button>
      </div>
      
      <Card className="glass-card">
        {loading ? (
          <div style={{ color: 'var(--text-muted)' }}>Carregando clientes...</div>
        ) : (
          <Table<Cliente>
            columns={columns}
            data={clientes}
            keyExtractor={(item) => item.id}
            emptyMessage="Nenhum cliente cadastrado."
          />
        )}
      </Card>

      <ClienteModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSave={handleSave} 
      />
    </div>
  );
}
