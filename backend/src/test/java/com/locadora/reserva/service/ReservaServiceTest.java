package com.locadora.reserva.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.BusinessException;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.reserva.dto.ReservaRequest;
import com.locadora.reserva.dto.ReservaResponse;
import com.locadora.reserva.entity.OrigemReserva;
import com.locadora.reserva.entity.Reserva;
import com.locadora.reserva.mapper.ReservaMapper;
import com.locadora.reserva.repository.ReservaRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

/**
 * Testes unitários do serviço de reservas.
 * Valida criação com sucesso e rejeição quando há conflito de datas.
 */
@ExtendWith(MockitoExtension.class)
class ReservaServiceTest {

    @Mock private ReservaRepository repository;
    @Mock private ReservaMapper mapper;
    @Mock private ClienteRepository clienteRepository;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private ContratoRepository contratoRepository;
    @InjectMocks private ReservaService service;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private Cliente cliente;
    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        cliente = new Cliente();
        cliente.setId(UUID.randomUUID());

        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    /**
     * Cenário feliz: criação de reserva sem conflitos deve retornar response não-nulo.
     */
    @Test
    void deveCriarReservaComSucesso() {
        LocalDateTime inicio = LocalDateTime.now().plusDays(1);
        LocalDateTime fim = LocalDateTime.now().plusDays(5);

        // Usa @Builder (ReservaRequest tem @Data + @Builder)
        ReservaRequest request = ReservaRequest.builder()
                .clienteId(cliente.getId())
                .veiculoId(veiculo.getId())
                .categoria("SUV")
                .dataInicio(inicio)
                .dataFim(fim)
                .origem(OrigemReserva.WHATSAPP)
                .build();

        when(clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(cliente.getId(), TENANT_ID))
                .thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TENANT_ID))
                .thenReturn(Optional.of(veiculo));
        // existsConflict agora espera 5 parâmetros: veiculoId, inicio, fim, reservaId, tenantId
        when(repository.existsConflict(eq(veiculo.getId()), eq(inicio), eq(fim), isNull(), eq(TENANT_ID)))
                .thenReturn(false);
        when(mapper.toEntity(request)).thenReturn(new Reserva());
        when(repository.save(any())).thenReturn(new Reserva());
        when(mapper.toResponse(any())).thenReturn(new ReservaResponse());

        ReservaResponse response = service.criar(request);
        assertNotNull(response);
    }

    /**
     * Regra de negócio: conflito de período em veículo deve ser rejeitado.
     */
    @Test
    void naoDeveCriarReservaSeHouverConflito() {
        LocalDateTime inicio = LocalDateTime.now().plusDays(1);
        LocalDateTime fim = LocalDateTime.now().plusDays(5);

        ReservaRequest request = ReservaRequest.builder()
                .clienteId(cliente.getId())
                .veiculoId(veiculo.getId())
                .categoria("SUV")
                .dataInicio(inicio)
                .dataFim(fim)
                .origem(OrigemReserva.WHATSAPP)
                .build();

        when(clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(cliente.getId(), TENANT_ID))
                .thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TENANT_ID))
                .thenReturn(Optional.of(veiculo));
        when(repository.existsConflict(eq(veiculo.getId()), eq(inicio), eq(fim), isNull(), eq(TENANT_ID)))
                .thenReturn(true);

        assertThrows(BusinessException.class, () -> service.criar(request));
    }
}
