package com.locadora.empresa.repository;

import com.locadora.empresa.entity.Empresa;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Empresa.
 * Conforme 08-guard-rails.md: apenas responsabilidade de persistência.
 */
@Repository
public interface EmpresaRepository extends JpaRepository<Empresa, UUID> {

    Optional<Empresa> findByCnpjAndDeletedAtIsNull(String cnpj);

    boolean existsByCnpj(String cnpj);
}
