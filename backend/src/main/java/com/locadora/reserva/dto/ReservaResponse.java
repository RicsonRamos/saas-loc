package com.locadora.reserva.dto;

import com.locadora.reserva.entity.OrigemReserva;
import com.locadora.reserva.entity.StatusReserva;
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
public class ReservaResponse {

    private UUID id;
    private UUID clienteId;
    private String clienteNome;
    private String clienteTelefone;
    private UUID veiculoId;
    private String veiculoPlaca;
    private String veiculoModelo;
    private String categoria;
    private StatusReserva status;
    private LocalDateTime dataInicio;
    private LocalDateTime dataFim;
    private OrigemReserva origem;
    private String observacoes;
    private LocalDateTime createdAt;
}
