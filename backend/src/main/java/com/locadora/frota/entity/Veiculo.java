package com.locadora.frota.entity;

import com.locadora.common.entity.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Aggregate Root: Veículo.
 * Conforme 05-modelo-dominio.md.
 */
@Entity
@Table(name = "veiculos", uniqueConstraints = {
        @UniqueConstraint(name = "uk_veiculos_placa", columnNames = {"placa"}),
        @UniqueConstraint(name = "uk_veiculos_chassi", columnNames = {"chassi"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Veiculo extends BaseEntity {

    @Column(nullable = false, length = 10)
    private String placa;

    @Column(nullable = false, length = 30)
    private String chassi;

    @Column(length = 20)
    private String renavam;

    @Column(nullable = false, length = 100)
    private String marca;

    @Column(nullable = false, length = 100)
    private String modelo;

    @Column(name = "ano_fabricacao", nullable = false)
    private Integer anoFabricacao;

    @Column(name = "ano_modelo", nullable = false)
    private Integer anoModelo;

    @Column(length = 50)
    private String cor;

    @Column(nullable = false)
    @Builder.Default
    private Integer quilometragem = 0;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    @Builder.Default
    private StatusVeiculo status = StatusVeiculo.DISPONIVEL;

    @Column(name = "valor_fipe", precision = 19, scale = 4)
    private BigDecimal valorFipe;

    @Column(name = "valor_compra", precision = 19, scale = 4)
    private BigDecimal valorCompra;

    @Column(name = "data_compra")
    private LocalDate dataCompra;

    @Column(name = "documento_url", length = 500)
    private String documentoUrl;
}
