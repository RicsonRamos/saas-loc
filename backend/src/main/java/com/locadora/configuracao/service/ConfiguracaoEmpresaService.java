package com.locadora.configuracao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.configuracao.dto.ConfiguracaoEmpresaDTO;
import com.locadora.configuracao.entity.ConfiguracaoEmpresa;
import com.locadora.configuracao.mapper.ConfiguracaoEmpresaMapper;
import com.locadora.configuracao.repository.ConfiguracaoEmpresaRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ConfiguracaoEmpresaService {

    private static final Logger log = LoggerFactory.getLogger(ConfiguracaoEmpresaService.class);

    private final ConfiguracaoEmpresaRepository repository;
    private final ConfiguracaoEmpresaMapper mapper;

    public ConfiguracaoEmpresaService(ConfiguracaoEmpresaRepository repository, ConfiguracaoEmpresaMapper mapper) {
        this.repository = repository;
        this.mapper = mapper;
    }

    @Transactional(readOnly = true)
    public ConfiguracaoEmpresaDTO obter() {
        ConfiguracaoEmpresa config = repository.findAll().stream()
                .findFirst()
                .orElseThrow(() -> new BusinessException("Configurações da empresa não encontradas."));
        return mapper.toDto(config);
    }

    @Transactional
    public ConfiguracaoEmpresaDTO atualizar(ConfiguracaoEmpresaDTO dto) {
        ConfiguracaoEmpresa config = repository.findAll().stream()
                .findFirst()
                .orElseThrow(() -> new BusinessException("Configurações da empresa não encontradas."));

        mapper.updateEntity(dto, config);
        config = repository.save(config);
        log.info("Configurações da empresa atualizadas por admin.");
        return mapper.toDto(config);
    }
}
