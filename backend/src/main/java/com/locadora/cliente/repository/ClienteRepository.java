package com.locadora.cliente.repository;

import com.locadora.cliente.entity.Cliente;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Cliente — Single-Tenant.
 */
@Repository
public interface ClienteRepository extends JpaRepository<Cliente, UUID> {

    Page<Cliente> findAllByDeletedAtIsNull(Pageable pageable);

    Optional<Cliente> findByIdAndDeletedAtIsNull(UUID id);

    boolean existsByDocumentoAndDeletedAtIsNull(String documento);
}
