package com.locadora.usuario.mapper;

import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.dto.UsuarioUpdateRequest;
import com.locadora.usuario.entity.Usuario;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface UsuarioMapper {

    UsuarioResponse toResponse(Usuario usuario);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "ativo", constant = "true")
    @Mapping(target = "senha", ignore = true)
    Usuario toEntity(UsuarioRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "email", ignore = true)
    @Mapping(target = "senha", ignore = true)
    void updateEntity(UsuarioUpdateRequest request, @MappingTarget Usuario usuario);
}
