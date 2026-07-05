package com.locadora.manutencao.repository;

import com.locadora.manutencao.entity.Manutencao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Manutenção — Single-Tenant.
 */
@Repository
public interface ManutencaoRepository extends JpaRepository<Manutencao, UUID> {

    Page<Manutencao> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    Page<Manutencao> findByVeiculoIdAndTenantIdAndDeletedAtIsNull(UUID veiculoId, UUID tenantId, Pageable pageable);

    Optional<Manutencao> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);
}
