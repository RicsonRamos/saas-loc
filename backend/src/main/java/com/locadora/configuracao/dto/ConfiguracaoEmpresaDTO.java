package com.locadora.configuracao.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.UUID;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ConfiguracaoEmpresaDTO {

    private UUID id;

    @NotBlank(message = "Nome fantasia é obrigatório")
    private String nomeFantasia;

    @NotBlank(message = "Razão social é obrigatória")
    private String razaoSocial;

    @NotBlank(message = "CNPJ é obrigatório")
    @Pattern(regexp = "\\d{2}\\.\\d{3}\\.\\d{3}/\\d{4}-\\d{2}|\\d{14}", message = "CNPJ inválido")
    private String cnpj;

    private String inscricaoEstadual;
    private String endereco;
    private String telefone;

    @Email(message = "E-mail inválido")
    private String email;

    private String logoUrl;
    private String horarioFuncionamento;
    private String politicaCombustivel;
    private String politicaQuilometragem;
    private String informacoesFiscais;
}
