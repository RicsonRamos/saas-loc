package com.locadora.financeiro.dto;

import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

/**
 * Payload de resposta de transação financeira, exibindo vínculos caso existam.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LancamentoResponse {
    
    private UUID id;
    private TipoTransacao tipo;
    private BigDecimal valor;
    private CategoriaFinanceira categoria;
    private String descricao;
    private StatusPagamento status;
    private LocalDate dataVencimento;
    private LocalDate dataPagamento;

    private UUID veiculoId;
    private String veiculoPlaca;

    private UUID contratoId;

    private String centroCusto;
    private String formaPagamento;
    private Integer parcelas;
    private String comprovanteUrl;
}
