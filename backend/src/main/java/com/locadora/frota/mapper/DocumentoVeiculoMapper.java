package com.locadora.frota.mapper;

import com.locadora.frota.dto.DocumentoVeiculoRequest;
import com.locadora.frota.dto.DocumentoVeiculoResponse;
import com.locadora.frota.entity.DocumentoVeiculo;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface DocumentoVeiculoMapper {

    @Mapping(target = "veiculoId", source = "veiculo.id")
    @Mapping(target = "veiculoPlaca", source = "veiculo.placa")
    @Mapping(target = "veiculoModelo", source = "veiculo.modelo")
    DocumentoVeiculoResponse toResponse(DocumentoVeiculo entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    DocumentoVeiculo toEntity(DocumentoVeiculoRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    void updateEntity(DocumentoVeiculoRequest request, @MappingTarget DocumentoVeiculo entity);
}
