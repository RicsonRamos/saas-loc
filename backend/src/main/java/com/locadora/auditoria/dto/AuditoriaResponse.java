package com.locadora.auditoria.dto;

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
public class AuditoriaResponse {

    private UUID id;
    private String usuario;
    private String acao;
    private String entidade;
    private UUID entidadeId;
    private String oldData;
    private String newData;
    private String ip;
    private String userAgent;
    private String correlationId;
    private LocalDateTime createdAt;
}
