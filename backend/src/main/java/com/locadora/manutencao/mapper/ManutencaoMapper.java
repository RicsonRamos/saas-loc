package com.locadora.manutencao.mapper;

import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoResponse;
import com.locadora.manutencao.entity.Manutencao;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface ManutencaoMapper {

    @Mapping(target = "veiculoId", source = "veiculo.id")
    @Mapping(target = "veiculoPlaca", source = "veiculo.placa")
    ManutencaoResponse toResponse(Manutencao manutencao);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "tenantId", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    @Mapping(target = "kmManutencao", ignore = true)
    @Mapping(target = "dataFim", ignore = true)
    @Mapping(target = "custo", ignore = true)
    @Mapping(target = "concluida", ignore = true)
    Manutencao toEntity(ManutencaoRequest request);
}
