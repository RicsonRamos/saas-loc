package com.locadora.configuracao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.configuracao.dto.ConfiguracaoEmpresaDTO;
import com.locadora.configuracao.entity.ConfiguracaoEmpresa;
import com.locadora.configuracao.mapper.ConfiguracaoEmpresaMapper;
import com.locadora.configuracao.repository.ConfiguracaoEmpresaRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ConfiguracaoEmpresaServiceTest {

    @Mock private ConfiguracaoEmpresaRepository repository;
    @Mock private ConfiguracaoEmpresaMapper mapper;
    @InjectMocks private ConfiguracaoEmpresaService service;

    @Test
    void deveObterConfiguracaoComSucesso() {
        ConfiguracaoEmpresa config = new ConfiguracaoEmpresa();
        config.setNomeFantasia("Locadora Exemplo");

        when(repository.findAll()).thenReturn(List.of(config));
        when(mapper.toDto(config)).thenReturn(new ConfiguracaoEmpresaDTO());

        ConfiguracaoEmpresaDTO result = service.obter();
        assertNotNull(result);
    }

    @Test
    void deveLancarExcecaoSeNaoHouverConfiguracao() {
        when(repository.findAll()).thenReturn(List.of());
        assertThrows(BusinessException.class, () -> service.obter());
    }
}
