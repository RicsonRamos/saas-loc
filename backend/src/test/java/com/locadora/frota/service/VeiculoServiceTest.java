package com.locadora.frota.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.dto.VeiculoRequest;
import com.locadora.frota.dto.VeiculoResponse;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.VeiculoMapper;
import com.locadora.frota.repository.VeiculoRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

/**
 * Testes unitários do serviço de veículos.
 * Valida regras de criação e exclusão segura (soft delete) de veículos da frota.
 */
@ExtendWith(MockitoExtension.class)
class VeiculoServiceTest {

    @Mock private VeiculoRepository veiculoRepository;
    @Mock private VeiculoMapper veiculoMapper;
    @InjectMocks private VeiculoService veiculoService;

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

    /**
     * Cenário feliz: criação de veículo com dados válidos deve retornar um response não-nulo.
     */
    @Test
    void deveCriarVeiculoComSucesso() {
        // Usa AllArgsConstructor — o DTO não possui setters
        VeiculoRequest request = new VeiculoRequest(
                "ABC-1234", "CHASSI123", null, "Toyota", "Corolla",
                2024, 2024, "Prata", 0, StatusVeiculo.DISPONIVEL,
                null, null, null, null, null, null, null, null,
                null, null, null, null, null, null
        );

        Veiculo veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setPlaca("ABC-1234");
        veiculo.setChassi("CHASSI123");

        when(veiculoMapper.toEntity(request)).thenReturn(veiculo);
        when(veiculoRepository.save(any())).thenReturn(veiculo);
        when(veiculoMapper.toResponse(veiculo)).thenReturn(new VeiculoResponse());

        VeiculoResponse response = veiculoService.criar(request);
        assertNotNull(response);
    }

    /**
     * Regra de negócio: veículo LOCADO não pode ser excluído (soft delete).
     */
    @Test
    void naoDeveExcluirVeiculoLocado() {
        UUID id = UUID.randomUUID();
        Veiculo veiculo = new Veiculo();
        veiculo.setId(id);
        veiculo.setStatus(StatusVeiculo.LOCADO);

        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, TENANT_ID))
                .thenReturn(Optional.of(veiculo));

        assertThrows(BusinessException.class, () -> veiculoService.excluir(id, UUID.randomUUID()));
    }

    /**
     * Quando não encontrar o veículo no banco deve lançar ResourceNotFoundException.
     */
    @Test
    void deveLancarExcecaoAoBuscarVeiculoInexistente() {
        UUID id = UUID.randomUUID();
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, TENANT_ID))
                .thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> veiculoService.buscarPorId(id));
    }
}
