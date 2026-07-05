package com.locadora.financeiro.entity;

/**
 * Categorias pré-definidas para as transações financeiras para simplificar relatórios do MVP.
 */
public enum CategoriaFinanceira {
    /** Receita oriunda de locação de veículos */
    ALUGUEL,
    
    /** Receita retida (caução que virou pagamento) ou devolvida (despesa) */
    CAUCAO,
    
    /** Despesa com reparos e peças */
    MANUTENCAO,
    
    /** Despesa com abastecimento */
    COMBUSTIVEL,
    
    /** Despesas com IPVA, multas de trânsito, etc */
    IMPOSTOS_TAXAS,
    
    /** Despesas com equipe (backoffice) */
    SALARIOS,
    
    /** Demais movimentações não categorizadas */
    OUTROS
}
