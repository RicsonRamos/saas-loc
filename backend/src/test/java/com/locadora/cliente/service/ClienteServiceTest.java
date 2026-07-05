package com.locadora.cliente.service;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.mapper.ClienteMapper;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.ResourceNotFoundException;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ClienteServiceTest {

    @Mock private ClienteRepository clienteRepository;
    @Mock private ClienteMapper clienteMapper;
    @InjectMocks private ClienteService clienteService;

    @Test
    void deveCriarClienteComSucesso() {
        ClienteRequest request = new ClienteRequest();
        request.setNome("João Silva");
        request.setDocumento("123.456.789-00");

        Cliente cliente = new Cliente();
        cliente.setId(UUID.randomUUID());
        cliente.setDocumento("12345678900");

        when(clienteRepository.existsByDocumentoAndDeletedAtIsNull("12345678900")).thenReturn(false);
        when(clienteMapper.toEntity(request)).thenReturn(cliente);
        when(clienteRepository.save(any())).thenReturn(cliente);
        when(clienteMapper.toResponse(cliente)).thenReturn(new ClienteResponse());

        ClienteResponse response = clienteService.criar(request);
        assertNotNull(response);
    }

    @Test
    void deveLancarExcecaoAoBuscarClienteInexistente() {
        UUID id = UUID.randomUUID();
        when(clienteRepository.findByIdAndDeletedAtIsNull(id)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> clienteService.buscarPorId(id));
    }
}
