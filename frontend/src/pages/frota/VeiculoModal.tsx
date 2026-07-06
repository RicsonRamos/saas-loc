import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { VeiculoRequest } from '../../interfaces/veiculo';

const veiculoSchema = z.object({
  placa: z.string().length(7, 'Placa deve ter 7 caracteres'),
  chassi: z.string().min(17, 'Chassi incompleto'),
  renavam: z.string().optional(),
  marca: z.string().min(2, 'Obrigatório'),
  modelo: z.string().min(2, 'Obrigatório'),
  anoFabricacao: z.preprocess((val) => Number(val), z.number().min(1900)),
  anoModelo: z.preprocess((val) => Number(val), z.number().min(1900)),
  cor: z.string().optional(),
  quilometragem: z.preprocess((val) => Number(val), z.number().min(0)),
  status: z.enum(['DISPONIVEL', 'RESERVADO', 'LOCADO', 'MANUTENCAO', 'INATIVO', 'VENDIDO']),
  valorFipe: z.preprocess((val) => Number(val), z.number().optional()),
});

type VeiculoFormData = z.infer<typeof veiculoSchema>;

interface VeiculoModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: VeiculoRequest) => Promise<void>;
}

export function VeiculoModal({ isOpen, onClose, onSave }: VeiculoModalProps) {
  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<VeiculoFormData>({
    resolver: zodResolver(veiculoSchema),
    defaultValues: {
      status: 'DISPONIVEL',
      quilometragem: 0,
    }
  });

  const onSubmit = async (data: VeiculoFormData) => {
    try {
      await onSave(data as VeiculoRequest);
      onClose();
    } catch (error) {
      console.error('Erro ao salvar veículo:', error);
      alert('Erro ao salvar veículo');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Novo Veículo" maxWidth="600px">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="Placa" {...register('placa')} error={errors.placa?.message} placeholder="ABC1234" />
          </div>
          <div style={{ flex: 2 }}>
            <Input label="Chassi" {...register('chassi')} error={errors.chassi?.message} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="Marca" {...register('marca')} error={errors.marca?.message} placeholder="Ex: Toyota" />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Modelo" {...register('modelo')} error={errors.modelo?.message} placeholder="Ex: Corolla" />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Cor" {...register('cor')} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="Ano Fabricação" type="number" {...register('anoFabricacao')} error={errors.anoFabricacao?.message} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Ano Modelo" type="number" {...register('anoModelo')} error={errors.anoModelo?.message} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Quilometragem (km)" type="number" {...register('quilometragem')} error={errors.quilometragem?.message} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Status Inicial</label>
            <select 
              {...register('status')}
              style={{
                width: '100%',
                padding: '12px',
                background: 'rgba(0,0,0,0.2)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--text-main)',
                outline: 'none'
              }}
            >
              <option value="DISPONIVEL">Disponível</option>
              <option value="MANUTENCAO">Em Manutenção</option>
              <option value="INATIVO">Inativo</option>
            </select>
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Valor FIPE (R$)" type="number" step="0.01" {...register('valorFipe')} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
          <Button variant="ghost" type="button" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Salvando...' : 'Salvar Veículo'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
