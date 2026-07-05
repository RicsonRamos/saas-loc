package com.locadora.reserva.mapper;

import com.locadora.reserva.dto.ReservaRequest;
import com.locadora.reserva.dto.ReservaResponse;
import com.locadora.reserva.entity.Reserva;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring")
public interface ReservaMapper {

    @Mapping(target = "clienteId", source = "cliente.id")
    @Mapping(target = "clienteNome", source = "cliente.nome")
    @Mapping(target = "clienteTelefone", source = "cliente.telefone")
    @Mapping(target = "veiculoId", source = "veiculo.id")
    @Mapping(target = "veiculoPlaca", source = "veiculo.placa")
    @Mapping(target = "veiculoModelo", source = "veiculo.modelo")
    ReservaResponse toResponse(Reserva entity);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "cliente", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    @Mapping(target = "status", ignore = true)
    Reserva toEntity(ReservaRequest request);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "cliente", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    void updateEntity(ReservaRequest request, @MappingTarget Reserva entity);
}
