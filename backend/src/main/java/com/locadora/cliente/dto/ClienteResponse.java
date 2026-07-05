package com.locadora.cliente.dto;

import com.locadora.cliente.entity.TipoCliente;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;

import java.time.LocalDate;
import java.util.UUID;

@Getter
@Builder
@AllArgsConstructor
public class ClienteResponse {

    private UUID id;
    private String nome;
    private TipoCliente tipo;
    private String documento;
    private String email;
    private String telefone;
    private String cnh;
    private LocalDate cnhValidade;
    
    private String cep;
    private String logradouro;
    private String numero;
    private String complemento;
    private String bairro;
    private String cidade;
    private String uf;

    private String cnhUrl;
    private String comprovanteResidenciaUrl;
    private String cnhCategoria;
    private Boolean bloqueado;
    private String observacoes;
}
