package com.locadora.contrato.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.BusinessException;
import com.locadora.contrato.dto.ContratoRequest;
import com.locadora.contrato.dto.ContratoResponse;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import com.locadora.contrato.mapper.ContratoMapper;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
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

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ContratoServiceTest {

    @Mock private ContratoRepository contratoRepository;
    @Mock private ContratoMapper contratoMapper;
    @Mock private ClienteRepository clienteRepository;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private FinanceiroService financeiroService;
    @InjectMocks private ContratoService contratoService;

    private Cliente cliente;
    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        cliente = new Cliente();
        cliente.setId(UUID.randomUUID());

        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculo.setQuilometragem(10000);
    }

    @Test
    void naoDeveAbrirContratoSeVeiculoIndisponivel() {
        veiculo.setStatus(StatusVeiculo.LOCADO);

        ContratoRequest request = new ContratoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setClienteId(cliente.getId());

        when(clienteRepository.findByIdAndDeletedAtIsNull(cliente.getId())).thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));

        assertThrows(BusinessException.class, () -> contratoService.abrirContrato(request));
    }

    @Test
    void deveAbrirContratoEAlterarStatusVeiculo() {
        ContratoRequest request = new ContratoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setClienteId(cliente.getId());
        request.setDataPrevistaDevolucao(LocalDate.now().plusDays(5));
        request.setValorDiaria(new BigDecimal("100.00"));

        Contrato contratoSalvo = new Contrato();
        contratoSalvo.setId(UUID.randomUUID());
        contratoSalvo.setStatus(StatusContrato.ATIVO);

        when(clienteRepository.findByIdAndDeletedAtIsNull(cliente.getId())).thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));
        when(contratoMapper.toEntity(request)).thenReturn(new Contrato());
        when(contratoRepository.save(any(Contrato.class))).thenReturn(contratoSalvo);
        when(contratoMapper.toResponse(any())).thenReturn(new ContratoResponse());

        contratoService.abrirContrato(request);

        verify(contratoRepository).save(any(Contrato.class));
    }
}
