package com.locadora.financeiro.dto;

import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

/**
 * Payload para criação de uma transação (despesa ou receita).
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class LancamentoRequest {

    @NotNull(message = "Tipo é obrigatório (RECEITA/DESPESA)")
    private TipoTransacao tipo;

    @NotNull(message = "Valor é obrigatório")
    @DecimalMin(value = "0.0", inclusive = false, message = "Valor deve ser maior que zero")
    private BigDecimal valor;

    @NotNull(message = "Categoria é obrigatória")
    private CategoriaFinanceira categoria;

    @NotBlank(message = "Descrição é obrigatória")
    @Size(max = 500)
    private String descricao;

    @NotNull(message = "Status do pagamento é obrigatório")
    private StatusPagamento status;

    @NotNull(message = "Data de vencimento é obrigatória")
    private LocalDate dataVencimento;

    private LocalDate dataPagamento;

    private UUID veiculoId;
    
    private UUID contratoId;
}
