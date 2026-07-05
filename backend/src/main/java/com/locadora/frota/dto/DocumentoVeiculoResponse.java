package com.locadora.frota.dto;

import com.locadora.frota.entity.TipoDocumentoVeiculo;
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
public class DocumentoVeiculoResponse {

    private UUID id;
    private UUID veiculoId;
    private String veiculoPlaca;
    private String veiculoModelo;
    private TipoDocumentoVeiculo tipo;
    private String numero;
    private LocalDate dataEmissao;
    private LocalDate validade;
    private UUID uploadId;
    private String observacoes;
}
