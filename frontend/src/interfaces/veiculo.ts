export type StatusVeiculo = 
  | 'DISPONIVEL'
  | 'RESERVADO'
  | 'LOCADO'
  | 'MANUTENCAO'
  | 'INATIVO'
  | 'VENDIDO';

export interface Veiculo {
  id: string;
  placa: string;
  chassi: string;
  renavam?: string;
  marca: string;
  modelo: string;
  anoFabricacao: number;
  anoModelo: number;
  cor?: string;
  quilometragem: number;
  status: StatusVeiculo;
  valorFipe?: number;
  valorCompra?: number;
  dataCompra?: string;
  documentoUrl?: string;
}

export interface VeiculoRequest extends Omit<Veiculo, 'id'> {}
