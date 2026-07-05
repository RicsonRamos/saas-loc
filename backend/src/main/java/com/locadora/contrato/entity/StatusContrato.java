package com.locadora.contrato.entity;

/**
 * Representa os possíveis estados de um Contrato de Locação.
 * <p>
 * O ciclo de vida normal é: RASCUNHO -> ATIVO -> ENCERRADO.
 * Caso haja desistência, pode ir de RASCUNHO -> CANCELADO.
 * Se houver pendências não resolvidas, pode ir para INADIMPLENTE.
 * </p>
 */
public enum StatusContrato {
    /**
     * O contrato está sendo montado (não efetiva cobrança nem afeta a frota).
     */
    RASCUNHO,
    
    /**
     * O contrato está vigente (o veículo está com o cliente).
     */
    ATIVO,
    
    /**
     * O contrato terminou e o veículo foi devolvido com sucesso.
     */
    ENCERRADO,
    
    /**
     * O contrato foi cancelado antes de ser ativado.
     */
    CANCELADO,
    
    /**
     * O contrato encerrou, o veículo foi devolvido, mas o cliente tem dívidas pendentes.
     */
    INADIMPLENTE
}
