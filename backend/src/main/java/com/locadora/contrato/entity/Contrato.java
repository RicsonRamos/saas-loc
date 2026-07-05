package com.locadora.contrato.entity;

import com.locadora.cliente.entity.Cliente;
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
import java.time.LocalDateTime;


@Entity
@Table(name = "contratos")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Contrato extends BaseEntity {

    /**
     * Cliente locatário. Ligação LAZY para não puxar dados quando não necessário.
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "cliente_id", nullable = false)
    private Cliente cliente;

    /**
     * Veículo sendo locado. Ligação LAZY.
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "veiculo_id", nullable = false)
    private Veiculo veiculo;

    /**
     * Status atual do contrato.
     */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    @Builder.Default
    private StatusContrato status = StatusContrato.RASCUNHO;

    /**
     * Data e hora exata que o contrato inicia (retirada do veículo).
     */
    @Column(name = "data_inicio", nullable = false)
    private LocalDateTime dataInicio;

    /**
     * Data e hora exata prevista para o término (devolução).
     */
    @Column(name = "data_fim_prevista", nullable = false)
    private LocalDateTime dataFimPrevista;

    /**
     * Data e hora real que o veículo foi devolvido (preenchida no encerramento).
     */
    @Column(name = "data_devolucao")
    private LocalDateTime dataDevolucao;

    /**
     * Valor principal combinado para a locação.
     */
    @Column(name = "valor_total", nullable = false, precision = 19, scale = 4)
    private BigDecimal valorTotal;

    /**
     * Valor retido do cliente como garantia (depositado ou travado no cartão).
     */
    @Column(precision = 19, scale = 4)
    private BigDecimal caucao;

    /**
     * Valor financeiro que foi de fato pago por quilometragem excedente, avarias, etc.
     */
    @Column(name = "valor_adicional", precision = 19, scale = 4)
    @Builder.Default
    private BigDecimal valorAdicional = BigDecimal.ZERO;

    /**
     * Hodômetro do veículo no instante em que ele sai da agência.
     */
    @Column(name = "km_inicial", nullable = false)
    private Integer kmInicial;

    /**
     * Hodômetro do veículo no instante em que ele retorna.
     */
    @Column(name = "km_final")
    private Integer kmFinal;

    /**
     * Quantidade de quilômetros além do estipulado na franquia (se houver).
     */
    @Column(name = "km_excedente")
    @Builder.Default
    private Integer kmExcedente = 0;

    @Column(name = "checklist_retirada_id")
    private UUID checklistRetiradaId;

    @Column(name = "checklist_devolucao_id")
    private UUID checklistDevolucaoId;

    @Column(nullable = false, precision = 19, scale = 4)
    @Builder.Default
    private BigDecimal multas = BigDecimal.ZERO;

    @Column(length = 20)
    private String combustivel;

    @Column(columnDefinition = "TEXT")
    private String acessorios;

    @Column(columnDefinition = "TEXT")
    private String observacoes;

    @Column(name = "assinatura_url", length = 500)
    private String assinaturaUrl;
}
