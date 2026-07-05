package com.locadora.reserva.dto;

import com.locadora.reserva.entity.OrigemReserva;
import com.locadora.reserva.entity.StatusReserva;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReservaRequest {

    @NotNull(message = "Cliente é obrigatório")
    private UUID clienteId;

    private UUID veiculoId;

    @NotBlank(message = "Categoria do veículo é obrigatória")
    private String categoria;

    @NotNull(message = "Data de início é obrigatória")
    private LocalDateTime dataInicio;

    @NotNull(message = "Data de término é obrigatória")
    private LocalDateTime dataFim;

    @NotNull(message = "Origem da reserva é obrigatória")
    private OrigemReserva origem;

    private StatusReserva status;
    private String observacoes;
}
