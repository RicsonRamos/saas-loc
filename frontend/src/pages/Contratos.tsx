import { useEffect, useState } from 'react';
import { Card } from '../components/ui/Card';
import { Table } from '../components/ui/Table';
import { Button } from '../components/ui/Button';
import { contratoService } from '../services/contratoService';
import { Contrato, ContratoRequest, EncerramentoContratoRequest } from '../interfaces/contrato';
import { ContratoModal } from './contratos/ContratoModal';
import { EncerrarContratoModal } from './contratos/EncerrarContratoModal';
import { FileText, Plus, CheckCircle, Ban } from 'lucide-react';
import { Badge } from '../components/ui/Badge';

export default function Contratos() {
  const [contratos, setContratos] = useState<Contrato[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [isCloseOpen, setIsCloseOpen] = useState(false);
  const [selectedContrato, setSelectedContrato] = useState<Contrato | null>(null);

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

  const handleCreate = async (data: ContratoRequest) => {
    await contratoService.criar(data);
    loadContratos();
  };

  const handleClose = async (data: EncerramentoContratoRequest) => {
    if (selectedContrato) {
      await contratoService.encerrar(selectedContrato.id, data);
      setSelectedContrato(null);
      loadContratos();
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ATIVO': return <Badge variant="info">Ativo</Badge>;
      case 'ENCERRADO': return <Badge variant="success">Encerrado</Badge>;
      case 'CANCELADO': return <Badge variant="error">Cancelado</Badge>;
      case 'INADIMPLENTE': return <Badge variant="warning">Inadimplente</Badge>;
      default: return <Badge variant="default">{status}</Badge>;
    }
  };

  const columns = [
    { header: 'ID', accessor: (row: Contrato) => row.id.split('-')[0].toUpperCase() },
    { header: 'Cliente', accessor: 'clienteNome' as keyof Contrato },
    { header: 'Veículo', accessor: 'veiculoPlaca' as keyof Contrato },
    { header: 'Data Início', accessor: (row: Contrato) => new Date(row.dataInicio).toLocaleDateString() },
    { header: 'Previsão Fim', accessor: (row: Contrato) => new Date(row.dataFimPrevista).toLocaleDateString() },
    { header: 'Valor (R$)', accessor: (row: Contrato) => row.valorTotal.toFixed(2) },
    { 
      header: 'Status', 
      accessor: (row: Contrato) => getStatusBadge(row.status)
    },
    { 
      header: 'Ações', 
      accessor: (row: Contrato) => (
        <div style={{ display: 'flex', gap: '8px' }}>
          {row.status === 'ATIVO' && (
            <Button variant="ghost" onClick={() => { setSelectedContrato(row); setIsCloseOpen(true); }} title="Encerrar Contrato">
              <CheckCircle size={16} color="var(--success)" />
            </Button>
          )}
          {row.status === 'ATIVO' && (
            <Button variant="ghost" title="Cancelar Contrato">
              <Ban size={16} color="var(--error)" />
            </Button>
          )}
        </div>
      ) 
    }
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '12px' }}>
          <FileText size={32} color="var(--primary-light)" />
          Contratos de Locação
        </h1>
        <Button variant="primary" onClick={() => setIsCreateOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Plus size={20} />
          Nova Locação
        </Button>
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

      <ContratoModal 
        isOpen={isCreateOpen}
        onClose={() => setIsCreateOpen(false)}
        onSave={handleCreate}
      />

      <EncerrarContratoModal 
        isOpen={isCloseOpen}
        onClose={() => { setIsCloseOpen(false); setSelectedContrato(null); }}
        onSave={handleClose}
        kmInicial={selectedContrato?.kmInicial}
      />
    </div>
  );
}
