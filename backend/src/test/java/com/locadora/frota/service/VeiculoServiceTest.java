package com.locadora.frota.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.frota.dto.VeiculoRequest;
import com.locadora.frota.dto.VeiculoResponse;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.VeiculoMapper;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.shared.tenant.TenantContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.Pageable;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Collections;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Testes do VeiculoService.
 */
@ExtendWith(MockitoExtension.class)
class VeiculoServiceTest {

    @Mock
    private VeiculoRepository veiculoRepository;

    @Mock
    private VeiculoMapper veiculoMapper;

    @InjectMocks
    private VeiculoService veiculoService;

    private UUID tenantId;
    private VeiculoRequest request;

    @BeforeEach
    void setUp() {
        tenantId = UUID.randomUUID();
        TenantContext.setTenantId(tenantId);

        request = new VeiculoRequest(
                "ABC1234",
                "CHASSI123456789",
                "RENAVAM123",
                "Toyota",
                "Corolla",
                2022,
                2023,
                "Preto",
                15000,
                StatusVeiculo.DISPONIVEL,
                new BigDecimal("120000.00"),
                new BigDecimal("115000.00"),
                LocalDate.now(),
                null
        );
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    @DisplayName("deve criar um veículo quando placa e chassi não existirem no tenant")
    void deveCriarVeiculo() {
        Veiculo veiculo = new Veiculo();
        veiculo.setPlaca("ABC1234");
        
        VeiculoResponse response = VeiculoResponse.builder().placa("ABC1234").build();

        when(veiculoRepository.existsByPlacaAndTenantIdAndDeletedAtIsNull(anyString(), any())).thenReturn(false);
        when(veiculoRepository.existsByChassiAndTenantIdAndDeletedAtIsNull(anyString(), any())).thenReturn(false);
        
        when(veiculoMapper.toEntity(any())).thenReturn(veiculo);
        when(veiculoRepository.save(any())).thenAnswer(i -> {
            Veiculo v = i.getArgument(0);
            assertEquals(tenantId, v.getTenantId());
            assertEquals("ABC1234", v.getPlaca());
            return v;
        });
        when(veiculoMapper.toResponse(any())).thenReturn(response);

        VeiculoResponse result = veiculoService.criar(request);

        assertNotNull(result);
        assertEquals("ABC1234", result.getPlaca());
        verify(veiculoRepository).save(any(Veiculo.class));
    }

    @Test
    @DisplayName("deve lançar erro se placa já existir no tenant")
    void deveLancarErroSePlacaExistir() {
        Veiculo veiculoExistente = new Veiculo();
        veiculoExistente.setId(UUID.randomUUID());
        veiculoExistente.setPlaca("ABC1234");
        veiculoExistente.setTenantId(tenantId);
        
        Page<Veiculo> pageResult = new PageImpl<>(Collections.singletonList(veiculoExistente));

        when(veiculoRepository.existsByPlacaAndTenantIdAndDeletedAtIsNull("ABC1234", tenantId)).thenReturn(true);
        when(veiculoRepository.findByTenantIdAndDeletedAtIsNull(eq(tenantId), any(Pageable.class))).thenReturn(pageResult);

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> veiculoService.criar(request)
        );

        assertEquals("Placa já cadastrada na frota", exception.getMessage());
        verify(veiculoRepository, never()).save(any());
    }

    @Test
    @DisplayName("não deve permitir excluir veículo se estiver alugado")
    void naoDeveExcluirVeiculoLocado() {
        UUID veiculoId = UUID.randomUUID();
        UUID userId = UUID.randomUUID();

        Veiculo veiculo = new Veiculo();
        veiculo.setId(veiculoId);
        veiculo.setTenantId(tenantId);
        veiculo.setStatus(StatusVeiculo.LOCADO);

        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculoId, tenantId)).thenReturn(Optional.of(veiculo));

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> veiculoService.excluir(veiculoId, userId)
        );

        assertEquals("Não é possível excluir um veículo que esteja alugado ou reservado", exception.getMessage());
        verify(veiculoRepository, never()).save(any());
    }

    @Test
    @DisplayName("deve permitir excluir veículo disponível")
    void deveExcluirVeiculoDisponivel() {
        UUID veiculoId = UUID.randomUUID();
        UUID userId = UUID.randomUUID();

        Veiculo veiculo = new Veiculo();
        veiculo.setId(veiculoId);
        veiculo.setTenantId(tenantId);
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);

        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculoId, tenantId)).thenReturn(Optional.of(veiculo));

        veiculoService.excluir(veiculoId, userId);

        assertTrue(veiculo.isDeleted());
        assertEquals(userId, veiculo.getDeletedBy());
        verify(veiculoRepository).save(veiculo);
    }
}
