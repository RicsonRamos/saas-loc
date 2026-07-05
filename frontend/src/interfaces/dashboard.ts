import { FluxoCaixaResponse } from './financeiro';

export interface OcupacaoFrotaDTO {
  totalVeiculos: number;
  veiculosDisponiveis: number;
  veiculosLocados: number;
  veiculosEmManutencao: number;
  taxaOcupacao: number;
}

export interface RentabilidadeVeiculoDTO {
  veiculoId: string;
  placa: string;
  modelo: string;
  totalReceitas: number;
  totalDespesas: number;
  saldoLiquido: number;
}

export interface DashboardResponse {
  ocupacaoFrota: OcupacaoFrotaDTO;
  balancoMensal: FluxoCaixaResponse;
  topVeiculosRentaveis: RentabilidadeVeiculoDTO[];
  topVeiculosPrejuizo: RentabilidadeVeiculoDTO[];
}
