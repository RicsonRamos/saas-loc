package com.locadora.contrato.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.contrato.dto.ChecklistRequest;
import com.locadora.contrato.dto.ChecklistResponse;
import com.locadora.contrato.entity.Checklist;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.TipoChecklist;
import com.locadora.contrato.mapper.ChecklistMapper;
import com.locadora.contrato.repository.ChecklistRepository;
import com.locadora.contrato.repository.ContratoRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;


@Service
public class ChecklistService {

    private static final Logger log = LoggerFactory.getLogger(ChecklistService.class);

    private final ChecklistRepository repository;
    private final ChecklistMapper mapper;
    private final ContratoRepository contratoRepository;
    private final ObjectMapper objectMapper;

    public ChecklistService(ChecklistRepository repository,
                            ChecklistMapper mapper,
                            ContratoRepository contratoRepository,
                            ObjectMapper objectMapper) {
        this.repository = repository;
        this.mapper = mapper;
        this.contratoRepository = contratoRepository;
        this.objectMapper = objectMapper;
    }

    @Transactional
    public ChecklistResponse salvar(ChecklistRequest request) {
        Contrato contrato = contratoRepository.findByIdAndDeletedAtIsNull(request.getContratoId())
                .orElseThrow(() -> new ResourceNotFoundException("Contrato", "id", request.getContratoId()));

        // Verifica se já existe um checklist desse tipo para este contrato
        repository.findByContratoIdAndTipoAndDeletedAtIsNull(contrato.getId(), request.getTipo())
                .ifPresent(existing -> {
                    throw new BusinessException("Já existe um checklist de " + request.getTipo() + " para este contrato.");
                });

        Checklist checklist = mapper.toEntity(request);
        checklist.setContrato(contrato);

        checklist = repository.save(checklist);
        log.info("Checklist de {} salvo para o contrato {}.", request.getTipo(), contrato.getId());
        return mapper.toResponse(checklist);
    }

    @Transactional(readOnly = true)
    public List<ChecklistResponse> buscarPorContrato(UUID contratoId) {
        return repository.findByContratoIdAndDeletedAtIsNull(contratoId).stream()
                .map(mapper::toResponse)
                .toList();
    }

    /**
     * Compara automaticamente os itens do checklist de Retirada com o de Devolução.
     * Retorna um mapa contendo as divergências.
     */
    @Transactional(readOnly = true)
    public Map<String, String> compararRetiradaEDevolucao(UUID contratoId) {
        Checklist retirada = repository.findByContratoIdAndTipoAndDeletedAtIsNull(contratoId, TipoChecklist.RETIRADA)
                .orElseThrow(() -> new BusinessException("Checklist de RETIRADA não encontrado para este contrato."));

        Checklist devolucao = repository.findByContratoIdAndTipoAndDeletedAtIsNull(contratoId, TipoChecklist.DEVOLUCAO)
                .orElseThrow(() -> new BusinessException("Checklist de DEVOLUÇÃO não encontrado para este contrato."));

        Map<String, String> divergencias = new HashMap<>();

        try {
            List<Map<String, String>> itensRetirada = objectMapper.readValue(
                    retirada.getItensJson(), new TypeReference<List<Map<String, String>>>() {});
            List<Map<String, String>> itensDevolucao = objectMapper.readValue(
                    devolucao.getItensJson(), new TypeReference<List<Map<String, String>>>() {});

            Map<String, String> mapaRetirada = converterParaMapa(itensRetirada);
            Map<String, String> mapaDevolucao = converterParaMapa(itensDevolucao);

            for (Map.Entry<String, String> entry : mapaRetirada.entrySet()) {
                String item = entry.getKey();
                String estadoRetirada = entry.getValue();
                String estadoDevolucao = mapaDevolucao.get(item);

                if (estadoDevolucao == null) {
                    divergencias.put(item, "Item ausente na devolução (Retirada: " + estadoRetirada + ")");
                } else if (!estadoRetirada.equalsIgnoreCase(estadoDevolucao)) {
                    divergencias.put(item, "Divergência: Retirada = " + estadoRetirada + " | Devolução = " + estadoDevolucao);
                }
            }

        } catch (Exception e) {
            log.error("Erro ao comparar checklists do contrato {}: {}", contratoId, e.getMessage());
            throw new BusinessException("Não foi possível processar e comparar os dados dos checklists.");
        }

        return divergencias;
    }

    private Map<String, String> converterParaMapa(List<Map<String, String>> listaItens) {
        Map<String, String> mapa = new HashMap<>();
        for (Map<String, String> map : listaItens) {
            String item = map.get("item");
            String estado = map.get("estado");
            if (item != null && estado != null) {
                mapa.put(item.trim(), estado.trim());
            }
        }
        return mapa;
    }
}
