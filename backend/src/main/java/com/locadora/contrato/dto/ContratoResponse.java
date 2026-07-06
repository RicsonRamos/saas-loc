package com.locadora.contrato.dto;

import com.locadora.contrato.entity.StatusContrato;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Payload retornado para o frontend, blindando IDs e senhas internas.
 */
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ContratoResponse {

    private UUID id;
    private UUID clienteId;
    private String clienteNome;
    private UUID veiculoId;
    private String veiculoPlaca;
    private StatusContrato status;
    private LocalDateTime dataInicio;
    private LocalDateTime dataFimPrevista;
    private LocalDateTime dataDevolucao;
    private BigDecimal valorTotal;
    private BigDecimal caucao;
    private BigDecimal valorAdicional;
    private Integer kmInicial;
    private Integer kmFinal;
    private Integer kmExcedente;
    private UUID checklistRetiradaId;
    private UUID checklistDevolucaoId;
    private BigDecimal multas;
    private String combustivel;
    private String acessorios;
    private String observacoes;
    private String assinaturaUrl;
}
