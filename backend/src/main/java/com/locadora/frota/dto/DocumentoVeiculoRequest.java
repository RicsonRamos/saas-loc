package com.locadora.frota.dto;

import com.locadora.frota.entity.TipoDocumentoVeiculo;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DocumentoVeiculoRequest {

    @NotNull(message = "Veículo é obrigatório")
    private UUID veiculoId;

    @NotNull(message = "Tipo de documento é obrigatório")
    private TipoDocumentoVeiculo tipo;

    private String numero;
    private LocalDate dataEmissao;

    @NotNull(message = "Data de validade é obrigatória")
    private LocalDate validade;

    private UUID uploadId;
    private String observacoes;
}
