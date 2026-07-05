package com.locadora.dashboard.service;

import com.locadora.dashboard.dto.DashboardResponse;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.repository.VeiculoRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DashboardServiceTest {

    @Mock private VeiculoRepository veiculoRepository;
    @Mock private FinanceiroService financeiroService;
    @Mock private LancamentoFinanceiroRepository lancamentoRepository;
    @InjectMocks private DashboardService dashboardService;

    @Test
    void deveCalcularTaxaOcupacao() {
        when(veiculoRepository.countByDeletedAtIsNull()).thenReturn(10L);
        when(veiculoRepository.countByStatusAndDeletedAtIsNull(StatusVeiculo.DISPONIVEL)).thenReturn(3L);
        when(veiculoRepository.countByStatusAndDeletedAtIsNull(StatusVeiculo.LOCADO)).thenReturn(5L);
        when(veiculoRepository.countByStatusAndDeletedAtIsNull(StatusVeiculo.MANUTENCAO)).thenReturn(2L);
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
        when(lancamentoRepository.getRentabilidadeVeiculos()).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(10L, response.getOcupacaoFrota().getTotalVeiculos());
        assertEquals(50.0, response.getOcupacaoFrota().getTaxaOcupacao());
    }

    @Test
    void naoDeveLancarExcecaoDivisaoPorZeroFrotaVazia() {
        when(veiculoRepository.countByDeletedAtIsNull()).thenReturn(0L);
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
        when(lancamentoRepository.getRentabilidadeVeiculos()).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(0.0, response.getOcupacaoFrota().getTaxaOcupacao());
    }
}
