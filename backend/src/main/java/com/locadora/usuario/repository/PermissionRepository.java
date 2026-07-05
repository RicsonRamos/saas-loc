package com.locadora.usuario.repository;

import com.locadora.usuario.entity.Permission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Set;
import java.util.UUID;

@Repository
public interface PermissionRepository extends JpaRepository<Permission, UUID> {

    @Query(value = "SELECT p.nome FROM permissions p " +
                   "JOIN role_permissions rp ON rp.permission_id = p.id " +
                   "JOIN usuario_roles ur ON ur.role = rp.role " +
                   "WHERE ur.usuario_id = :usuarioId " +
                   "UNION " +
                   "SELECT p.nome FROM permissions p " +
                   "JOIN user_permissions up ON up.permission_id = p.id " +
                   "WHERE up.usuario_id = :usuarioId", nativeQuery = true)
    Set<String> findPermissionNamesByUsuarioId(@Param("usuarioId") UUID usuarioId);
}
