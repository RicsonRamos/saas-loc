package com.locadora.usuario.dto;

import com.locadora.usuario.entity.Role;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.Set;
import java.util.UUID;

/**
 * Response DTO de Usuário.
 * Nunca expõe a senha ou dados internos da entidade.
 */
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UsuarioResponse {

    private UUID id;
    private String nome;
    private String email;
    private Boolean ativo;
    private Set<Role> roles;
    private Boolean mustChangePassword;
    private LocalDateTime createdAt;
}
