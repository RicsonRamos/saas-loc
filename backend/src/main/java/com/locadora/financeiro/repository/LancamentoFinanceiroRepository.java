package com.locadora.financeiro.repository;

import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
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
 * Repository de Lançamentos Financeiros.
 * Possui queries agregadoras essenciais para o fluxo de caixa mensal.
 */
@Repository
public interface LancamentoFinanceiroRepository extends JpaRepository<LancamentoFinanceiro, UUID> {

    /**
     * Retorna o balancete completo paginado, isolado pelo Tenant.
     */
    Page<LancamentoFinanceiro> findByTenantIdAndDeletedAtIsNull(UUID tenantId, Pageable pageable);

    /**
     * Busca os detalhes de uma transação isolando o tenant.
     */
    Optional<LancamentoFinanceiro> findByIdAndTenantIdAndDeletedAtIsNull(UUID id, UUID tenantId);

    /**
     * Query customizada: Soma todos os valores de um determinado Tipo (Receita/Despesa),
     * em um intervalo de datas baseado na DATA DE PAGAMENTO (Caixa efetivo),
     * e cujo status seja PAGO.
     * 
     * @param tenantId A qual locadora pertence os dados.
     * @param tipo Tipo da transação (RECEITA ou DESPESA).
     * @param status Status do pagamento (Sempre usaremos PAGO).
     * @param inicio Primeiro dia do mês/período.
     * @param fim Último dia do mês/período.
     * @return O total somado, ou nulo se não houver registros.
     */
    @Query("SELECT SUM(l.valor) FROM LancamentoFinanceiro l WHERE l.tenantId = :tenantId " +
           "AND l.tipo = :tipo AND l.status = :status AND l.deletedAt IS NULL " +
           "AND l.dataPagamento >= :inicio AND l.dataPagamento <= :fim")
    BigDecimal sumValorByTipoAndStatusAndPeriodo(
            @Param("tenantId") UUID tenantId,
            @Param("tipo") TipoTransacao tipo,
            @Param("status") StatusPagamento status,
            @Param("inicio") LocalDate inicio,
            @Param("fim") LocalDate fim
    );

    /**
     * Agrupa as receitas e despesas PAGAS por veículo para apurar o ROI/Lucro.
     */
    @Query("SELECT v.id as veiculoId, v.placa as placa, v.modelo as modelo, " +
           "SUM(CASE WHEN l.tipo = 'RECEITA' THEN l.valor ELSE 0 END) as totalReceitas, " +
           "SUM(CASE WHEN l.tipo = 'DESPESA' THEN l.valor ELSE 0 END) as totalDespesas " +
           "FROM LancamentoFinanceiro l JOIN l.veiculo v " +
           "WHERE l.tenantId = :tenantId AND l.status = 'PAGO' AND l.deletedAt IS NULL " +
           "GROUP BY v.id, v.placa, v.modelo")
    List<RentabilidadeVeiculoProjection> getRentabilidadeVeiculos(@Param("tenantId") UUID tenantId);
}
