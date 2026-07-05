package com.locadora.alerta.service;

import com.locadora.alerta.dto.AlertaResponse;
import com.locadora.alerta.entity.Alerta;
import com.locadora.alerta.entity.TipoAlerta;
import com.locadora.alerta.repository.AlertaRepository;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.entity.DocumentoVeiculo;
import com.locadora.frota.repository.DocumentoVeiculoRepository;
import com.locadora.shared.tenant.TenantContext;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

@Service
public class AlertaService {

    private static final Logger log = LoggerFactory.getLogger(AlertaService.class);

    private final AlertaRepository repository;
    private final ClienteRepository clienteRepository;
    private final DocumentoVeiculoRepository documentoVeiculoRepository;
    private final UsuarioRepository usuarioRepository;

    public AlertaService(AlertaRepository repository,
                         ClienteRepository clienteRepository,
                         DocumentoVeiculoRepository documentoVeiculoRepository,
                         UsuarioRepository usuarioRepository) {
        this.repository = repository;
        this.clienteRepository = clienteRepository;
        this.documentoVeiculoRepository = documentoVeiculoRepository;
        this.usuarioRepository = usuarioRepository;
    }

    @Transactional(readOnly = true)
    public List<AlertaResponse> obterPendentes() {
        return repository.findByTenantIdAndLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc(TenantContext.getTenantId()).stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<AlertaResponse> obterTodos() {
        return repository.findByTenantIdAndDeletedAtIsNullOrderByDataAlertaDesc(TenantContext.getTenantId()).stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Transactional
    public void marcarComoLido(UUID id) {
        Alerta alerta = repository.findByIdAndTenantIdAndDeletedAtIsNull(id, TenantContext.getTenantId())
                .orElseThrow(() -> new ResourceNotFoundException("Alerta", "id", id));
        alerta.setLido(true);
        repository.save(alerta);
        log.info("Alerta {} marcado como lido.", id);
    }

    @Transactional
    public void marcarTodosComoLidos() {
        List<Alerta> pendentes = repository.findByTenantIdAndLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc(TenantContext.getTenantId());
        pendentes.forEach(alerta -> alerta.setLido(true));
        repository.saveAll(pendentes);
        log.info("Todos os alertas pendentes foram marcados como lidos.");
    }

    @Transactional
    public void criarAlerta(TipoAlerta tipo, String titulo, String descricao, UUID entidadeId) {
        UUID tenantId = TenantContext.getTenantId();
        if (repository.existsByTipoAndEntidadeIdAndLidoFalseAndTenantIdAndDeletedAtIsNull(tipo, entidadeId, tenantId)) {
            // Evita criar alertas duplicados idênticos ainda não lidos
            return;
        }

        Alerta alerta = Alerta.builder()
                .tipo(tipo)
                .titulo(titulo)
                .descricao(descricao)
                .entidadeId(entidadeId)
                .lido(false)
                .dataAlerta(LocalDate.now())
                .build();
        alerta.setTenantId(tenantId);

        repository.save(alerta);
        log.info("Alerta gerado: {} - {}", titulo, tipo);
    }

    /**
     * Varredura diária automática para gerar alertas de CNH vencendo e documentos vencendo.
     * Roda à meia-noite todos os dias.
     */
    @Scheduled(cron = "0 0 0 * * ?")
    @Transactional
    public void verificarEPontuarAlertas() {
        log.info("Iniciando varredura automatizada para geração de alertas multi-tenant...");

        // Busca todos os tenants distintos cadastrados no sistema através dos usuários
        List<UUID> tenantIds = usuarioRepository.findAll().stream()
                .map(Usuario::getTenantId)
                .filter(java.util.Objects::nonNull)
                .distinct()
                .toList();

        for (UUID tenantId : tenantIds) {
            try {
                TenantContext.setTenantId(tenantId);
                verificarEPontuarAlertasParaTenant(tenantId);
            } catch (Exception e) {
                log.error("Erro ao processar alertas para o tenant {}: {}", tenantId, e.getMessage());
            } finally {
                TenantContext.clear();
            }
        }
        log.info("Varredura de alertas concluída.");
    }

    private void verificarEPontuarAlertasParaTenant(UUID tenantId) {
        LocalDate limite30Dias = LocalDate.now().plusDays(30);

        // 1. Verificar CNH de Clientes
        List<Cliente> clientes = clienteRepository.findByTenantIdAndDeletedAtIsNull(tenantId, org.springframework.data.domain.Pageable.unpaged()).getContent();
        for (Cliente c : clientes) {
            if (c.getCnhValidade() != null && c.getCnhValidade().isBefore(limite30Dias)) {
                String desc = "A CNH do cliente " + c.getNome() + " vence em " + c.getCnhValidade();
                criarAlerta(TipoAlerta.CNH, "CNH Próxima ao Vencimento", desc, c.getId());
            }
        }

        // 2. Verificar Documentos de Veículos (IPVA, Seguro, Licenciamento)
        List<DocumentoVeiculo> documentos = documentoVeiculoRepository.findByTenantIdAndDeletedAtIsNullAndValidadeBetween(tenantId, LocalDate.now().minusYears(1), limite30Dias);
        for (DocumentoVeiculo doc : documentos) {
            String desc = "O documento de " + doc.getTipo() + " do veículo de placa " + doc.getVeiculo().getPlaca() + " vence em " + doc.getValidade();
            criarAlerta(TipoAlerta.valueOf(doc.getTipo().name()), "Vencimento de Documento de Veículo", desc, doc.getVeiculo().getId());
        }
    }

    private AlertaResponse mapToResponse(Alerta entity) {
        return AlertaResponse.builder()
                .id(entity.getId())
                .tipo(entity.getTipo())
                .titulo(entity.getTitulo())
                .descricao(entity.getDescricao())
                .entidadeId(entity.getEntidadeId())
                .lido(entity.getLido())
                .dataAlerta(entity.getDataAlerta())
                .createdAt(entity.getCreatedAt())
                .build();
    }
}
