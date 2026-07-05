package com.locadora.configuracao.mapper;

import com.locadora.configuracao.dto.ConfiguracaoEmpresaDTO;
import com.locadora.configuracao.entity.ConfiguracaoEmpresa;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface ConfiguracaoEmpresaMapper {

    ConfiguracaoEmpresaDTO toDto(ConfiguracaoEmpresa entity);

    @Mapping(target = "id", ignore = true)
    ConfiguracaoEmpresa toEntity(ConfiguracaoEmpresaDTO dto);

    @Mapping(target = "id", ignore = true)
    void updateEntity(ConfiguracaoEmpresaDTO dto, @MappingTarget ConfiguracaoEmpresa entity);
}
