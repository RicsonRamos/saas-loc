package com.locadora.financeiro.mapper;

import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.dto.LancamentoResponse;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring")
public interface LancamentoMapper {

    @Mapping(target = "veiculoId", source = "veiculo.id")
    @Mapping(target = "veiculoPlaca", source = "veiculo.placa")
    @Mapping(target = "contratoId", source = "contrato.id")
    LancamentoResponse toResponse(LancamentoFinanceiro lancamento);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "tenantId", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    @Mapping(target = "contrato", ignore = true)
    LancamentoFinanceiro toEntity(LancamentoRequest request);
}
