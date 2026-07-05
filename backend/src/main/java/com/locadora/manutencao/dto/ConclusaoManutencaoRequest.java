package com.locadora.manutencao.dto;

import jakarta.validation.constraints.DecimalMin;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

/**
 * Payload utilizado no endpoint de conclusão de serviço.
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class ConclusaoManutencaoRequest {

    /**
     * Custo apurado do reparo.
     */
    @NotNull(message = "Custo é obrigatório")
    @DecimalMin(value = "0.0", message = "Custo não pode ser negativo")
    private BigDecimal custo;

    /**
     * Data de liberação da oficina.
     */
    @NotNull(message = "Data de fim é obrigatória")
    private LocalDate dataFim;
    
    /**
     * Se houve troca de peça que não constava no início, pode concatenar. (Opcional)
     */
    private String detalhesAdicionais;
}
