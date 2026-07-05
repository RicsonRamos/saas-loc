package com.locadora.dashboard.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.util.UUID;

/**
 * Versão concreta e processada da rentabilidade, já com o cálculo de lucro efetuado no Java.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class RentabilidadeVeiculoDTO {

    private UUID veiculoId;
    private String placa;
    private String modelo;
    private BigDecimal totalReceitas;
    private BigDecimal totalDespesas;
    private BigDecimal saldoLiquido; // Receita - Despesa
}
