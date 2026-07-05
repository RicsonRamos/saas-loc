package com.locadora.manutencao.service;

import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.manutencao.dto.ConclusaoManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoResponse;
import com.locadora.manutencao.entity.Manutencao;
import com.locadora.manutencao.mapper.ManutencaoMapper;
import com.locadora.manutencao.repository.ManutencaoRepository;
import com.locadora.shared.tenant.TenantContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.List;
import java.util.UUID;

/**
 * Serviço responsável por orquestrar idas e vindas da oficina.
 * Controla o status do veículo e lança custos automaticamente no financeiro.
 */
@Service
public class ManutencaoService {

    private static final Logger log = LoggerFactory.getLogger(ManutencaoService.class);

    private final ManutencaoRepository manutencaoRepository;
    private final ManutencaoMapper manutencaoMapper;
    private final VeiculoRepository veiculoRepository;
    private final FinanceiroService financeiroService;

    public ManutencaoService(ManutencaoRepository manutencaoRepository,
                             ManutencaoMapper manutencaoMapper,
                             VeiculoRepository veiculoRepository,
                             FinanceiroService financeiroService) {
        this.manutencaoRepository = manutencaoRepository;
        this.manutencaoMapper = manutencaoMapper;
        this.veiculoRepository = veiculoRepository;
        this.financeiroService = financeiroService;
    }

    /**
     * Inicia o registro de manutenção e bloqueia o carro para locação.
     */
    @Transactional
    public ManutencaoResponse iniciar(ManutencaoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();

        Veiculo veiculo = veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

        if (veiculo.getStatus() == StatusVeiculo.LOCADO) {
            throw new BusinessException("Não é possível enviar um carro LOCADO para a oficina. Encerre o contrato primeiro.");
        }

        // Bloqueia veículo na frota
        veiculo.setStatus(StatusVeiculo.MANUTENCAO);
        veiculoRepository.save(veiculo);

        Manutencao manutencao = manutencaoMapper.toEntity(request);
        manutencao.setTenantId(tenantId);
        manutencao.setVeiculo(veiculo);
        manutencao.setKmManutencao(veiculo.getQuilometragem());
        
        manutencao = manutencaoRepository.save(manutencao);
        log.info("Veiculo {} enviado para manutenção. (Tenant: {})", veiculo.getPlaca(), tenantId);

        return manutencaoMapper.toResponse(manutencao);
    }

    /**
     * Conclui o serviço, libera o carro e debita o caixa.
     */
    @Transactional
    public ManutencaoResponse concluir(UUID id, ConclusaoManutencaoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();

        Manutencao manutencao = manutencaoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Manutencao", "id", id));

        if (manutencao.isConcluida()) {
            throw new BusinessException("Esta manutenção já foi concluída.");
        }

        manutencao.setConcluida(true);
        manutencao.setDataFim(request.getDataFim());
        manutencao.setCusto(request.getCusto());

        if (request.getDetalhesAdicionais() != null && !request.getDetalhesAdicionais().isBlank()) {
            manutencao.setDescricao(manutencao.getDescricao() + " | Adicional: " + request.getDetalhesAdicionais());
        }

        // Libera veículo na frota
        Veiculo veiculo = manutencao.getVeiculo();
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculoRepository.save(veiculo);

        manutencao = manutencaoRepository.save(manutencao);

        // Gera a despesa financeira automaticamente se houve custo
        if (request.getCusto() != null && request.getCusto().compareTo(BigDecimal.ZERO) > 0) {
            LancamentoRequest despesa = new LancamentoRequest(
                    TipoTransacao.DESPESA,
                    request.getCusto(),
                    CategoriaFinanceira.MANUTENCAO,
                    "Pagamento de oficina (Manutenção " + manutencao.getId() + ")",
                    StatusPagamento.PAGO,
                    request.getDataFim(),
                    request.getDataFim(),
                    veiculo.getId(),
                    null
            );
            financeiroService.criar(despesa);
            log.info("Despesa de oficina lançada no caixa para veículo {}. (Tenant: {})", veiculo.getPlaca(), tenantId);
        }

        return manutencaoMapper.toResponse(manutencao);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ManutencaoResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        Page<Manutencao> page = manutencaoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<ManutencaoResponse> data = page.getContent().stream().map(manutencaoMapper::toResponse).toList();
        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public PagedResponse<ManutencaoResponse> listarPorVeiculo(UUID veiculoId, Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        Page<Manutencao> page = manutencaoRepository.findByVeiculoIdAndTenantIdAndDeletedAtIsNull(veiculoId, tenantId, pageable);
        List<ManutencaoResponse> data = page.getContent().stream().map(manutencaoMapper::toResponse).toList();
        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }
}
