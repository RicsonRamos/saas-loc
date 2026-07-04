package com.locadora.cliente.service;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.entity.TipoCliente;
import com.locadora.cliente.mapper.ClienteMapper;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.BusinessException;
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

import java.util.Collections;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Testes do ClienteService.
 */
@ExtendWith(MockitoExtension.class)
class ClienteServiceTest {

    @Mock
    private ClienteRepository clienteRepository;

    @Mock
    private ClienteMapper clienteMapper;

    @InjectMocks
    private ClienteService clienteService;

    private UUID tenantId;
    private ClienteRequest request;

    @BeforeEach
    void setUp() {
        tenantId = UUID.randomUUID();
        TenantContext.setTenantId(tenantId);

        request = new ClienteRequest(
                "Locatário da Silva",
                TipoCliente.PESSOA_FISICA,
                "123.456.789-10",
                "locatario@email.com",
                "11999999999",
                "12345678900",
                null,
                "12345-678",
                "Rua A",
                "123",
                "",
                "Bairro",
                "São Paulo",
                "SP",
                null,
                null
        );
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    @DisplayName("deve limpar o documento (CPF/CNPJ) ao criar cliente e garantir tenant")
    void deveLimparDocumentoECriarCliente() {
        Cliente cliente = new Cliente();
        ClienteResponse response = ClienteResponse.builder().documento("12345678910").build();

        when(clienteRepository.existsByDocumentoAndTenantIdAndDeletedAtIsNull(anyString(), eq(tenantId)))
                .thenReturn(false);
        when(clienteMapper.toEntity(any())).thenReturn(cliente);
        when(clienteRepository.save(any())).thenAnswer(i -> {
            Cliente saved = i.getArgument(0);
            assertEquals(tenantId, saved.getTenantId());
            assertEquals("12345678910", saved.getDocumento());
            return saved;
        });
        when(clienteMapper.toResponse(any())).thenReturn(response);

        ClienteResponse result = clienteService.criar(request);

        assertNotNull(result);
        assertEquals("12345678910", result.getDocumento());
        verify(clienteRepository).save(any(Cliente.class));
    }

    @Test
    @DisplayName("deve rejeitar cadastro se documento já existir no tenant")
    void deveRejeitarDocumentoDuplicado() {
        Cliente clienteExistente = new Cliente();
        clienteExistente.setId(UUID.randomUUID());
        clienteExistente.setDocumento("12345678910");
        clienteExistente.setTenantId(tenantId);
        
        Page<Cliente> pageResult = new PageImpl<>(Collections.singletonList(clienteExistente));

        when(clienteRepository.existsByDocumentoAndTenantIdAndDeletedAtIsNull("12345678910", tenantId))
                .thenReturn(true);
        when(clienteRepository.findByTenantIdAndDeletedAtIsNull(eq(tenantId), any(Pageable.class)))
                .thenReturn(pageResult);

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> clienteService.criar(request)
        );

        assertEquals("Já existe um cliente cadastrado com este documento (CPF/CNPJ).", exception.getMessage());
        verify(clienteRepository, never()).save(any());
    }
}
