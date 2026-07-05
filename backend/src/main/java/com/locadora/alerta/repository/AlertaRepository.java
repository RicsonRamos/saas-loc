package com.locadora.alerta.repository;

import com.locadora.alerta.entity.Alerta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface AlertaRepository extends JpaRepository<Alerta, UUID> {

    List<Alerta> findByTenantIdAndLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc(UUID tenantId);

    List<Alerta> findByTenantIdAndDeletedAtIsNullOrderByDataAlertaDesc(UUID tenantId);

    Optional<Alerta> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    boolean existsByTipoAndEntidadeIdAndLidoFalseAndTenantIdAndDeletedAtIsNull(com.locadora.alerta.entity.TipoAlerta tipo, UUID entidadeId, UUID tenantId);
}
