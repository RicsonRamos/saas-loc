package com.locadora.contrato.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.FutureOrPresent;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Payload recebido do frontend para iniciar um novo contrato de locação.
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class ContratoRequest {

    /**
     * ID do Cliente que vai alugar.
     */
    @NotNull(message = "O cliente é obrigatório")
    private UUID clienteId;

    /**
     * ID do Veículo que será alugado.
     */
    @NotNull(message = "O veículo é obrigatório")
    private UUID veiculoId;

    /**
     * Data/hora estipulada para retirada.
     */
    @NotNull(message = "Data de início é obrigatória")
    private LocalDateTime dataInicio;

    /**
     * Data/hora estipulada para devolução.
     */
    @NotNull(message = "Data de devolução prevista é obrigatória")
    @FutureOrPresent(message = "A data de devolução prevista não pode estar no passado")
    private LocalDateTime dataFimPrevista;

    /**
     * Valor total estipulado para a locação (diárias + taxas).
     */
    @NotNull(message = "Valor total é obrigatório")
    @DecimalMin(value = "0.0", inclusive = false, message = "Valor total deve ser maior que zero")
    private BigDecimal valorTotal;

    /**
     * Valor cobrado/retido do cliente como garantia.
     */
    @DecimalMin(value = "0.0", message = "A caução não pode ser negativa")
    private BigDecimal caucao;

    private UUID checklistRetiradaId;
    private UUID checklistDevolucaoId;
    private BigDecimal multas;
    private String combustivel;
    private String acessorios;
    private String observacoes;
    private String assinaturaUrl;
}
