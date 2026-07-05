package com.locadora.cliente.mapper;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.entity.Cliente;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface ClienteMapper {

    ClienteResponse toResponse(Cliente cliente);

    @Mapping(target = "id", ignore = true)
    Cliente toEntity(ClienteRequest request);

    @Mapping(target = "id", ignore = true)
    void updateEntity(ClienteRequest request, @MappingTarget Cliente cliente);
}
