package com.locadora.frota.dto;

import com.locadora.frota.entity.StatusVeiculo;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class VeiculoRequest {

    @NotBlank(message = "Placa é obrigatória")
    @Size(max = 10, message = "Placa deve ter no máximo 10 caracteres")
    private String placa;

    @NotBlank(message = "Chassi é obrigatório")
    @Size(max = 30, message = "Chassi deve ter no máximo 30 caracteres")
    private String chassi;

    @Size(max = 20, message = "Renavam deve ter no máximo 20 caracteres")
    private String renavam;

    @NotBlank(message = "Marca é obrigatória")
    @Size(max = 100, message = "Marca deve ter no máximo 100 caracteres")
    private String marca;

    @NotBlank(message = "Modelo é obrigatório")
    @Size(max = 100, message = "Modelo deve ter no máximo 100 caracteres")
    private String modelo;

    @NotNull(message = "Ano de fabricação é obrigatório")
    @Min(value = 1900, message = "Ano de fabricação inválido")
    private Integer anoFabricacao;

    @NotNull(message = "Ano do modelo é obrigatório")
    @Min(value = 1900, message = "Ano do modelo inválido")
    private Integer anoModelo;

    @Size(max = 50, message = "Cor deve ter no máximo 50 caracteres")
    private String cor;

    @NotNull(message = "Quilometragem é obrigatória")
    @Min(value = 0, message = "Quilometragem não pode ser negativa")
    private Integer quilometragem;

    @NotNull(message = "Status é obrigatório")
    private StatusVeiculo status;

    private BigDecimal valorFipe;

    private BigDecimal valorCompra;

    private LocalDate dataCompra;

    @Size(max = 500)
    private String documentoUrl;
}
