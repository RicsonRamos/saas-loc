package com.locadora.financeiro.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

/**
 * Representa um sumário financeiro de um determinado mês/período.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FluxoCaixaResponse {
    
    private int ano;
    private int mes;
    
    /** Somatório de todas as receitas PAGAS no período */
    private BigDecimal totalReceitas;
    
    /** Somatório de todas as despesas PAGAS no período */
    private BigDecimal totalDespesas;
    
    /** Resultado: Receitas - Despesas */
    private BigDecimal saldoLiquido;
}
