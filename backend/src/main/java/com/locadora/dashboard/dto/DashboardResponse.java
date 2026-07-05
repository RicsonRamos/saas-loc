package com.locadora.dashboard.dto;

import com.locadora.financeiro.dto.FluxoCaixaResponse;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.util.List;

/**
 * Payload consolidado do Dashboard da aplicação.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DashboardResponse {

    /** Retrato momentâneo da frota */
    private OcupacaoFrotaDTO ocupacaoFrota;

    /** Balanço do mês atual (aproveitando o EPIC 5) */
    private FluxoCaixaResponse balancoMensal;

    /** Ranking Top 5 dos veículos que mais geraram dinheiro */
    private List<RentabilidadeVeiculoDTO> topVeiculosRentaveis;

    /** Ranking Top 5 dos veículos que mais deram prejuízo/despesa */
    private List<RentabilidadeVeiculoDTO> topVeiculosPrejuizo;
}
