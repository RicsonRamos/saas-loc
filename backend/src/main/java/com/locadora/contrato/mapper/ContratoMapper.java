package com.locadora.contrato.mapper;

import com.locadora.contrato.dto.ContratoRequest;
import com.locadora.contrato.dto.ContratoResponse;
import com.locadora.contrato.entity.Contrato;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

/**
 * Interface MapStruct encarregada de transferir os dados das requisições para Entidades e vice-versa.
 */
@Mapper(componentModel = "spring")
public interface ContratoMapper {

    /**
     * Transforma a entidade num DTO seguro para o Frontend.
     * Mapeia os dados subjacentes das chaves estrangeiras.
     */
    @Mapping(target = "clienteId", source = "cliente.id")
    @Mapping(target = "clienteNome", source = "cliente.nome")
    @Mapping(target = "veiculoId", source = "veiculo.id")
    @Mapping(target = "veiculoPlaca", source = "veiculo.placa")
    ContratoResponse toResponse(Contrato contrato);

    /**
     * Transforma a Request na Entidade, ignorando os campos sensíveis e as entidades aninhadas,
     * as quais devem ser validadas e anexadas pelo Service posteriormente.
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "tenantId", ignore = true)
    @Mapping(target = "status", ignore = true)
    @Mapping(target = "kmInicial", ignore = true)
    @Mapping(target = "kmFinal", ignore = true)
    @Mapping(target = "kmExcedente", ignore = true)
    @Mapping(target = "dataDevolucao", ignore = true)
    @Mapping(target = "valorAdicional", ignore = true)
    @Mapping(target = "cliente", ignore = true)
    @Mapping(target = "veiculo", ignore = true)
    Contrato toEntity(ContratoRequest request);
}
