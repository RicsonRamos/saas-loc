package com.locadora.contrato.repository;

import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Contrato — Single-Tenant.
 */
@Repository
public interface ContratoRepository extends JpaRepository<Contrato, UUID> {

    Page<Contrato> findByDeletedAtIsNull(Pageable pageable);

    Optional<Contrato> findByIdAndDeletedAtIsNull(UUID id);

    boolean existsByVeiculoIdAndStatusAndDeletedAtIsNull(UUID veiculoId, StatusContrato status);
}
