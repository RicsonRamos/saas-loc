package com.locadora.contrato.dto;

import com.locadora.contrato.entity.TipoChecklist;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ChecklistRequest {

    @NotNull(message = "Contrato é obrigatório")
    private UUID contratoId;

    @NotNull(message = "Tipo de checklist é obrigatório")
    private TipoChecklist tipo;

    @NotBlank(message = "Itens do checklist são obrigatórios")
    private String itensJson; // JSON string format

    private String fotosJson; // JSON string format
    private String assinaturaClienteUrl;
    private String assinaturaOperadorUrl;
}
