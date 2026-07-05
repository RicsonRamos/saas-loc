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
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
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
 * Serviço responsável por toda a lógica de negócio de Contratos.
 * Orquestra o ciclo de vida da locação, acerto de quilometragem e o status do veículo na frota.
 */
@Service
public class ContratoService {

    private static final Logger log = LoggerFactory.getLogger(ContratoService.class);

    private final ContratoRepository contratoRepository;
    private final ContratoMapper contratoMapper;
    private final ClienteRepository clienteRepository;
    private final VeiculoRepository veiculoRepository;

    public ContratoService(ContratoRepository contratoRepository, 
                           ContratoMapper contratoMapper, 
                           ClienteRepository clienteRepository, 
                           VeiculoRepository veiculoRepository) {
        this.contratoRepository = contratoRepository;
        this.contratoMapper = contratoMapper;
        this.clienteRepository = clienteRepository;
        this.veiculoRepository = veiculoRepository;
    }

    /**
     * Cria um novo contrato e efetiva a locação do veículo.
     *
     * @param request Payload com os dados estipulados para a locação.
     * @return O contrato já persistido e mapeado.
     */
    @Transactional
    public ContratoResponse criar(ContratoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();

        // 1. Validar e Buscar Entidades (Cliente e Veículo)
        Cliente cliente = clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getClienteId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Cliente", "id", request.getClienteId()));

        Veiculo veiculo = veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

        // 2. Regra de Negócio: Verificar se Veículo está disponível para locação
        if (veiculo.getStatus() != StatusVeiculo.DISPONIVEL) {
            throw new BusinessException("O veículo selecionado não está disponível para locação. Status atual: " + veiculo.getStatus());
        }

        // 3. Regra de Negócio: Verificar se já existe contrato ativo para o veículo
        if (contratoRepository.existsByVeiculoIdAndStatusAndTenantIdAndDeletedAtIsNull(veiculo.getId(), StatusContrato.ATIVO, tenantId)) {
            throw new BusinessException("O veículo selecionado já possui um contrato ativo.");
        }

        // 4. Instanciar o Contrato
        Contrato contrato = contratoMapper.toEntity(request);
        contrato.setTenantId(tenantId);
        contrato.setCliente(cliente);
        contrato.setVeiculo(veiculo);
        contrato.setStatus(StatusContrato.ATIVO);
        
        // Congela o Hodômetro atual do carro no contrato
        contrato.setKmInicial(veiculo.getQuilometragem());
        
        // 5. Atualizar Status do Veículo na Frota
        veiculo.setStatus(StatusVeiculo.LOCADO);
        veiculoRepository.save(veiculo);

        // 6. Salvar Contrato
        contrato = contratoRepository.save(contrato);
        log.info("Contrato {} criado com sucesso. (Veículo: {}, Cliente: {}, Tenant: {})", 
                 contrato.getId(), veiculo.getPlaca(), cliente.getDocumento(), tenantId);

        return contratoMapper.toResponse(contrato);
    }

    /**
     * Lista contratos de forma paginada para a locadora.
     */
    @Transactional(readOnly = true)
    public PagedResponse<ContratoResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.requireTenantId();
        
        Page<Contrato> page = contratoRepository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<ContratoResponse> data = page.getContent().stream()
                .map(contratoMapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    /**
     * Busca os detalhes de um contrato isolando o cruzamento de locadoras.
     */
    @Transactional(readOnly = true)
    public ContratoResponse buscarPorId(UUID id) {
        return contratoMapper.toResponse(obterContratoPorId(id));
    }

    /**
     * Encerra um contrato (Checkout da Locação).
     * <p>Recebe a devolução das chaves, o hodômetro final, acerta os valores 
     * adicionais e libera o veículo novamente para a frota.</p>
     *
     * @param id O ID do contrato a ser finalizado.
     * @param request O payload com os dados de encerramento.
     * @return Contrato finalizado.
     */
    @Transactional
    public ContratoResponse encerrar(UUID id, EncerramentoContratoRequest request) {
        UUID tenantId = TenantContext.requireTenantId();
        Contrato contrato = obterContratoPorId(id);

        if (contrato.getStatus() != StatusContrato.ATIVO) {
            throw new BusinessException("Apenas contratos ATIVOS podem ser encerrados.");
        }

        if (request.getKmFinal() < contrato.getKmInicial()) {
            throw new BusinessException("A quilometragem final não pode ser menor que a inicial (" + contrato.getKmInicial() + " km).");
        }

        // 1. Atualizar Contrato
        contrato.setStatus(StatusContrato.ENCERRADO);
        contrato.setDataDevolucao(request.getDataDevolucao());
        contrato.setKmFinal(request.getKmFinal());
        
        // Em um sistema real complexo haveria cálculo automático (franquia de KM), 
        // mas aqui vamos apenas armazenar o quanto o usuário digitou ou calculou no frontend (opcional)
        if (request.getValorAdicional() != null) {
            contrato.setValorAdicional(request.getValorAdicional());
        }

        // 2. Atualizar o Veículo da Frota (Devolver o carro)
        Veiculo veiculo = contrato.getVeiculo();
        veiculo.setQuilometragem(request.getKmFinal());
        veiculo.setStatus(StatusVeiculo.DISPONIVEL); // Libera o veículo
        veiculoRepository.save(veiculo);

        // 3. Persistir e finalizar
        contrato = contratoRepository.save(contrato);
        log.info("Contrato {} encerrado com sucesso. Veículo {} devolvido ao pátio. (Tenant: {})", 
                 contrato.getId(), veiculo.getPlaca(), tenantId);

        return contratoMapper.toResponse(contrato);
    }

    /**
     * Auxiliar interno para obter o contrato garantindo a integridade de permissão do Tenant.
     */
    private Contrato obterContratoPorId(UUID id) {
        UUID tenantId = TenantContext.requireTenantId();
        return contratoRepository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Contrato", "id", id));
    }
}
