package com.locadora.frota.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.dto.DocumentoVeiculoRequest;
import com.locadora.frota.dto.DocumentoVeiculoResponse;
import com.locadora.frota.entity.DocumentoVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.DocumentoVeiculoMapper;
import com.locadora.frota.repository.DocumentoVeiculoRepository;
import com.locadora.frota.repository.VeiculoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.UUID;


@Service
public class DocumentoVeiculoService {

    private static final Logger log = LoggerFactory.getLogger(DocumentoVeiculoService.class);

    private final DocumentoVeiculoRepository repository;
    private final DocumentoVeiculoMapper mapper;
    private final VeiculoRepository veiculoRepository;

    public DocumentoVeiculoService(DocumentoVeiculoRepository repository,
                                   DocumentoVeiculoMapper mapper,
                                   VeiculoRepository veiculoRepository) {
        this.repository = repository;
        this.mapper = mapper;
        this.veiculoRepository = veiculoRepository;
    }

    @Transactional
    public DocumentoVeiculoResponse criar(DocumentoVeiculoRequest request) {
        Veiculo veiculo = veiculoRepository.findByIdAndDeletedAtIsNull(request.getVeiculoId())
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

        // Valida se já existe um documento ativo do mesmo tipo
        repository.findByVeiculoIdAndTipoAndDeletedAtIsNull(veiculo.getId(), request.getTipo())
                .ifPresent(existing -> {
                    throw new BusinessException("Já existe um documento de " + request.getTipo() + " ativo para este veículo.");
                });

        DocumentoVeiculo documento = mapper.toEntity(request);
        documento.setVeiculo(veiculo);

        documento = repository.save(documento);
        log.info("Documento de {} cadastrado para veículo {}", request.getTipo(), veiculo.getPlaca());

        return mapper.toResponse(documento);
    }

    @Transactional
    public DocumentoVeiculoResponse atualizar(UUID id, DocumentoVeiculoRequest request) {
        DocumentoVeiculo documento = repository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("DocumentoVeiculo", "id", id));

        mapper.updateEntity(request, documento);
        documento = repository.save(documento);
        log.info("Documento {} atualizado com sucesso.", id);

        return mapper.toResponse(documento);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        DocumentoVeiculo documento = repository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("DocumentoVeiculo", "id", id));

        documento.softDelete(currentUserId);
        repository.save(documento);
        log.info("Documento {} excluído logicamente.", id);
    }

    @Transactional(readOnly = true)
    public List<DocumentoVeiculoResponse> listarPorVeiculo(UUID veiculoId) {
        return repository.findByVeiculoIdAndDeletedAtIsNull(veiculoId).stream()
                .map(mapper::toResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public DocumentoVeiculoResponse buscarPorId(UUID id) {
        DocumentoVeiculo documento = repository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("DocumentoVeiculo", "id", id));
        return mapper.toResponse(documento);
    }
}
