package com.locadora.empresa.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

/**
 * DTO para registro de nova empresa com primeiro usuário administrador.
 */
@Getter
@NoArgsConstructor
@AllArgsConstructor
public class RegistroEmpresaRequest {

    // Dados da empresa
    @NotBlank(message = "Nome fantasia é obrigatório")
    @Size(max = 200)
    private String nomeFantasia;

    @NotBlank(message = "Razão social é obrigatória")
    @Size(max = 300)
    private String razaoSocial;

    @NotBlank(message = "CNPJ é obrigatório")
    @Size(min = 14, max = 18)
    private String cnpj;

    // Dados do primeiro usuário (admin)
    @NotBlank(message = "Nome do administrador é obrigatório")
    @Size(max = 200)
    private String nomeAdmin;

    @NotBlank(message = "E-mail do administrador é obrigatório")
    @Email(message = "E-mail inválido")
    private String emailAdmin;

    @NotBlank(message = "Senha é obrigatória")
    @Size(min = 8, message = "Senha deve ter no mínimo 8 caracteres")
    private String senhaAdmin;
}
