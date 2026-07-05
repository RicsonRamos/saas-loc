package com.locadora.auditoria.repository;

import com.locadora.auditoria.entity.Auditoria;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AuditoriaRepository extends JpaRepository<Auditoria, UUID> {

    Page<Auditoria> findAllByOrderByCreatedAtDesc(Pageable pageable);

    List<Auditoria> findByCorrelationId(String correlationId);
}
