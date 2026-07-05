package com.locadora.dashboard.service;

import com.locadora.dashboard.dto.DashboardResponse;
import com.locadora.dashboard.dto.OcupacaoFrotaDTO;
import com.locadora.dashboard.dto.RentabilidadeVeiculoDTO;
import com.locadora.dashboard.dto.RentabilidadeVeiculoProjection;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.shared.tenant.TenantContext;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.UUID;
import java.util.stream.Collectors;

/**
 * Serviço exclusivo para montar o painel executivo (Dashboard).
 * Foca em processamento matemático e agregação de dados em tempo real.
 */
@Service
public class DashboardService {

    private final VeiculoRepository veiculoRepository;
    private final FinanceiroService financeiroService;
    private final LancamentoFinanceiroRepository lancamentoFinanceiroRepository;

    public DashboardService(VeiculoRepository veiculoRepository,
                            FinanceiroService financeiroService,
                            LancamentoFinanceiroRepository lancamentoFinanceiroRepository) {
        this.veiculoRepository = veiculoRepository;
        this.financeiroService = financeiroService;
        this.lancamentoFinanceiroRepository = lancamentoFinanceiroRepository;
    }

    /**
     * Monta o Payload pesado do dashboard utilizando chamadas otimizadas para o DB.
     */
    @Transactional(readOnly = true)
    public DashboardResponse obterDashboardMensal() {
        UUID tenantId = TenantContext.requireTenantId();
        
        // 1. KPI Frota
        OcupacaoFrotaDTO frotaDTO = apurarOcupacaoFrota(tenantId);
        
        // 2. KPI Financeiro do Mês (Reutilizando a regra do EPIC 5)
        LocalDate hoje = LocalDate.now();
        FluxoCaixaResponse fluxo = financeiroService.obterFluxoMensal(hoje.getYear(), hoje.getMonthValue());
        
        // 3. KPI Rentabilidade (Calculado no Java após o GROUP BY do Postgres)
        List<RentabilidadeVeiculoProjection> projecoes = lancamentoFinanceiroRepository.getRentabilidadeVeiculos(tenantId);
        
        List<RentabilidadeVeiculoDTO> rentabilidades = projecoes.stream().map(p -> {
            BigDecimal rec = p.getTotalReceitas() != null ? p.getTotalReceitas() : BigDecimal.ZERO;
            BigDecimal des = p.getTotalDespesas() != null ? p.getTotalDespesas() : BigDecimal.ZERO;
            return RentabilidadeVeiculoDTO.builder()
                    .veiculoId(p.getVeiculoId())
                    .placa(p.getPlaca())
                    .modelo(p.getModelo())
                    .totalReceitas(rec)
                    .totalDespesas(des)
                    .saldoLiquido(rec.subtract(des))
                    .build();
        }).collect(Collectors.toList());

        // Ordenar os Top 5 Lucro
        List<RentabilidadeVeiculoDTO> topRentaveis = rentabilidades.stream()
                .sorted(Comparator.comparing(RentabilidadeVeiculoDTO::getSaldoLiquido).reversed())
                .limit(5)
                .toList();

        // Ordenar os Top 5 Prejuízo
        List<RentabilidadeVeiculoDTO> topPrejuizo = rentabilidades.stream()
                .sorted(Comparator.comparing(RentabilidadeVeiculoDTO::getSaldoLiquido))
                .limit(5)
                .toList();

        return DashboardResponse.builder()
                .ocupacaoFrota(frotaDTO)
                .balancoMensal(fluxo)
                .topVeiculosRentaveis(topRentaveis)
                .topVeiculosPrejuizo(topPrejuizo)
                .build();
    }

    /**
     * Calcula as porcentagens de ocupação.
     */
    private OcupacaoFrotaDTO apurarOcupacaoFrota(UUID tenantId) {
        long total = veiculoRepository.countByTenantIdAndDeletedAtIsNull(tenantId);
        long disponiveis = veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.DISPONIVEL);
        long locados = veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.LOCADO);
        long oficina = veiculoRepository.countByTenantIdAndStatusAndDeletedAtIsNull(tenantId, StatusVeiculo.MANUTENCAO);

        double taxaOcupacao = 0.0;
        if (total > 0) {
            taxaOcupacao = ((double) locados / total) * 100.0;
        }

        return OcupacaoFrotaDTO.builder()
                .totalVeiculos(total)
                .veiculosDisponiveis(disponiveis)
                .veiculosLocados(locados)
                .veiculosEmManutencao(oficina)
                .taxaOcupacao(Math.round(taxaOcupacao * 100.0) / 100.0) // Arredonda 2 casas
                .build();
    }
}
