package com.locadora.contrato.dto;

import com.locadora.contrato.entity.TipoChecklist;
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
public class ChecklistResponse {

    private UUID id;
    private UUID contratoId;
    private TipoChecklist tipo;
    private String itensJson;
    private String fotosJson;
    private String assinaturaClienteUrl;
    private String assinaturaOperadorUrl;
    private LocalDateTime createdAt;
}
