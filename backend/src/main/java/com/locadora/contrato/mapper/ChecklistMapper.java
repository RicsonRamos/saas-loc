package com.locadora.contrato.mapper;

import com.locadora.contrato.dto.ChecklistRequest;
import com.locadora.contrato.dto.ChecklistResponse;
import com.locadora.contrato.entity.Checklist;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface ChecklistMapper {

    @Mapping(target = "contratoId", source = "contrato.id")
    ChecklistResponse toResponse(Checklist entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "contrato", ignore = true)
    Checklist toEntity(ChecklistRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "contrato", ignore = true)
    void updateEntity(ChecklistRequest request, @MappingTarget Checklist entity);
}
