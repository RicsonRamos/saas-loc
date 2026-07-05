package com.locadora.financeiro.service;

import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.dto.LancamentoResponse;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.mapper.LancamentoMapper;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.shared.tenant.TenantContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

/**
 * Serviço responsável por controlar o fluxo de caixa (entradas e saídas).
 */
@Service
public class FinanceiroService {

    private static final Logger log = LoggerFactory.getLogger(FinanceiroService.class);

    private final LancamentoFinanceiroRepository lancamentoRepository;
    private final LancamentoMapper lancamentoMapper;
    private final VeiculoRepository veiculoRepository;
    private final ContratoRepository contratoRepository;

    public FinanceiroService(LancamentoFinanceiroRepository lancamentoRepository,
                             LancamentoMapper lancamentoMapper,
                             VeiculoRepository veiculoRepository,
                             ContratoRepository contratoRepository) {
        this.lancamentoRepository = lancamentoRepository;
        this.lancamentoMapper = lancamentoMapper;
        this.veiculoRepository = veiculoRepository;
        this.contratoRepository = contratoRepository;
    }

    /**
     * Cria uma nova transação, seja manual ou acionada por outro módulo.
     */
    @Transactional
    public LancamentoResponse criar(LancamentoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();

        LancamentoFinanceiro lancamento = lancamentoMapper.toEntity(request);
        lancamento.setTenantId(tenantId);

        // Vínculos Opcionais (se passados, devemos garantir que pertencem ao tenant)
        if (request.getVeiculoId() != null) {
            lancamento.setVeiculo(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                    .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId())));
        }

        if (request.getContratoId() != null) {
            lancamento.setContrato(contratoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getContratoId(), tenantId)
                    .orElseThrow(() -> new ResourceNotFoundException("Contrato", "id", request.getContratoId())));
        }

        lancamento = lancamentoRepository.save(lancamento);
        log.info("Lançamento financeiro {} ({}) registrado. (Tenant: {})", 
                 lancamento.getTipo(), lancamento.getValor(), tenantId);

        return lancamentoMapper.toResponse(lancamento);
    }

    /**
     * Lista lançamentos paginados para o extrato da locadora.
     */
    @Transactional(readOnly = true)
    public PagedResponse<LancamentoResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        
        Page<LancamentoFinanceiro> page = lancamentoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<LancamentoResponse> data = page.getContent().stream()
                .map(lancamentoMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    /**
     * Apura o fluxo de caixa de um determinado mês e ano usando agregação otimizada no banco.
     */
    @Transactional(readOnly = true)
    public FluxoCaixaResponse obterFluxoMensal(int ano, int mes) {
        UUID tenantId = TenantContext.requireTenantId();

        LocalDate inicio = LocalDate.of(ano, mes, 1);
        LocalDate fim = inicio.withDayOfMonth(inicio.lengthOfMonth());

        BigDecimal receitas = lancamentoRepository.sumValorByTipoAndStatusAndPeriodo(
                tenantId, TipoTransacao.RECEITA, StatusPagamento.PAGO, inicio, fim);
        
        BigDecimal despesas = lancamentoRepository.sumValorByTipoAndStatusAndPeriodo(
                tenantId, TipoTransacao.DESPESA, StatusPagamento.PAGO, inicio, fim);

        // Trata nulos gerados pelo SUM do banco vazio
        receitas = (receitas == null) ? BigDecimal.ZERO : receitas;
        despesas = (despesas == null) ? BigDecimal.ZERO : despesas;
        BigDecimal saldoLiquido = receitas.subtract(despesas);

        return FluxoCaixaResponse.builder()
                .ano(ano)
                .mes(mes)
                .totalReceitas(receitas)
                .totalDespesas(despesas)
                .saldoLiquido(saldoLiquido)
                .build();
    }
}
