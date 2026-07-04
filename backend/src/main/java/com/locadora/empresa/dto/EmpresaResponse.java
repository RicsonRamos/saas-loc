package com.locadora.empresa.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDateTime;
import java.util.UUID;

/**
 * Response DTO de Empresa.
 * Conforme 08-guard-rails.md: nunca expor entidades JPA.
 */
@Getter
@Builder
@AllArgsConstructor
public class EmpresaResponse {

    private UUID id;
    private String nomeFantasia;
    private String razaoSocial;
    private String cnpj;
    private String endereco;
    private String telefone;
    private String email;
    private String logoUrl;
    private Boolean ativo;
    private LocalDateTime createdAt;
}
