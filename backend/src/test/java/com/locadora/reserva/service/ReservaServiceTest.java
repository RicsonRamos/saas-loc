package com.locadora.reserva.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.BusinessException;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.reserva.dto.ReservaRequest;
import com.locadora.reserva.dto.ReservaResponse;
import com.locadora.reserva.entity.OrigemReserva;
import com.locadora.reserva.entity.Reserva;
import com.locadora.reserva.entity.StatusReserva;
import com.locadora.reserva.mapper.ReservaMapper;
import com.locadora.reserva.repository.ReservaRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ReservaServiceTest {

    @Mock private ReservaRepository repository;
    @Mock private ReservaMapper mapper;
    @Mock private ClienteRepository clienteRepository;
    @Mock private VeiculoRepository veiculoRepository;
    @InjectMocks private ReservaService service;

    private Cliente cliente;
    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        cliente = new Cliente();
        cliente.setId(UUID.randomUUID());

        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
    }

    @Test
    void deveCriarReservaComSucesso() {
        ReservaRequest request = new ReservaRequest();
        request.setClienteId(cliente.getId());
        request.setVeiculoId(veiculo.getId());
        request.setCategoria("SUV");
        request.setDataInicio(LocalDateTime.now().plusDays(1));
        request.setDataFim(LocalDateTime.now().plusDays(5));
        request.setOrigem(OrigemReserva.WHATSAPP);

        when(clienteRepository.findByIdAndDeletedAtIsNull(cliente.getId())).thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));
        when(repository.existsConflict(any(), any(), any(), any())).thenReturn(false);
        when(mapper.toEntity(request)).thenReturn(new Reserva());
        when(repository.save(any())).thenReturn(new Reserva());
        when(mapper.toResponse(any())).thenReturn(new ReservaResponse());

        ReservaResponse response = service.criar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveCriarReservaSeHouverConflito() {
        ReservaRequest request = new ReservaRequest();
        request.setClienteId(cliente.getId());
        request.setVeiculoId(veiculo.getId());
        request.setCategoria("SUV");
        request.setDataInicio(LocalDateTime.now().plusDays(1));
        request.setDataFim(LocalDateTime.now().plusDays(5));

        when(clienteRepository.findByIdAndDeletedAtIsNull(cliente.getId())).thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));
        when(repository.existsConflict(any(), any(), any(), any())).thenReturn(true);

        assertThrows(BusinessException.class, () -> service.criar(request));
    }
}
