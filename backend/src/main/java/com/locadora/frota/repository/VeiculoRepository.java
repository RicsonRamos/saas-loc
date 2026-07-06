package com.locadora.frota.repository;

import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Veículo — Single-Tenant.
 */
@Repository
public interface VeiculoRepository extends JpaRepository<Veiculo, UUID> {

    Page<Veiculo> findAllByDeletedAtIsNull(Pageable pageable);

    Optional<Veiculo> findByIdAndDeletedAtIsNull(UUID id);

    boolean existsByPlacaAndDeletedAtIsNull(String placa);

    boolean existsByChassiAndDeletedAtIsNull(String chassi);

    long countByDeletedAtIsNull();

    long countByStatusAndDeletedAtIsNull(StatusVeiculo status);
}
