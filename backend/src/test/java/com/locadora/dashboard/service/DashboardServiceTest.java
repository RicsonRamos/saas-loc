package com.locadora.dashboard.service;

import com.locadora.dashboard.dto.DashboardResponse;
import com.locadora.dashboard.dto.RentabilidadeVeiculoProjection;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.shared.tenant.TenantContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DashboardServiceTest {

    @Mock
    private VeiculoRepository veiculoRepository;

    @Mock
    private FinanceiroService financeiroService;

    @Mock
    private LancamentoFinanceiroRepository lancamentoRepository;

    @InjectMocks
    private DashboardService dashboardService;

    private final UUID tenantId = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        TenantContext.setTenantId(tenantId);
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void deveCalcularTaxaDeOcupacaoCorretamente() {
        // Mock frota: 10 carros no total (5 locados, 3 disp, 2 oficina)
        when(veiculoRepository.countByTenantIdAndDeletedAtIsNull(tenantId)).thenReturn(10L);
        when(veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.DISPONIVEL)).thenReturn(3L);
        when(veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.LOCADO)).thenReturn(5L);
        when(veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.MANUTENCAO)).thenReturn(2L);
        
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
                
        when(lancamentoRepository.getRentabilidadeVeiculos(tenantId)).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(10L, response.getOcupacaoFrota().getTotalVeiculos());
        assertEquals(50.0, response.getOcupacaoFrota().getTaxaOcupacao()); // 5 / 10 = 50%
    }

    @Test
    void naoDeveLancarExcecaoDivisaoPorZeroSeFrotaVazia() {
        when(veiculoRepository.countByTenantIdAndDeletedAtIsNull(tenantId)).thenReturn(0L);
        
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
                
        when(lancamentoRepository.getRentabilidadeVeiculos(tenantId)).thenReturn(List.of());

        DashboardResponse response = dashboardService.obterDashboardMensal();

        assertNotNull(response);
        assertEquals(0.0, response.getOcupacaoFrota().getTaxaOcupacao());
    }

    @Test
    void deveOrdernarTopRentaveisEPrejuizo() {
        // Simulando a projeção retornando dados agrupados pelo banco
        RentabilidadeVeiculoProjection carroLucro = criarProjecao("ABC-1234", "Civic", new BigDecimal("5000.00"), new BigDecimal("1000.00")); // +4000
        RentabilidadeVeiculoProjection carroPreju = criarProjecao("XYZ-9999", "Gol", new BigDecimal("1000.00"), new BigDecimal("3000.00")); // -2000
        
        when(veiculoRepository.countByTenantIdAndDeletedAtIsNull(tenantId)).thenReturn(2L);
        
        when(financeiroService.obterFluxoMensal(any(Integer.class), any(Integer.class)))
                .thenReturn(FluxoCaixaResponse.builder().build());
                
        when(lancamentoRepository.getRentabilidadeVeiculos(tenantId)).thenReturn(List.of(carroLucro, carroPreju));

        DashboardResponse response = dashboardService.obterDashboardMensal();

        // Top Lucro deve ter o Civic em 1º
        assertEquals("ABC-1234", response.getTopVeiculosRentaveis().get(0).getPlaca());
        assertEquals(new BigDecimal("4000.00"), response.getTopVeiculosRentaveis().get(0).getSaldoLiquido());

        // Top Prejuízo deve ter o Gol em 1º (ordem crescente de saldo)
        assertEquals("XYZ-9999", response.getTopVeiculosPrejuizo().get(0).getPlaca());
        assertEquals(new BigDecimal("-2000.00"), response.getTopVeiculosPrejuizo().get(0).getSaldoLiquido());
    }

    private RentabilidadeVeiculoProjection criarProjecao(String placa, String modelo, BigDecimal receitas, BigDecimal despesas) {
        return new RentabilidadeVeiculoProjection() {
            @Override
            public UUID getVeiculoId() { return UUID.randomUUID(); }
            @Override
            public String getPlaca() { return placa; }
            @Override
            public String getModelo() { return modelo; }
            @Override
            public BigDecimal getTotalReceitas() { return receitas; }
            @Override
            public BigDecimal getTotalDespesas() { return despesas; }
        };
    }
}
