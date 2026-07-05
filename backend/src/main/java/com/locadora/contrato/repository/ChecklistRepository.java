package com.locadora.contrato.repository;

import com.locadora.contrato.entity.Checklist;
import com.locadora.contrato.entity.TipoChecklist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface ChecklistRepository extends JpaRepository<Checklist, UUID> {

    List<Checklist> findByContratoIdAndTenantIdAndDeletedAtIsNull(UUID contratoId, UUID tenantId);

    Optional<Checklist> findByContratoIdAndTipoAndTenantIdAndDeletedAtIsNull(UUID contratoId, TipoChecklist tipo, UUID tenantId);

    Optional<Checklist> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);
}
