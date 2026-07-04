package com.locadora.frota.service;

import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.dto.VeiculoRequest;
import com.locadora.frota.dto.VeiculoResponse;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.VeiculoMapper;
import com.locadora.frota.repository.VeiculoRepository;
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
 * Serviço de Frota (Veículos).
 * Conforme 08-guard-rails.md: toda regra de negócio aqui.
 */
@Service
public class VeiculoService {

    private static final Logger log = LoggerFactory.getLogger(VeiculoService.class);

    private final VeiculoRepository veiculoRepository;
    private final VeiculoMapper veiculoMapper;

    public VeiculoService(VeiculoRepository veiculoRepository, VeiculoMapper veiculoMapper) {
        this.veiculoRepository = veiculoRepository;
        this.veiculoMapper = veiculoMapper;
    }

    @Transactional
    public VeiculoResponse criar(VeiculoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();

        validarUnicidade(request.getPlaca(), request.getChassi(), null, tenantId);

        Veiculo veiculo = veiculoMapper.toEntity(request);
        veiculo.setTenantId(tenantId);
        
        // Padronização: Placa sempre maiúscula
        veiculo.setPlaca(veiculo.getPlaca().toUpperCase());

        veiculo = veiculoRepository.save(veiculo);
        log.info("Veículo criado com sucesso: {} (Tenant: {})", veiculo.getPlaca(), tenantId);

        return veiculoMapper.toResponse(veiculo);
    }

    @Transactional(readOnly = true)
    public PagedResponse<VeiculoResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        
        Page<Veiculo> page = veiculoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<VeiculoResponse> data = page.getContent().stream()
                .map(veiculoMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public VeiculoResponse buscarPorId(UUID id) {
        return veiculoMapper.toResponse(obterVeiculoPorId(id));
    }

    @Transactional
    public VeiculoResponse atualizar(UUID id, VeiculoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();
        Veiculo veiculo = obterVeiculoPorId(id);

        validarUnicidade(request.getPlaca(), request.getChassi(), veiculo.getId(), tenantId);

        veiculoMapper.updateEntity(request, veiculo);
        veiculo.setPlaca(veiculo.getPlaca().toUpperCase());

        veiculo = veiculoRepository.save(veiculo);
        log.info("Veículo atualizado: {} (Tenant: {})", veiculo.getPlaca(), tenantId);

        return veiculoMapper.toResponse(veiculo);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        Veiculo veiculo = obterVeiculoPorId(id);

        // Regra de negócio: não é possível excluir veículo que esteja alugado ou reservado
        if (veiculo.getStatus() == StatusVeiculo.LOCADO || veiculo.getStatus() == StatusVeiculo.RESERVADO) {
            throw new BusinessException("Não é possível excluir um veículo que esteja alugado ou reservado");
        }

        veiculo.softDelete(currentUserId);
        veiculoRepository.save(veiculo);
        
        log.info("Veículo excluído (soft delete): {} (Tenant: {})", veiculo.getPlaca(), veiculo.getTenantId());
    }

    private Veiculo obterVeiculoPorId(UUID id) {
        UUID tenantId = TenantContext.requireTenantId();
        return veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", id));
    }

    private void validarUnicidade(String placa, String chassi, UUID veiculoIdIgnorado, UUID tenantId) {
        // Busca se existe e não é o próprio veículo sendo atualizado
        if (veiculoRepository.existsByPlacaAndTenantIdAndDeletedAtIsNull(placa, tenantId)) {
            // Como JPA não permite check and exclude facilmente no exists(), fazemos um contorno simples.
            // Para produção pesada, ideal seria um findByPlaca e comparar IDs.
            Veiculo existente = veiculoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                    .stream().filter(v -> v.getPlaca().equalsIgnoreCase(placa)).findFirst().orElse(null);
            
            if (existente != null && !existente.getId().equals(veiculoIdIgnorado)) {
                throw new BusinessException("Placa já cadastrada na frota");
            }
        }

        if (veiculoRepository.existsByChassiAndTenantIdAndDeletedAtIsNull(chassi, tenantId)) {
            Veiculo existente = veiculoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                    .stream().filter(v -> v.getChassi().equalsIgnoreCase(chassi)).findFirst().orElse(null);
                    
            if (existente != null && !existente.getId().equals(veiculoIdIgnorado)) {
                throw new BusinessException("Chassi já cadastrado na frota");
            }
        }
    }
}
