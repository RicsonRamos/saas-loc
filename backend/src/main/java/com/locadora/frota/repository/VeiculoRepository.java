package com.locadora.frota.repository;

import com.locadora.frota.entity.Veiculo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Veículo.
 * Garante consultas isoladas por tenant.
 */
@Repository
public interface VeiculoRepository extends JpaRepository<Veiculo, UUID> {

    Page<Veiculo> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    Optional<Veiculo> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    boolean existsByPlacaAndTenantIdAndDeletedAtIsNull(String placa, UUID tenantId);

    boolean existsByChassiAndTenantIdAndDeletedAtIsNull(String chassi, UUID tenantId);
}
