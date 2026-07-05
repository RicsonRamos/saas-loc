package com.locadora.contrato.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * Payload utilizado na rota de encerramento de contrato (Checkout/Devolução).
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class EncerramentoContratoRequest {

    /**
     * Hodômetro real constatado na devolução.
     */
    @NotNull(message = "O KM final é obrigatório")
    @Min(value = 0, message = "O KM final não pode ser negativo")
    private Integer kmFinal;

    /**
     * Data/hora real em que as chaves foram devolvidas (pode ser diferente da dataPrevista).
     */
    @NotNull(message = "A data de devolução é obrigatória")
    private LocalDateTime dataDevolucao;

    /**
     * Quaisquer valores adicionais calculados (por atraso, multa, km excedente, avarias).
     */
    @DecimalMin(value = "0.0", message = "O valor adicional não pode ser negativo")
    private BigDecimal valorAdicional;
}
