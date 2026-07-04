package com.locadora.cliente.dto;

import com.locadora.cliente.entity.TipoCliente;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class ClienteRequest {

    @NotBlank(message = "Nome/Razão Social é obrigatório")
    @Size(max = 200, message = "Nome deve ter no máximo 200 caracteres")
    private String nome;

    @NotNull(message = "Tipo de cliente é obrigatório")
    private TipoCliente tipo;

    @NotBlank(message = "Documento (CPF/CNPJ) é obrigatório")
    @Size(max = 20, message = "Documento deve ter no máximo 20 caracteres")
    private String documento;

    @Email(message = "E-mail inválido")
    @Size(max = 200, message = "E-mail deve ter no máximo 200 caracteres")
    private String email;

    @Size(max = 20, message = "Telefone deve ter no máximo 20 caracteres")
    private String telefone;

    @Size(max = 20, message = "CNH deve ter no máximo 20 caracteres")
    private String cnh;

    private LocalDate cnhValidade;

    @Size(max = 10, message = "CEP deve ter no máximo 10 caracteres")
    private String cep;

    @Size(max = 200, message = "Logradouro deve ter no máximo 200 caracteres")
    private String logradouro;

    @Size(max = 20, message = "Número deve ter no máximo 20 caracteres")
    private String numero;

    @Size(max = 100, message = "Complemento deve ter no máximo 100 caracteres")
    private String complemento;

    @Size(max = 100, message = "Bairro deve ter no máximo 100 caracteres")
    private String bairro;

    @Size(max = 100, message = "Cidade deve ter no máximo 100 caracteres")
    private String cidade;

    @Size(max = 2, message = "UF deve ter 2 caracteres")
    private String uf;

    @Size(max = 500)
    private String cnhUrl;

    @Size(max = 500)
    private String comprovanteResidenciaUrl;
}
