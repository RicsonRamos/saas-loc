package com.locadora.manutencao.dto;

import com.locadora.manutencao.entity.TipoManutencao;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

/**
 * Payload retornado para a listagem do frontend.
 */
@Getter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ManutencaoResponse {
    
    private UUID id;
    private UUID veiculoId;
    private String veiculoPlaca;
    private TipoManutencao tipo;
    private String descricao;
    private Integer kmManutencao;
    private LocalDate dataInicio;
    private LocalDate dataFim;
    private BigDecimal custo;
    private boolean concluida;
}
