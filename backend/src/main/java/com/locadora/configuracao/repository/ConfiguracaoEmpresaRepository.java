package com.locadora.configuracao.repository;

import com.locadora.configuracao.entity.ConfiguracaoEmpresa;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ConfiguracaoEmpresaRepository extends JpaRepository<ConfiguracaoEmpresa, UUID> {
}
