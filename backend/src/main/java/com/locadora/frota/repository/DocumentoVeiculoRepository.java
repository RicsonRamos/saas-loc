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

    List<DocumentoVeiculo> findByVeiculoIdAndDeletedAtIsNull(UUID veiculoId);

    Optional<DocumentoVeiculo> findByIdAndDeletedAtIsNull(UUID id);

    Optional<DocumentoVeiculo> findByVeiculoIdAndTipoAndDeletedAtIsNull(UUID veiculoId, TipoDocumentoVeiculo tipo);

    List<DocumentoVeiculo> findByDeletedAtIsNullAndValidadeBetween(LocalDate start, LocalDate end);
}
