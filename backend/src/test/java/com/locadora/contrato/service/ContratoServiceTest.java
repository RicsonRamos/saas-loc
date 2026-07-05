package com.locadora.contrato.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.BusinessException;
import com.locadora.contrato.dto.ContratoRequest;
import com.locadora.contrato.dto.DevolucaoRequest;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
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
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ContratoServiceTest {

    @Mock
    private ContratoRepository contratoRepository;

    @Mock
    private ClienteRepository clienteRepository;

    @Mock
    private VeiculoRepository veiculoRepository;

    @Mock
    private FinanceiroService financeiroService;

    @InjectMocks
    private ContratoService contratoService;

    private final UUID tenantId = UUID.randomUUID();
    private Cliente cliente;
    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        TenantContext.setTenantId(tenantId);
        
        cliente = new Cliente();
        cliente.setId(UUID.randomUUID());
        cliente.setTenantId(tenantId);
        
        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setTenantId(tenantId);
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculo.setQuilometragemAtual(10000);
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void naoDeveAbrirContratoSeVeiculoIndisponivel() {
        veiculo.setStatus(StatusVeiculo.LOCADO);
        
        ContratoRequest request = new ContratoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setClienteId(cliente.getId());
        
        when(clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(cliente.getId(), tenantId))
                .thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), tenantId))
                .thenReturn(Optional.of(veiculo));

        assertThrows(BusinessException.class, () -> contratoService.abrirContrato(request));
    }

    @Test
    void deveAbrirContratoAlterandoStatusDoVeiculo() {
        ContratoRequest request = new ContratoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setClienteId(cliente.getId());
        request.setDataPrevistaDevolucao(LocalDate.now().plusDays(5));
        request.setValorDiaria(new BigDecimal("100.00"));
        
        when(clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(cliente.getId(), tenantId))
                .thenReturn(Optional.of(cliente));
        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), tenantId))
                .thenReturn(Optional.of(veiculo));
                
        Contrato contratoSalvo = new Contrato();
        contratoSalvo.setId(UUID.randomUUID());
        contratoSalvo.setStatus(StatusContrato.ABERTO);
        when(contratoRepository.save(any(Contrato.class))).thenReturn(contratoSalvo);

        contratoService.abrirContrato(request);
        
        assertEquals(StatusVeiculo.LOCADO, veiculo.getStatus());
        verify(contratoRepository).save(any(Contrato.class));
    }
}
