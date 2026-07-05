package com.locadora.manutencao.entity;

/**
 * Representa os tipos de manutenção aplicáveis a um veículo.
 */
public enum TipoManutencao {
    /**
     * Revisão periódica (ex: troca de óleo, pastilhas) para evitar quebras.
     */
    PREVENTIVA,
    
    /**
     * Conserto após quebra ou acidente.
     */
    CORRETIVA
}
