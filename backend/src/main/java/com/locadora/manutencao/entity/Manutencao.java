package com.locadora.manutencao.entity;

import com.locadora.common.entity.BaseEntity;
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
 * Aggregate Root: Manutencao.
 * Registra os serviços realizados em um veículo na oficina.
 */
@Entity
@Table(name = "manutencoes")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Manutencao extends BaseEntity {

    /**
     * Veículo que está passando pelo serviço. LAZY para não poluir as queries.
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "veiculo_id", nullable = false)
    private Veiculo veiculo;

    /**
     * Natureza da manutenção.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TipoManutencao tipo;

    /**
     * Descrição livre das peças trocadas ou defeito constatado.
     */
    @Column(nullable = false, length = 1000)
    private String descricao;

    /**
     * Quilometragem do veículo no momento em que entrou na oficina.
     */
    @Column(name = "km_manutencao", nullable = false)
    private Integer kmManutencao;

    /**
     * Data de entrada do veículo na oficina.
     */
    @Column(name = "data_inicio", nullable = false)
    private LocalDate dataInicio;

    /**
     * Data de saída (quando a manutenção foi concluída). Null se estiver em andamento.
     */
    @Column(name = "data_fim")
    private LocalDate dataFim;

    /**
     * Custo total do reparo, para integrar com o módulo financeiro.
     */
    @Column(nullable = false, precision = 19, scale = 4)
    @Builder.Default
    private BigDecimal custo = BigDecimal.ZERO;

    /**
     * Indica se a oficina liberou o carro.
     */
    @Column(nullable = false)
    @Builder.Default
    private boolean concluida = false;
}
