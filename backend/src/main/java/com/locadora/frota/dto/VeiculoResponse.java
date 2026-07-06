package com.locadora.frota.dto;

import com.locadora.frota.entity.StatusVeiculo;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class VeiculoResponse {

    private UUID id;
    private String placa;
    private String chassi;
    private String renavam;
    private String marca;
    private String modelo;
    private Integer anoFabricacao;
    private Integer anoModelo;
    private String cor;
    private Integer quilometragem;
    private StatusVeiculo status;
    private BigDecimal valorFipe;
    private BigDecimal valorCompra;
    private LocalDate dataCompra;
    private String documentoUrl;
    private String combustivel;
    private String cambio;
    private Integer capacidadeTanque;
    private LocalDate proximaRevisao;
    private LocalDate proximaTrocaOleo;
    private String seguro;
    private String ipva;
    private String crlv;
    private String licenciamento;
    private String categoria;
}
