package com.locadora.contrato.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.contrato.dto.ContratoRequest;
import com.locadora.contrato.dto.ContratoResponse;
import com.locadora.contrato.dto.EncerramentoContratoRequest;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import com.locadora.contrato.mapper.ContratoMapper;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
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

import com.locadora.shared.tenant.TenantContext;

/**
 * Serviço de Contratos — Multi-Tenant.
 * Orquestra o ciclo de vida da locação, quilometragem e status do veículo.
 */
@Service
public class ContratoService {

    private static final Logger log = LoggerFactory.getLogger(ContratoService.class);

    private final ContratoRepository contratoRepository;
    private final ContratoMapper contratoMapper;
    private final ClienteRepository clienteRepository;
    private final VeiculoRepository veiculoRepository;
    private final FinanceiroService financeiroService;

    public ContratoService(ContratoRepository contratoRepository,
                           ContratoMapper contratoMapper,
                           ClienteRepository clienteRepository,
                           VeiculoRepository veiculoRepository,
                           FinanceiroService financeiroService) {
        this.contratoRepository = contratoRepository;
        this.contratoMapper = contratoMapper;
        this.clienteRepository = clienteRepository;
        this.veiculoRepository = veiculoRepository;
        this.financeiroService = financeiroService;
    }

    @Transactional
    public ContratoResponse abrirContrato(ContratoRequest request) {
        UUID tenantId = TenantContext.getTenantId();

        Cliente cliente = clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getClienteId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Cliente", "id", request.getClienteId()));

        Veiculo veiculo = veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

        if (veiculo.getStatus() != StatusVeiculo.DISPONIVEL) {
            throw new BusinessException("O veículo selecionado não está disponível para locação. Status atual: " + veiculo.getStatus());
        }

        if (contratoRepository.existsByVeiculoIdAndStatusAndTenantIdAndDeletedAtIsNull(veiculo.getId(), StatusContrato.ATIVO, tenantId)) {
            throw new BusinessException("O veículo selecionado já possui um contrato ativo.");
        }

        Contrato contrato = contratoMapper.toEntity(request);
        contrato.setCliente(cliente);
        contrato.setVeiculo(veiculo);
        contrato.setStatus(StatusContrato.ATIVO);
        contrato.setKmInicial(veiculo.getQuilometragem());

        veiculo.setStatus(StatusVeiculo.LOCADO);
        veiculoRepository.save(veiculo);

        contrato = contratoRepository.save(contrato);
        log.info("Contrato {} criado. Veículo: {}, Cliente: {}", contrato.getId(), veiculo.getPlaca(), cliente.getDocumento());

        return contratoMapper.toResponse(contrato);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ContratoResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.getTenantId();
        Page<Contrato> page = contratoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<ContratoResponse> data = page.getContent().stream()
                .map(contratoMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public ContratoResponse buscarPorId(UUID id) {
        return contratoMapper.toResponse(obterContratoPorId(id));
    }

    @Transactional
    public ContratoResponse encerrar(UUID id, EncerramentoContratoRequest request) {
        Contrato contrato = obterContratoPorId(id);

        if (contrato.getStatus() != StatusContrato.ATIVO) {
            throw new BusinessException("Apenas contratos ATIVOS podem ser encerrados.");
        }

        if (request.getKmFinal() < contrato.getKmInicial()) {
            throw new BusinessException("A quilometragem final não pode ser menor que a inicial (" + contrato.getKmInicial() + " km).");
        }

        contrato.setStatus(StatusContrato.ENCERRADO);
        contrato.setDataDevolucao(request.getDataDevolucao());
        contrato.setKmFinal(request.getKmFinal());

        if (request.getValorAdicional() != null) {
            contrato.setValorAdicional(request.getValorAdicional());
        }

        Veiculo veiculo = contrato.getVeiculo();
        veiculo.setQuilometragem(request.getKmFinal());
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculoRepository.save(veiculo);

        contrato = contratoRepository.save(contrato);

        BigDecimal valorAcerto = contrato.getValorTotal().add(contrato.getValorAdicional());
        LancamentoRequest lancamentoRequest = LancamentoRequest.builder()
                .tipo(TipoTransacao.RECEITA)
                .valor(valorAcerto)
                .categoria(CategoriaFinanceira.ALUGUEL)
                .descricao("Recebimento referente ao contrato " + contrato.getId())
                .status(StatusPagamento.PAGO)
                .dataVencimento(LocalDate.now())
                .dataPagamento(LocalDate.now())
                .veiculoId(veiculo.getId())
                .contratoId(contrato.getId())
                .build();
        financeiroService.criarLancamento(lancamentoRequest);

        log.info("Contrato {} encerrado. Veículo {} devolvido.", contrato.getId(), veiculo.getPlaca());

        return contratoMapper.toResponse(contrato);
    }

    private Contrato obterContratoPorId(UUID id) {
        return contratoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, TenantContext.getTenantId())
                .orElseThrow(() -> new ResourceNotFoundException("Contrato", "id", id));
    }
}
