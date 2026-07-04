package com.locadora.cliente.repository;

import com.locadora.cliente.entity.Cliente;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Cliente.
 * Garante consultas isoladas por tenant.
 */
@Repository
public interface ClienteRepository extends JpaRepository<Cliente, UUID> {

    Page<Cliente> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    Optional<Cliente> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    boolean existsByDocumentoAndTenantIdAndDeletedAtIsNull(String documento, UUID tenantId);
}
