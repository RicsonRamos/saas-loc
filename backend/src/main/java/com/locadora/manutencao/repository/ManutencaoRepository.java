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

    Page<Manutencao> findByDeletedAtIsNull(Pageable pageable);

    Page<Manutencao> findByVeiculoIdAndDeletedAtIsNull(UUID veiculoId, Pageable pageable);

    Optional<Manutencao> findByIdAndDeletedAtIsNull(UUID id);
}
