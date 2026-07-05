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
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

import com.locadora.shared.tenant.TenantContext;
import java.util.UUID;

/**
 * Serviço do Dashboard — Multi-Tenant.
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

    @Transactional(readOnly = true)
    public DashboardResponse obterDashboardMensal() {
        UUID tenantId = TenantContext.getTenantId();
        OcupacaoFrotaDTO frotaDTO = apurarOcupacaoFrota(tenantId);

        LocalDate hoje = LocalDate.now();
        FluxoCaixaResponse fluxo = financeiroService.obterFluxoMensal(hoje.getYear(), hoje.getMonthValue());

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

        List<RentabilidadeVeiculoDTO> topRentaveis = rentabilidades.stream()
                .sorted(Comparator.comparing(RentabilidadeVeiculoDTO::getSaldoLiquido).reversed())
                .limit(5)
                .toList();

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

    private OcupacaoFrotaDTO apurarOcupacaoFrota(UUID tenantId) {
        long total = veiculoRepository.countByTenantIdAndDeletedAtIsNull(tenantId);
        long disponiveis = veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.DISPONIVEL, tenantId);
        long locados = veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.LOCADO, tenantId);
        long oficina = veiculoRepository.countByStatusAndTenantIdAndDeletedAtIsNull(StatusVeiculo.MANUTENCAO, tenantId);

        double taxaOcupacao = 0.0;
        if (total > 0) {
            taxaOcupacao = ((double) locados / total) * 100.0;
        }

        return OcupacaoFrotaDTO.builder()
                .totalVeiculos(total)
                .veiculosDisponiveis(disponiveis)
                .veiculosLocados(locados)
                .veiculosEmManutencao(oficina)
                .taxaOcupacao(Math.round(taxaOcupacao * 100.0) / 100.0)
                .build();
    }
}
