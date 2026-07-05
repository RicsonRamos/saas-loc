package com.locadora.reserva.service;

import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.dto.PagedResponse;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.StatusContrato;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.reserva.dto.ReservaRequest;
import com.locadora.reserva.dto.ReservaResponse;
import com.locadora.reserva.entity.Reserva;
import com.locadora.reserva.entity.StatusReserva;
import com.locadora.reserva.mapper.ReservaMapper;
import com.locadora.reserva.repository.ReservaRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

import com.locadora.shared.tenant.TenantContext;

@Service
public class ReservaService {

    private static final Logger log = LoggerFactory.getLogger(ReservaService.class);

    private final ReservaRepository repository;
    private final ReservaMapper mapper;
    private final ClienteRepository clienteRepository;
    private final VeiculoRepository veiculoRepository;
    private final ContratoRepository contratoRepository;

    public ReservaService(ReservaRepository repository,
                          ReservaMapper mapper,
                          ClienteRepository clienteRepository,
                          VeiculoRepository veiculoRepository,
                          ContratoRepository contratoRepository) {
        this.repository = repository;
        this.mapper = mapper;
        this.clienteRepository = clienteRepository;
        this.veiculoRepository = veiculoRepository;
        this.contratoRepository = contratoRepository;
    }

    @Transactional
    public ReservaResponse criar(ReservaRequest request) {
        if (request.getDataFim().isBefore(request.getDataInicio())) {
            throw new BusinessException("A data de término não pode ser anterior à data de início.");
        }

        UUID tenantId = TenantContext.getTenantId();

        Cliente cliente = clienteRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getClienteId(), tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Cliente", "id", request.getClienteId()));

        Veiculo veiculo = null;
        if (request.getVeiculoId() != null) {
            veiculo = veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                    .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

            if (repository.existsConflict(veiculo.getId(), request.getDataInicio(), request.getDataFim(), null, tenantId)) {
                throw new BusinessException("O veículo já possui reserva ou aluguel ativo para o período informado.");
            }
        }

        Reserva reserva = mapper.toEntity(request);
        reserva.setCliente(cliente);
        reserva.setVeiculo(veiculo);
        reserva.setStatus(StatusReserva.RESERVADO);

        reserva = repository.save(reserva);
        log.info("Nova reserva criada para o cliente {} (ID: {})", cliente.getNome(), reserva.getId());

        return mapper.toResponse(reserva);
    }

    @Transactional
    public ReservaResponse atualizar(UUID id, ReservaRequest request) {
        UUID tenantId = TenantContext.getTenantId();

        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));

        if (reserva.getStatus() == StatusReserva.CONVERTIDO_EM_CONTRATO || reserva.getStatus() == StatusReserva.FINALIZADO) {
            throw new BusinessException("Reservas concluídas ou convertidas não podem ser alteradas.");
        }

        if (request.getDataFim().isBefore(request.getDataInicio())) {
            throw new BusinessException("A data de término não pode ser anterior à data de início.");
        }

        if (request.getVeiculoId() != null) {
            Veiculo veiculo = veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(request.getVeiculoId(), tenantId)
                    .orElseThrow(() -> new ResourceNotFoundException("Veículo", "id", request.getVeiculoId()));

            if (repository.existsConflict(veiculo.getId(), request.getDataInicio(), request.getDataFim(), id, tenantId)) {
                throw new BusinessException("O veículo já possui reserva ativa para o período informado.");
            }
            reserva.setVeiculo(veiculo);
        } else {
            reserva.setVeiculo(null);
        }

        mapper.updateEntity(request, reserva);
        reserva = repository.save(reserva);
        log.info("Reserva {} atualizada com sucesso.", id);

        return mapper.toResponse(reserva);
    }

    @Transactional
    public ReservaResponse cancelar(UUID id) {
        UUID tenantId = TenantContext.getTenantId();
        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));

        if (reserva.getStatus() == StatusReserva.CONVERTIDO_EM_CONTRATO || reserva.getStatus() == StatusReserva.FINALIZADO) {
            throw new BusinessException("Esta reserva já foi finalizada ou convertida em contrato e não pode ser cancelada.");
        }

        reserva.setStatus(StatusReserva.CANCELADO);
        reserva = repository.save(reserva);
        log.info("Reserva {} cancelada com sucesso.", id);
        return mapper.toResponse(reserva);
    }

    @Transactional
    public ReservaResponse confirmar(UUID id) {
        UUID tenantId = TenantContext.getTenantId();
        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));

        if (reserva.getStatus() != StatusReserva.RESERVADO) {
            throw new BusinessException("Apenas reservas pendentes (RESERVADO) podem ser confirmadas.");
        }

        reserva.setStatus(StatusReserva.CONFIRMADO);
        reserva = repository.save(reserva);
        log.info("Reserva {} confirmada pelo operador.", id);
        return mapper.toResponse(reserva);
    }

    @Transactional
    public void excluir(UUID id, UUID currentUserId) {
        UUID tenantId = TenantContext.getTenantId();
        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));

        reserva.softDelete(currentUserId);
        repository.save(reserva);
        log.info("Reserva {} excluída logicamente.", id);
    }

    @Transactional(readOnly = true)
    public PagedResponse<ReservaResponse> listar(Pageable pageable) {
        UUID tenantId = TenantContext.getTenantId();
        Page<Reserva> page = repository.findByTenantIdAndDeletedAtIsNull(tenantId, pageable);
        List<ReservaResponse> data = page.getContent().stream()
                .map(mapper::toResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    @Transactional(readOnly = true)
    public ReservaResponse buscarPorId(UUID id) {
        UUID tenantId = TenantContext.getTenantId();
        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));
        return mapper.toResponse(reserva);
    }

    @Transactional
    public UUID converterEmContrato(UUID id, BigDecimal valorDiaria) {
        UUID tenantId = TenantContext.getTenantId();
        Reserva reserva = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, tenantId)
                .orElseThrow(() -> new ResourceNotFoundException("Reserva", "id", id));

        if (reserva.getStatus() == StatusReserva.CANCELADO || reserva.getStatus() == StatusReserva.CONVERTIDO_EM_CONTRATO) {
            throw new BusinessException("Reserva não elegível para conversão em contrato.");
        }

        if (reserva.getVeiculo() == null) {
            throw new BusinessException("Por favor, selecione um veículo específico para esta reserva antes de convertê-la.");
        }

        Veiculo veiculo = reserva.getVeiculo();
        if (veiculo.getStatus() != StatusVeiculo.DISPONIVEL) {
            throw new BusinessException("O veículo " + veiculo.getPlaca() + " está indisponível para locação.");
        }

        // 1. Criar e preencher contrato
        Contrato contrato = new Contrato();
        contrato.setCliente(reserva.getCliente());
        contrato.setVeiculo(veiculo);
        contrato.setStatus(StatusContrato.ATIVO);
        contrato.setDataInicio(reserva.getDataInicio());
        contrato.setDataFimPrevista(reserva.getDataFim());
        contrato.setKmInicial(veiculo.getQuilometragem());
        
        // Calcula valor inicial básico (dias * valorDiaria)
        long dias = java.time.temporal.ChronoUnit.DAYS.between(reserva.getDataInicio(), reserva.getDataFim());
        if (dias <= 0) dias = 1;
        contrato.setValorTotal(valorDiaria.multiply(BigDecimal.valueOf(dias)));
        contrato.setValorAdicional(BigDecimal.ZERO);

        contrato = contratoRepository.save(contrato);

        // 2. Bloquear veículo na frota
        veiculo.setStatus(StatusVeiculo.LOCADO);
        veiculoRepository.save(veiculo);

        // 3. Atualizar reserva
        reserva.setStatus(StatusReserva.CONVERTIDO_EM_CONTRATO);
        repository.save(reserva);

        log.info("Reserva {} convertida em Contrato {} com sucesso.", id, contrato.getId());
        return contrato.getId();
    }
}
