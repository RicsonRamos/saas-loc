package com.locadora.manutencao.repository;

import com.locadora.manutencao.entity.Manutencao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Manutenção.
 * Aplica isolamento de tenant em todas as queries.
 */
@Repository
public interface ManutencaoRepository extends JpaRepository<Manutencao, UUID> {

    /**
     * Lista todas as manutenções da locadora.
     */
    Page<Manutencao> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);
    
    /**
     * Lista as manutenções de um veículo específico.
     */
    Page<Manutencao> findByVeiculoIdAndTenantIdAndDeletedAtIsNull(UUID veiculoId, UUID tenantId, Pageable pageable);

    /**
     * Busca uma manutenção por ID.
     */
    Optional<Manutencao> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);
}
