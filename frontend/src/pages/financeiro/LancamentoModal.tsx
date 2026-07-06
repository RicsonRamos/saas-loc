import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { LancamentoRequest } from '../../interfaces/financeiro';

const lancamentoSchema = z.object({
  tipo: z.enum(['RECEITA', 'DESPESA']),
  valor: z.preprocess((val) => Number(val), z.number().min(0.01, 'Valor inválido')),
  categoria: z.enum(['ALUGUEL', 'CAUCAO', 'MANUTENCAO', 'COMBUSTIVEL', 'IMPOSTOS_TAXAS', 'SALARIOS', 'OUTROS']),
  descricao: z.string().min(3, 'Descrição obrigatória'),
  status: z.enum(['PENDENTE', 'PAGO', 'CANCELADO']),
  dataVencimento: z.string().min(1, 'Obrigatório'),
  dataPagamento: z.string().optional().or(z.literal('')),
});

type LancamentoFormData = z.infer<typeof lancamentoSchema>;

interface LancamentoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: LancamentoRequest) => Promise<void>;
}

export function LancamentoModal({ isOpen, onClose, onSave }: LancamentoModalProps) {
  const { register, handleSubmit, formState: { errors, isSubmitting }, watch } = useForm<LancamentoFormData>({
    resolver: zodResolver(lancamentoSchema),
    defaultValues: {
      tipo: 'DESPESA',
      status: 'PENDENTE'
    }
  });

  const onSubmit = async (data: LancamentoFormData) => {
    try {
      await onSave({
        ...data,
        dataVencimento: data.dataVencimento + 'T12:00:00Z',
        dataPagamento: data.dataPagamento ? data.dataPagamento + 'T12:00:00Z' : undefined
      } as unknown as LancamentoRequest);
      onClose();
    } catch (error) {
      console.error('Erro ao salvar lançamento:', error);
      alert('Erro ao salvar lançamento');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Novo Lançamento Financeiro" maxWidth="600px">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Tipo</label>
            <select 
              {...register('tipo')}
              style={{
                width: '100%', padding: '12px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)', color: 'var(--text-main)', outline: 'none'
              }}
            >
              <option value="RECEITA">Receita</option>
              <option value="DESPESA">Despesa</option>
            </select>
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Valor (R$)" type="number" step="0.01" {...register('valor')} error={errors.valor?.message} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Categoria</label>
            <select 
              {...register('categoria')}
              style={{
                width: '100%', padding: '12px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)', color: 'var(--text-main)', outline: 'none'
              }}
            >
              <option value="ALUGUEL">Aluguel</option>
              <option value="CAUCAO">Caução</option>
              <option value="MANUTENCAO">Manutenção</option>
              <option value="COMBUSTIVEL">Combustível</option>
              <option value="IMPOSTOS_TAXAS">Impostos/Taxas</option>
              <option value="SALARIOS">Salários</option>
              <option value="OUTROS">Outros</option>
            </select>
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Status</label>
            <select 
              {...register('status')}
              style={{
                width: '100%', padding: '12px', background: 'rgba(0,0,0,0.2)', border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)', color: 'var(--text-main)', outline: 'none'
              }}
            >
              <option value="PENDENTE">Pendente</option>
              <option value="PAGO">Pago</option>
              <option value="CANCELADO">Cancelado</option>
            </select>
          </div>
        </div>

        <Input label="Descrição" {...register('descricao')} error={errors.descricao?.message} placeholder="Ex: Pagamento conta de luz" />

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="Data de Vencimento" type="date" {...register('dataVencimento')} error={errors.dataVencimento?.message} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Data de Pagamento" type="date" {...register('dataPagamento')} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
          <Button variant="ghost" type="button" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Salvando...' : 'Salvar Lançamento'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
