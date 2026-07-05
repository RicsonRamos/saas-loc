package com.locadora.alerta.dto;

import com.locadora.alerta.entity.TipoAlerta;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AlertaResponse {

    private UUID id;
    private TipoAlerta tipo;
    private String titulo;
    private String descricao;
    private UUID entidadeId;
    private Boolean lido;
    private LocalDate dataAlerta;
    private LocalDateTime createdAt;
}
