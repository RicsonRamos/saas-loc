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
 * Serviço de Frota (Veículos) — Multi-Tenant.
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
        validarUnicidade(request.getPlaca(), request.getChassi(), null);

        Veiculo veiculo = veiculoMapper.toEntity(request);
        veiculo.setPlaca(veiculo.getPlaca().toUpperCase());

        veiculo = veiculoRepository.save(veiculo);
        log.info("Veículo criado com sucesso: {}", veiculo.getPlaca());

        return veiculoMapper.toResponse(veiculo);
    }

    @Transactional(readOnly = true)
    public PagedResponse<VeiculoResponse> listar(Pageable pageable) {
        Page<Veiculo> page = veiculoRepository.findByTenantIdAndDeletedAtIsNull(TenantContext.getTenantId(), pageable);
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
        Veiculo veiculo = obterVeiculoPorId(id);
        validarUnicidade(request.getPlaca(), request.getChassi(), veiculo.getId());

        veiculoMapper.updateEntity(request, veiculo);
        veiculo.setPlaca(veiculo.getPlaca().toUpperCase());

        veiculo = veiculoRepository.save(veiculo);
        log.info("Veículo atualizado: {}", veiculo.getPlaca());

        return veiculoMapper.toResponse(veiculo);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        Veiculo veiculo = obterVeiculoPorId(id);

        if (veiculo.getStatus() == StatusVeiculo.LOCADO || veiculo.getStatus() == StatusVeiculo.RESERVADO) {
            throw new BusinessException("Não é possível excluir um veículo que esteja alugado ou reservado");
        }

        veiculo.softDelete(currentUserId);
        veiculoRepository.save(veiculo);
        log.info("Veículo excluído (soft delete): {}", veiculo.getPlaca());
    }

    private Veiculo obterVeiculoPorId(UUID id) {
        return veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, TenantContext.getTenantId())
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", id));
    }

    private void validarUnicidade(String placa, String chassi, UUID veiculoIdIgnorado) {
        if (existeOutroComPlaca(placa, veiculoIdIgnorado)) {
            throw new BusinessException("Placa já cadastrada na frota");
        }
        if (existeOutroComChassi(chassi, veiculoIdIgnorado)) {
            throw new BusinessException("Chassi já cadastrado na frota");
        }
    }

    private boolean existeOutroComPlaca(String placa, UUID idIgnorado) {
        UUID tenantId = TenantContext.getTenantId();
        return veiculoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                .stream()
                .filter(v -> v.getPlaca().equalsIgnoreCase(placa))
                .anyMatch(v -> !v.getId().equals(idIgnorado));
    }

    private boolean existeOutroComChassi(String chassi, UUID idIgnorado) {
        UUID tenantId = TenantContext.getTenantId();
        return veiculoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, Pageable.unpaged())
                .stream()
                .filter(v -> v.getChassi().equalsIgnoreCase(chassi))
                .anyMatch(v -> !v.getId().equals(idIgnorado));
    }
}
