package com.locadora.financeiro.repository;

import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.dashboard.dto.RentabilidadeVeiculoProjection;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Repository de Lançamentos Financeiros — Single-Tenant.
 */
@Repository
public interface LancamentoFinanceiroRepository extends JpaRepository<LancamentoFinanceiro, UUID> {

    Page<LancamentoFinanceiro> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    Optional<LancamentoFinanceiro> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    @Query("SELECT SUM(l.valor) FROM LancamentoFinanceiro l " +
           "WHERE l.tipo = :tipo AND l.status = :status AND l.deletedAt IS NULL AND l.tenantId = :tenantId " +
           "AND l.dataPagamento >= :inicio AND l.dataPagamento <= :fim")
    BigDecimal sumValorByTipoAndStatusAndPeriodo(
            @Param("tipo") TipoTransacao tipo,
            @Param("status") StatusPagamento status,
            @Param("inicio") LocalDate inicio,
            @Param("fim") LocalDate fim,
            @Param("tenantId") UUID tenantId
    );

    @Query("SELECT v.id as veiculoId, v.placa as placa, v.modelo as modelo, " +
           "SUM(CASE WHEN l.tipo = 'RECEITA' THEN l.valor ELSE 0 END) as totalReceitas, " +
           "SUM(CASE WHEN l.tipo = 'DESPESA' THEN l.valor ELSE 0 END) as totalDespesas " +
           "FROM LancamentoFinanceiro l JOIN l.veiculo v " +
           "WHERE l.status = 'PAGO' AND l.deletedAt IS NULL AND l.tenantId = :tenantId " +
           "GROUP BY v.id, v.placa, v.modelo")
    List<RentabilidadeVeiculoProjection> getRentabilidadeVeiculos(@Param("tenantId") UUID tenantId);

    List<LancamentoFinanceiro> findByTenantIdAndDataPagamentoBetweenAndDeletedAtIsNullOrderByDataPagamentoDesc(
            UUID tenantId, LocalDate inicio, LocalDate fim);
}
