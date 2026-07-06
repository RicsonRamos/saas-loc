package com.locadora.alerta.service;

import com.locadora.alerta.dto.AlertaResponse;
import com.locadora.alerta.entity.Alerta;
import com.locadora.alerta.entity.TipoAlerta;
import com.locadora.alerta.repository.AlertaRepository;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.repository.DocumentoVeiculoRepository;
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
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class AlertaServiceTest {

    @Mock private AlertaRepository repository;
    @Mock private ClienteRepository clienteRepository;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private DocumentoVeiculoRepository documentoVeiculoRepository;
    @InjectMocks private AlertaService service;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private Alerta alerta;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        alerta = new Alerta();
        alerta.setId(UUID.randomUUID());
        alerta.setTipo(TipoAlerta.CNH);
        alerta.setTitulo("CNH Expirando");
        alerta.setDescricao("Vence em breve");
        alerta.setLido(false);
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    @Test
    void deveObterAlertasPendentes() {
        when(repository.findByTenantIdAndLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc(TENANT_ID)).thenReturn(List.of(alerta));

        List<AlertaResponse> response = service.obterPendentes();

        assertFalse(response.isEmpty());
        assertEquals(1, response.size());
        assertEquals("CNH Expirando", response.getFirst().getTitulo());
    }

    @Test
    void deveMarcarComoLidoComSucesso() {
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(alerta.getId(), TENANT_ID)).thenReturn(Optional.of(alerta));

        service.marcarComoLido(alerta.getId());

        assertTrue(alerta.getLido());
        verify(repository).save(alerta);
    }

    @Test
    void deveLancarExcecaoAoMarcarComoLidoAlertaInexistente() {
        UUID id = UUID.randomUUID();
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(id, TENANT_ID)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> service.marcarComoLido(id));
    }

    @Test
    void deveCriarAlertaSeNaoExistirPendente() {
        UUID clienteId = UUID.randomUUID();
        when(repository.existsByTipoAndEntidadeIdAndLidoFalseAndTenantIdAndDeletedAtIsNull(TipoAlerta.CNH, clienteId, TENANT_ID)).thenReturn(false);

        service.criarAlerta(TipoAlerta.CNH, "Título", "Descrição", clienteId);

        verify(repository).save(any(Alerta.class));
    }

    @Test
    void naoDeveCriarAlertaSeJaExistirPendente() {
        UUID clienteId = UUID.randomUUID();
        when(repository.existsByTipoAndEntidadeIdAndLidoFalseAndTenantIdAndDeletedAtIsNull(TipoAlerta.CNH, clienteId, TENANT_ID)).thenReturn(true);

        service.criarAlerta(TipoAlerta.CNH, "Título", "Descrição", clienteId);

        verify(repository, never()).save(any(Alerta.class));
    }
}
