import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { EncerramentoContratoRequest } from '../../interfaces/contrato';

const encerramentoSchema = z.object({
  kmFinal: z.preprocess((val) => Number(val), z.number().min(0, 'Deve ser maior que 0')),
  dataDevolucao: z.string().min(1, 'Obrigatório'),
  valorAdicional: z.preprocess((val) => Number(val), z.number().optional()),
});

type EncerramentoFormData = z.infer<typeof encerramentoSchema>;

interface EncerrarContratoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: EncerramentoContratoRequest) => Promise<void>;
  kmInicial?: number;
}

export function EncerrarContratoModal({ isOpen, onClose, onSave, kmInicial = 0 }: EncerrarContratoModalProps) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<EncerramentoFormData>({
    resolver: zodResolver(encerramentoSchema),
  });

  const onSubmit = async (data: EncerramentoFormData) => {
    if (data.kmFinal < kmInicial) {
      alert(`O KM Final não pode ser menor que o KM Inicial (${kmInicial})`);
      return;
    }
    try {
      await onSave({
        ...data,
        dataDevolucao: data.dataDevolucao + 'T12:00:00Z'
      });
      onClose();
    } catch (error) {
      console.error('Erro ao encerrar:', error);
      alert('Erro ao encerrar contrato');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Encerrar Locação (Checkout)" maxWidth="500px">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        <div style={{ background: 'rgba(255,255,255,0.05)', padding: '12px', borderRadius: '8px' }}>
          <span style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>KM Inicial no momento da locação: </span>
          <strong style={{ color: 'var(--primary-light)' }}>{kmInicial} km</strong>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="KM Atual (Devolução)" type="number" {...register('kmFinal')} error={errors.kmFinal?.message} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Data da Devolução" type="date" {...register('dataDevolucao')} error={errors.dataDevolucao?.message} />
          </div>
        </div>

        <Input label="Valor Adicional (R$)" type="number" step="0.01" {...register('valorAdicional')} 
               placeholder="Ex: Combustível, multas, avarias..." />

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
          <Button variant="ghost" type="button" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit" disabled={isSubmitting} style={{ background: 'var(--success)' }}>
            {isSubmitting ? 'Encerrando...' : 'Confirmar Devolução'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
