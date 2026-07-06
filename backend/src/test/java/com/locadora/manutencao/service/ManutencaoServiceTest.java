package com.locadora.manutencao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.manutencao.dto.ConclusaoManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoResponse;
import com.locadora.manutencao.entity.Manutencao;
import com.locadora.manutencao.entity.TipoManutencao;
import com.locadora.manutencao.mapper.ManutencaoMapper;
import com.locadora.manutencao.repository.ManutencaoRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

/**
 * Testes unitários do serviço de manutenção.
 * Cobre regras de negócio: bloqueio de veículo locado e conclusão com geração de despesa.
 */
@ExtendWith(MockitoExtension.class)
class ManutencaoServiceTest {

    @Mock private ManutencaoRepository manutencaoRepository;
    @Mock private ManutencaoMapper manutencaoMapper;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private FinanceiroService financeiroService;
    @InjectMocks private ManutencaoService manutencaoService;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private Veiculo veiculo;
    private Manutencao manutencao;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculo.setQuilometragem(50000);
        veiculo.setPlaca("ABC-1234");

        manutencao = new Manutencao();
        manutencao.setId(UUID.randomUUID());
        manutencao.setVeiculo(veiculo);
        manutencao.setDescricao("Troca de óleo");
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    /**
     * Veículo com status LOCADO não pode ser enviado para oficina.
     */
    @Test
    void naoDeveRegistrarManutencaoSeVeiculoLocado() {
        veiculo.setStatus(StatusVeiculo.LOCADO);
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TENANT_ID))
                .thenReturn(Optional.of(veiculo));

        // Usa AllArgsConstructor — DTO não possui setters
        ManutencaoRequest request = new ManutencaoRequest(
                veiculo.getId(), TipoManutencao.CORRETIVA, "Reparo no motor", LocalDate.now()
        );

        assertThrows(BusinessException.class, () -> manutencaoService.registrarManutencao(request));
    }

    /**
     * Conclusão de manutenção: libera veículo, registra custo e gera lançamento financeiro.
     */
    @Test
    void deveConcluirManutencaoEDesbloquearVeiculo() {
        when(manutencaoRepository.findByIdAndTenantIdAndDeletedAtIsNull(manutencao.getId(), TENANT_ID))
                .thenReturn(Optional.of(manutencao));
        when(manutencaoMapper.toResponse(any())).thenReturn(new ManutencaoResponse());
        when(manutencaoRepository.save(any())).thenReturn(manutencao);
        when(veiculoRepository.save(any())).thenReturn(veiculo);

        // Usa AllArgsConstructor — DTO não possui setters
        ConclusaoManutencaoRequest request = new ConclusaoManutencaoRequest(
                new BigDecimal("500.00"), LocalDate.now(), null
        );

        manutencaoService.concluirManutencao(manutencao.getId(), request);

        assertNotNull(manutencao.getDataFim());
        assertEquals(new BigDecimal("500.00"), manutencao.getCusto());
        assertEquals(StatusVeiculo.DISPONIVEL, veiculo.getStatus());

        verify(financeiroService).criarLancamento(any());
        verify(manutencaoRepository).save(manutencao);
    }
}
