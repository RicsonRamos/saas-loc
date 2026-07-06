package com.locadora.alerta.repository;

import com.locadora.alerta.entity.Alerta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface AlertaRepository extends JpaRepository<Alerta, UUID> {

    List<Alerta> findByTenantIdAndLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc();

    List<Alerta> findByTenantIdAndDeletedAtIsNullOrderByDataAlertaDesc();

    Optional<Alerta> findByIdAndDeletedAtIsNull(UUID id);

    boolean existsByTipoAndEntidadeIdAndLidoFalseAndDeletedAtIsNull(com.locadora.alerta.entity.TipoAlerta tipo, UUID entidadeId);
}
