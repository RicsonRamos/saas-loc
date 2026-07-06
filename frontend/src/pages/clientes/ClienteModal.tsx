import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Modal } from '../../components/ui/Modal';
import { Button } from '../../components/ui/Button';
import { Input } from '../../components/ui/Input';
import { ClienteRequest } from '../../interfaces/cliente';

const clienteSchema = z.object({
  nome: z.string().min(3, 'Nome muito curto'),
  tipo: z.enum(['PESSOA_FISICA', 'PESSOA_JURIDICA']),
  documento: z.string().min(11, 'Documento inválido'),
  email: z.string().email('E-mail inválido').optional().or(z.literal('')),
  telefone: z.string().optional(),
  cnh: z.string().optional(),
  cep: z.string().optional(),
  logradouro: z.string().optional(),
  numero: z.string().optional(),
  cidade: z.string().optional(),
  uf: z.string().max(2).optional(),
});

type ClienteFormData = z.infer<typeof clienteSchema>;

interface ClienteModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (data: ClienteRequest) => Promise<void>;
}

export function ClienteModal({ isOpen, onClose, onSave }: ClienteModalProps) {
  const { register, handleSubmit, formState: { errors, isSubmitting }, watch } = useForm<ClienteFormData>({
    resolver: zodResolver(clienteSchema),
    defaultValues: {
      tipo: 'PESSOA_FISICA'
    }
  });

  const tipo = watch('tipo');

  const onSubmit = async (data: ClienteFormData) => {
    try {
      await onSave(data as ClienteRequest);
      onClose();
    } catch (error) {
      console.error('Erro ao salvar:', error);
      alert('Erro ao salvar cliente');
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Novo Cliente" maxWidth="600px">
      <form onSubmit={handleSubmit(onSubmit)} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', marginBottom: '8px', fontSize: '0.9rem', color: 'var(--text-muted)' }}>Tipo</label>
            <select 
              {...register('tipo')}
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
              <option value="PESSOA_FISICA">Pessoa Física (CPF)</option>
              <option value="PESSOA_JURIDICA">Pessoa Jurídica (CNPJ)</option>
            </select>
          </div>
          
          <div style={{ flex: 2 }}>
            <Input 
              label={tipo === 'PESSOA_FISICA' ? 'CPF' : 'CNPJ'}
              placeholder="Apenas números"
              {...register('documento')}
              error={errors.documento?.message}
            />
          </div>
        </div>

        <Input 
          label={tipo === 'PESSOA_FISICA' ? 'Nome Completo' : 'Razão Social'}
          {...register('nome')}
          error={errors.nome?.message}
        />

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="E-mail" type="email" {...register('email')} error={errors.email?.message} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Telefone" {...register('telefone')} />
          </div>
        </div>

        {tipo === 'PESSOA_FISICA' && (
          <Input label="Número da CNH" {...register('cnh')} />
        )}

        <div style={{ borderTop: '1px solid var(--border-color)', margin: '16px 0' }} />
        
        <h4 style={{ margin: 0, color: 'var(--text-muted)' }}>Endereço (Opcional)</h4>
        
        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 1 }}>
            <Input label="CEP" {...register('cep')} />
          </div>
          <div style={{ flex: 2 }}>
            <Input label="Logradouro" {...register('logradouro')} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="Número" {...register('numero')} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px' }}>
          <div style={{ flex: 2 }}>
            <Input label="Cidade" {...register('cidade')} />
          </div>
          <div style={{ flex: 1 }}>
            <Input label="UF" {...register('uf')} />
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px' }}>
          <Button variant="ghost" type="button" onClick={onClose}>Cancelar</Button>
          <Button variant="primary" type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Salvando...' : 'Salvar Cliente'}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
