package com.locadora.empresa.mapper;

import com.locadora.empresa.dto.EmpresaRequest;
import com.locadora.empresa.dto.EmpresaResponse;
import com.locadora.empresa.entity.Empresa;
import org.mapstruct.Mapper;
import org.mapstruct.MappingTarget;

/**
 * Mapper de Empresa usando MapStruct conforme 04-stack-tecnologica.md.
 */
@Mapper(componentModel = "spring")
public interface EmpresaMapper {

    EmpresaResponse toResponse(Empresa empresa);

    Empresa toEntity(EmpresaRequest request);

    void updateEntity(EmpresaRequest request, @MappingTarget Empresa empresa);
}
