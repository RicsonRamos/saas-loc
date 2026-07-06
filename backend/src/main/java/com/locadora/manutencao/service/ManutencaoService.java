package com.locadora.manutencao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.common.dto.PagedResponse;
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
 * Serviço de Manutenção — Multi-Tenant.
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

    @Transactional
    public ManutencaoResponse registrarManutencao(ManutencaoRequest request) {
        Veiculo veiculo = veiculoRepository.findByIdAndDeletedAtIsNull(request.getVeiculoId())
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

        if (veiculo.getStatus() == StatusVeiculo.LOCADO) {
            throw new BusinessException("Veículo está locado e não pode entrar em manutenção.");
        }

        Manutencao manutencao = manutencaoMapper.toEntity(request);
        manutencao.setVeiculo(veiculo);
        manutencao.setKmManutencao(veiculo.getQuilometragem());
        manutencao.setDataInicio(LocalDate.now());

        veiculo.setStatus(StatusVeiculo.MANUTENCAO);
        veiculoRepository.save(veiculo);

        manutencao = manutencaoRepository.save(manutencao);
        log.info("Veículo {} enviado para manutenção.", veiculo.getPlaca());

        return manutencaoMapper.toResponse(manutencao);
    }

    @Transactional
    public ManutencaoResponse concluirManutencao(UUID id, ConclusaoManutencaoRequest request) {
        Manutencao manutencao = manutencaoRepository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("Manutenção", "id", id));

        manutencao.setDataFim(LocalDate.now());
        manutencao.setConcluida(true);

        if (request.getCusto() != null) {
            manutencao.setCusto(request.getCusto());
        }

        Veiculo veiculo = manutencao.getVeiculo();
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculoRepository.save(veiculo);

        manutencao = manutencaoRepository.save(manutencao);

        if (manutencao.getCusto() != null && manutencao.getCusto().compareTo(BigDecimal.ZERO) > 0) {
            LancamentoRequest lancamento = LancamentoRequest.builder()
                    .tipo(TipoTransacao.DESPESA)
                    .valor(manutencao.getCusto())
                    .categoria(CategoriaFinanceira.MANUTENCAO)
                    .descricao("Manutenção do veículo " + veiculo.getPlaca() + " - " + manutencao.getDescricao())
                    .status(StatusPagamento.PAGO)
                    .dataVencimento(LocalDate.now())
                    .dataPagamento(LocalDate.now())
                    .veiculoId(veiculo.getId())
                    .build();
            financeiroService.criarLancamento(lancamento);
            log.info("Despesa de oficina lançada no caixa para veículo {}.", veiculo.getPlaca());
        }

        return manutencaoMapper.toResponse(manutencao);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ManutencaoResponse> listar(Pageable pageable) {
        Page<Manutencao> page = manutencaoRepository.findByTenantIdAndDeletedAtIsNull(pageable);
        List<ManutencaoResponse> data = page.getContent().stream()
                .map(manutencaoMapper::toResponse)
                .toList();
        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public PagedResponse<ManutencaoResponse> listarPorVeiculo(UUID veiculoId, Pageable pageable) {
        Page<Manutencao> page = manutencaoRepository.findByVeiculoIdAndDeletedAtIsNull(veiculoId, pageable);
        List<ManutencaoResponse> data = page.getContent().stream()
                .map(manutencaoMapper::toResponse)
                .toList();
        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }
}
