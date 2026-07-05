package com.locadora.financeiro.entity;

/**
 * Representa a situação atual do pagamento da transação.
 */
public enum StatusPagamento {
    /**
     * Boleto gerado, fatura em aberto ou dívida não quitada.
     */
    PENDENTE,
    
    /**
     * Dinheiro efetivamente entrou ou saiu do caixa.
     */
    PAGO,
    
    /**
     * Lançamento estornado, cancelado ou invalidado.
     */
    CANCELADO
}
