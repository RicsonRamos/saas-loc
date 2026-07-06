import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { ContratoRequest } from '../../interfaces/contrato';
import { clienteService } from '../../services/clienteService';
import { veiculoService } from '../../services/veiculoService';
import { Cliente } from '../../interfaces/cliente';
import { Veiculo } from '../../interfaces/veiculo';

const contratoSchema = z.object({
  clienteId: z.string().uuid('Selecione um cliente'),
  veiculoId: z.string().uuid('Selecione um veículo'),
  dataInicio: z.string().min(1, 'Obrigatório'),
  dataFimPrevista: z.string().min(1, 'Obrigatório'),
  valorTotal: z.coerce.number().min(1, 'Valor obrigatório'),
  caucao: z.coerce.number().optional(),
});

type ContratoFormData = z.infer<typeof contratoSchema>;

interface ContratoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: ContratoRequest) => Promise<void>;
}

export function ContratoModal({ isOpen, onClose, onSave }: ContratoModalProps) {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [veiculos, setVeiculos] = useState<Veiculo[]>([]);
  const [loading, setLoading] = useState(true);

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<ContratoFormData>({
    resolver: zodResolver(contratoSchema) as any,
  });

  useEffect(() => {
    if (isOpen) {
      loadData();
    }
  }, [isOpen]);

  async function loadData() {
    setLoading(true);
    try {
      const [resClientes, resVeiculos] = await Promise.all([
        clienteService.listar(0, 100),
        veiculoService.listar(0, 100)
      ]);
      setClientes(resClientes.data);
      // Filtra apenas disponíveis
      setVeiculos(resVeiculos.data.filter(v => v.status === 'DISPONIVEL'));
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }

  const onSubmit = async (data: ContratoFormData) => {
    try {
      // Ajustar fuso ou formato de data se necessário pro back
      await onSave({
        ...data,
        dataInicio: data.dataInicio + 'T12:00:00Z',
        dataFimPrevista: data.dataFimPrevista + 'T12:00:00Z'
      } as unknown as ContratoRequest);
      onClose();
    } catch (error) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao gerar contrato');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Nova Locação" maxWidth="600px">
      {loading ? (
        <div style={{ color: 'var(--text-muted)' }}>Carregando dados...</div>
      ) : (
        <form onSubmit={handleSubmit(onSubmit as any)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Cliente</label>
            <select 
              {...register('clienteId')}
              style={{
                padding: '12px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)', color: 'var(--text-main)', outline: 'none'
              }}
            >
              <option value="">Selecione...</option>
              {clientes.map(c => <option key={c.id} value={c.id}>{c.nome} ({c.documento})</option>)}
            </select>
            {errors.clienteId && <span style={{ color: 'var(--error)', fontSize: '0.8rem' }}>{errors.clienteId.message}</span>}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            <label style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Veículo (Apenas Disponíveis)</label>
            <select 
              {...register('veiculoId')}
              style={{
                padding: '12px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)', color: 'var(--text-main)', outline: 'none'
              }}
            >
              <option value="">Selecione...</option>
              {veiculos.map(v => <option key={v.id} value={v.id}>{v.modelo} - {v.placa}</option>)}
            </select>
            {errors.veiculoId && <span style={{ color: 'var(--error)', fontSize: '0.8rem' }}>{errors.veiculoId.message}</span>}
          </div>

          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ flex: 1 }}>
              <Input label="Data de Início" type="date" {...register('dataInicio')} error={errors.dataInicio?.message} />
            </div>
            <div style={{ flex: 1 }}>
              <Input label="Data Prevista de Devolução" type="date" {...register('dataFimPrevista')} error={errors.dataFimPrevista?.message} />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px' }}>
            <div style={{ flex: 1 }}>
              <Input label="Valor Total (R$)" type="number" step="0.01" {...register('valorTotal')} error={errors.valorTotal?.message} />
            </div>
            <div style={{ flex: 1 }}>
              <Input label="Caução Retida (R$)" type="number" step="0.01" {...register('caucao')} />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
            <Button variant="ghost" type="button" onClick={onClose}>Cancelar</Button>
            <Button variant="primary" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Gerando...' : 'Gerar Contrato'}
            </Button>
          </div>
        </form>
      )}
    </Modal>
  );
}
