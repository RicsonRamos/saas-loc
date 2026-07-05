package com.locadora.financeiro.entity;

import com.locadora.common.entity.BaseEntity;
import com.locadora.contrato.entity.Contrato;
import com.locadora.frota.entity.Veiculo;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Aggregate Root: LancamentoFinanceiro.
 * Registra entradas e saídas de capital. Pode ter vínculos opcionais com
 * outras entidades para relatórios de rentabilidade (ROI).
 */
@Entity
@Table(name = "lancamentos_financeiros")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LancamentoFinanceiro extends BaseEntity {

    /**
     * Define se é Receita ou Despesa.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TipoTransacao tipo;

    /**
     * Valor monetário da transação. Sempre positivo (o tipo define se soma ou subtrai).
     */
    @Column(nullable = false, precision = 19, scale = 4)
    private BigDecimal valor;

    /**
     * Categoria para agrupamento em dashboards.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private CategoriaFinanceira categoria;

    /**
     * Descrição livre preenchida pelo operador ou pelo sistema.
     */
    @Column(nullable = false, length = 500)
    private String descricao;

    /**
     * Situação do título.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    @Builder.Default
    private StatusPagamento status = StatusPagamento.PAGO;

    /**
     * Data limite/acordada para pagamento.
     */
    @Column(name = "data_vencimento", nullable = false)
    private LocalDate dataVencimento;

    /**
     * Data real da efetivação do pagamento. Null se pendente.
     */
    @Column(name = "data_pagamento")
    private LocalDate dataPagamento;

    /**
     * Opcional: Veículo atrelado (Ex: Custo de manutenção deste carro específico).
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "veiculo_id")
    private Veiculo veiculo;

    /**
     * Opcional: Contrato atrelado (Ex: Recebimento do aluguel XYZ).
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contrato_id")
    private Contrato contrato;

    @Column(name = "centro_custo", length = 100)
    private String centroCusto;

    @Column(name = "forma_pagamento", length = 50)
    private String formaPagamento;

    @Column
    @Builder.Default
    private Integer parcelas = 1;

    @Column(name = "comprovante_url", length = 500)
    private String comprovanteUrl;
}
