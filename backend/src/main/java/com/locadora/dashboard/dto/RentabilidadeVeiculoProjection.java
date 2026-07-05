package com.locadora.dashboard.dto;

import java.math.BigDecimal;
import java.util.UUID;

/**
 * Projeção JPA utilizada pelo Spring Data para agrupar os somatórios (GROUP BY) no banco de dados.
 */
public interface RentabilidadeVeiculoProjection {
    
    UUID getVeiculoId();
    
    String getPlaca();
    
    String getModelo();
    
    BigDecimal getTotalReceitas();
    
    BigDecimal getTotalDespesas();
}
