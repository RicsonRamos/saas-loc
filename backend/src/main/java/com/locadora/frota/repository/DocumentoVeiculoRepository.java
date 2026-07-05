package com.locadora.frota.repository;

import com.locadora.frota.entity.DocumentoVeiculo;
import com.locadora.frota.entity.TipoDocumentoVeiculo;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface DocumentoVeiculoRepository extends JpaRepository<DocumentoVeiculo, UUID> {

    List<DocumentoVeiculo> findByVeiculoIdAndTenantIdAndDeletedAtIsNull(UUID veiculoId, UUID tenantId);

    Optional<DocumentoVeiculo> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    Optional<DocumentoVeiculo> findByVeiculoIdAndTipoAndTenantIdAndDeletedAtIsNull(UUID veiculoId, TipoDocumentoVeiculo tipo, UUID tenantId);

    List<DocumentoVeiculo> findByTenantIdAndDeletedAtIsNullAndValidadeBetween(UUID tenantId, LocalDate start, LocalDate end);
}
