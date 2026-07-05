package com.locadora.upload.dto;

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
public class UploadResponse {

    private UUID id;
    private UUID uuidArquivo;
    private String nomeOriginal;
    private String mimeType;
    private Long tamanho;
    private Integer largura;
    private Integer altura;
    private String relacionamentoTipo;
    private UUID relacionamentoId;
    private LocalDateTime createdAt;
}
