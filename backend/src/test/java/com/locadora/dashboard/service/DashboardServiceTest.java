package com.locadora.dashboard.service;

import com.locadora.dashboard.dto.DashboardResponse;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.repository.VeiculoRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DashboardServiceTest {

    @Mock private VeiculoRepository veiculoRepository;
    @Mock private FinanceiroService financeiroService;
    @Mock private LancamentoFinanceiroRepository lancamentoRepository;
    @InjectMocks private DashboardService dashboardService;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    @Test
    void deveCalcularTaxaOcupacao() {
        when(veiculoRepository.countByTenantIdAndDeletedAtIsNull(TENANT_ID)).thenReturn(10L);
        when(veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.DISPONIVEL, TENANT_ID)).thenReturn(3L);
        when(veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.LOCADO, TENANT_ID)).thenReturn(5L);
        when(veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.MANUTENCAO, TENANT_ID)).thenReturn(2L);
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
        when(lancamentoRepository.getRentabilidadeVeiculos(TENANT_ID)).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(10L, response.getOcupacaoFrota().getTotalVeiculos());
        assertEquals(50.0, response.getOcupacaoFrota().getTaxaOcupacao());
    }

    @Test
    void naoDeveLancarExcecaoDivisaoPorZeroFrotaVazia() {
        when(veiculoRepository.countByTenantIdAndDeletedAtIsNull(TENANT_ID)).thenReturn(0L);
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
        when(lancamentoRepository.getRentabilidadeVeiculos(TENANT_ID)).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(0.0, response.getOcupacaoFrota().getTaxaOcupacao());
    }
}
