package com.locadora.manutencao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.manutencao.dto.ConclusaoManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.entity.Manutencao;
import com.locadora.manutencao.entity.TipoManutencao;
import com.locadora.manutencao.repository.ManutencaoRepository;
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
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ManutencaoServiceTest {

    @Mock
    private ManutencaoRepository manutencaoRepository;

    @Mock
    private VeiculoRepository veiculoRepository;

    @Mock
    private FinanceiroService financeiroService;

    @InjectMocks
    private ManutencaoService manutencaoService;

    private final UUID tenantId = UUID.randomUUID();
    private Veiculo veiculo;
    private Manutencao manutencao;

    @BeforeEach
    void setUp() {
        TenantContext.setTenantId(tenantId);
        
        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setTenantId(tenantId);
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        
        manutencao = new Manutencao();
        manutencao.setId(UUID.randomUUID());
        manutencao.setTenantId(tenantId);
        manutencao.setVeiculo(veiculo);
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void naoDeveRegistrarManutencaoSeVeiculoLocado() {
        veiculo.setStatus(StatusVeiculo.LOCADO);
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), tenantId))
                .thenReturn(Optional.of(veiculo));
                
        ManutencaoRequest request = new ManutencaoRequest();
        request.setVeiculoId(veiculo.getId());
        
        assertThrows(BusinessException.class, () -> manutencaoService.registrarManutencao(request));
    }

    @Test
    void deveConcluirManutencaoEDesbloquearVeiculoEGerarDespesa() {
        when(manutencaoRepository.findByIdAndTenantIdAndDeletedAtIsNull(manutencao.getId(), tenantId))
                .thenReturn(Optional.of(manutencao));
                
        ConclusaoManutencaoRequest request = new ConclusaoManutencaoRequest();
        request.setCusto(new BigDecimal("500.00"));
        
        manutencaoService.concluirManutencao(manutencao.getId(), request);
        
        assertNotNull(manutencao.getDataFim());
        assertEquals(new BigDecimal("500.00"), manutencao.getCusto());
        assertEquals(StatusVeiculo.DISPONIVEL, veiculo.getStatus());
        
        verify(financeiroService).criarLancamento(any(LancamentoRequest.class));
        verify(manutencaoRepository).save(manutencao);
    }
}
