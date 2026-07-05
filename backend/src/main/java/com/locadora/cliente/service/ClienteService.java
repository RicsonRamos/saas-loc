package com.locadora.cliente.service;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.mapper.ClienteMapper;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

import com.locadora.shared.tenant.TenantContext;

/**
 * Serviço de Clientes — Multi-Tenant.
 */
@Service
public class ClienteService {

    private static final Logger log = LoggerFactory.getLogger(ClienteService.class);

    private final ClienteRepository clienteRepository;
    private final ClienteMapper clienteMapper;

    public ClienteService(ClienteRepository clienteRepository, ClienteMapper clienteMapper) {
        this.clienteRepository = clienteRepository;
        this.clienteMapper = clienteMapper;
    }

    @Transactional
    public ClienteResponse criar(ClienteRequest request) {
        String documentoLimpo = limparDocumento(request.getDocumento());
        validarDocumentoUnico(documentoLimpo, null);

        Cliente cliente = clienteMapper.toEntity(request);
        cliente.setDocumento(documentoLimpo);

        cliente = clienteRepository.save(cliente);
        log.info("Cliente criado com sucesso: {}", cliente.getDocumento());

        return clienteMapper.toResponse(cliente);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ClienteResponse> listar(Pageable pageable) {
        Page<Cliente> page = clienteRepository.findByTenantIdAndDeletedAtIsNull(TenantContext.getTenantId(), pageable);
        List<ClienteResponse> data = page.getContent().stream()
                .map(clienteMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public ClienteResponse buscarPorId(UUID id) {
        return clienteMapper.toResponse(obterClientePorId(id));
    }

    @Transactional
    public ClienteResponse atualizar(UUID id, ClienteRequest request) {
        Cliente cliente = obterClientePorId(id);

        String documentoLimpo = limparDocumento(request.getDocumento());
        validarDocumentoUnico(documentoLimpo, cliente.getId());

        clienteMapper.updateEntity(request, cliente);
        cliente.setDocumento(documentoLimpo);

        cliente = clienteRepository.save(cliente);
        log.info("Cliente atualizado: {}", cliente.getDocumento());

        return clienteMapper.toResponse(cliente);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        Cliente cliente = obterClientePorId(id);
        cliente.softDelete(currentUserId);
        clienteRepository.save(cliente);
        log.info("Cliente excluído (soft delete): {}", cliente.getDocumento());
    }

    private Cliente obterClientePorId(UUID id) {
        return clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, TenantContext.getTenantId())
                .orElseThrow(() -> new ResourceNotFoundException("Cliente", "id", id));
    }

    private String limparDocumento(String documento) {
        if (documento == null) return null;
        return documento.replaceAll("[^0-9]", "");
    }

    private void validarDocumentoUnico(String documento, UUID clienteIdIgnorado) {
        UUID tenantId = TenantContext.getTenantId();
        if (clienteRepository.existsByDocumentoAndTenantIdAndDeletedAtIsNull(documento, tenantId)) {
            // Verifica se o documento pertence ao próprio cliente sendo atualizado
            clienteRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                    .stream()
                    .filter(c -> c.getDocumento().equals(documento))
                    .findFirst()
                    .ifPresent(existente -> {
                        if (!existente.getId().equals(clienteIdIgnorado)) {
                            throw new BusinessException("Já existe um cliente cadastrado com este documento (CPF/CNPJ).");
                        }
                    });
        }
    }
}
