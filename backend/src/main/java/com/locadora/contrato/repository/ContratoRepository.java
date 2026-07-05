package com.locadora.contrato.repository;

import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Contrato.
 * 
 * <p>Responsabilidades: 
 * Acesso a banco de dados estritamente filtrado por Tenant.
 * Verifica a existência de conflitos de locação.</p>
 */
@Repository
public interface ContratoRepository extends JpaRepository<Contrato, UUID> {

    /**
     * Lista contratos filtrando por locadora e ignorando contratos excluídos logicamente.
     */
    Page<Contrato> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    /**
     * Busca os detalhes de um contrato isolando o acesso cruzado.
     */
    Optional<Contrato> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    /**
     * Verifica se existe algum contrato ATIVO para determinado veículo na empresa.
     * Utilizado pela regra de negócios para evitar que um veículo seja alugado duas vezes simultaneamente.
     */
    boolean existsByVeiculoIdAndStatusAndTenantIdAndDeletedAtIsNull(UUID veiculoId, StatusContrato status, UUID tenantId);
}
