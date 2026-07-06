import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { clienteService } from '../services/clienteService';
import { Cliente } from '../interfaces/cliente';

export default function Clientes() {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState(true);

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

  const columns = [
    { header: 'Nome', accessor: 'nome' as keyof Cliente },
    { header: 'Documento', accessor: 'documento' as keyof Cliente },
    { header: 'E-mail', accessor: 'email' as keyof Cliente },
    { header: 'Telefone', accessor: 'telefone' as keyof Cliente },
    { 
      header: 'Ações', 
      accessor: (row: Cliente) => (
        <Button variant="ghost" onClick={() => alert(`Editar ${row.nome}`)}>Editar</Button>
      ) 
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700 }}>Clientes</h1>
        <Button variant="primary">Novo Cliente</Button>
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
    </div>
  );
}
