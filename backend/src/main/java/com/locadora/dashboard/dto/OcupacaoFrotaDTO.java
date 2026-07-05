package com.locadora.dashboard.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * Retrato atual da disponibilidade e utilização da frota.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OcupacaoFrotaDTO {

    /** Total de carros na base do tenant */
    private long totalVeiculos;

    /** Carros parados no pátio */
    private long veiculosDisponiveis;

    /** Carros gerando dinheiro (alugados) */
    private long veiculosLocados;

    /** Carros gerando despesa (oficina) */
    private long veiculosEmManutencao;

    /** Porcentagem (0 a 100) da frota que está locada (veiculosLocados / totalVeiculos) */
    private double taxaOcupacao;
}
