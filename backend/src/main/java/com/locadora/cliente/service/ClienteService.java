package com.locadora.cliente.service;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.mapper.ClienteMapper;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.shared.tenant.TenantContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;

/**
 * Serviço de Clientes.
 * Conforme 08-guard-rails.md: toda regra de negócio aqui.
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
        UUID tenantId = TenantContext.requireTenantId();

        String documentoLimpo = limparDocumento(request.getDocumento());
        validarUnicidade(documentoLimpo, null, tenantId);

        Cliente cliente = clienteMapper.toEntity(request);
        cliente.setTenantId(tenantId);
        cliente.setDocumento(documentoLimpo);

        cliente = clienteRepository.save(cliente);
        log.info("Cliente criado com sucesso: {} (Tenant: {})", cliente.getDocumento(), tenantId);

        return clienteMapper.toResponse(cliente);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ClienteResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        
        Page<Cliente> page = clienteRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
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
        UUID tenantId = TenantContext.requireTenantId();
        Cliente cliente = obterClientePorId(id);

        String documentoLimpo = limparDocumento(request.getDocumento());
        validarUnicidade(documentoLimpo, cliente.getId(), tenantId);

        clienteMapper.updateEntity(request, cliente);
        cliente.setDocumento(documentoLimpo);

        cliente = clienteRepository.save(cliente);
        log.info("Cliente atualizado: {} (Tenant: {})", cliente.getDocumento(), tenantId);

        return clienteMapper.toResponse(cliente);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        Cliente cliente = obterClientePorId(id);

        // TODO (EPIC 4): Validar se o cliente possui contratos ativos antes de permitir exclusão.
        // Como o módulo de Contratos ainda não existe, deixaremos um comentário.

        cliente.softDelete(currentUserId);
        clienteRepository.save(cliente);
        
        log.info("Cliente excluído (soft delete): {} (Tenant: {})", cliente.getDocumento(), cliente.getTenantId());
    }

    private Cliente obterClientePorId(UUID id) {
        UUID tenantId = TenantContext.requireTenantId();
        return clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Cliente", "id", id));
    }

    private String limparDocumento(String documento) {
        if (documento == null) return null;
        return documento.replaceAll("[^0-9]", "");
    }

    private void validarUnicidade(String documento, UUID clienteIdIgnorado, UUID tenantId) {
        if (clienteRepository.existsByDocumentoAndTenantIdAndDeletedAtIsNull(documento, tenantId)) {
            // Contorno simples para ignorar o próprio ID durante update
            Cliente existente = clienteRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                    .stream().filter(c -> c.getDocumento().equals(documento)).findFirst().orElse(null);
            
            if (existente != null && !existente.getId().equals(clienteIdIgnorado)) {
                throw new BusinessException("Já existe um cliente cadastrado com este documento (CPF/CNPJ).");
            }
        }
    }
}
