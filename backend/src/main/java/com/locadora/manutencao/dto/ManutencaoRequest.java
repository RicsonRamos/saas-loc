package com.locadora.manutencao.dto;

import com.locadora.manutencao.entity.TipoManutencao;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.UUID;

/**
 * Payload utilizado ao iniciar um serviço no veículo (mandar para oficina).
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class ManutencaoRequest {

    /**
     * Veículo que será enviado para manutenção.
     */
    @NotNull(message = "Veículo é obrigatório")
    private UUID veiculoId;

    /**
     * Natureza da manutenção (preventiva, corretiva).
     */
    @NotNull(message = "Tipo de manutenção é obrigatório")
    private TipoManutencao tipo;

    /**
     * Descrição do defeito ou do que será trocado.
     */
    @NotBlank(message = "Descrição é obrigatória")
    @Size(max = 1000)
    private String descricao;

    /**
     * Data que entrou na oficina.
     */
    @NotNull(message = "Data de início é obrigatória")
    private LocalDate dataInicio;
}
