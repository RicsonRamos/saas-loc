package com.locadora.usuario.repository;

import com.locadora.usuario.entity.Usuario;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Usuário — Single-Tenant.
 */
@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, UUID> {

    Optional<Usuario> findByEmailAndDeletedAtIsNull(String email);

    boolean existsByEmail(String email);

    Page<Usuario> findByDeletedAtIsNull(Pageable pageable);

    Optional<Usuario> findByIdAndDeletedAtIsNull(UUID id);
}
