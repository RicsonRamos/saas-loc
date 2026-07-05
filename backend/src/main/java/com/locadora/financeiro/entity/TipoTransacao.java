package com.locadora.financeiro.entity;

/**
 * Representa a natureza da transação financeira.
 */
public enum TipoTransacao {
    /**
     * Dinheiro entrando no caixa da locadora (Ex: Locação, multas).
     */
    RECEITA,
    
    /**
     * Dinheiro sainendo do caixa da locadora (Ex: Manutenção, compra de veículos, salários).
     */
    DESPESA
}
