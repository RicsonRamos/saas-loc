package com.locadora.alerta.service;

import com.locadora.alerta.dto.AlertaResponse;
import com.locadora.alerta.entity.Alerta;
import com.locadora.alerta.entity.TipoAlerta;
import com.locadora.alerta.repository.AlertaRepository;
import com.locadora.cliente.entity.Cliente;
import com.locadora.cliente.repository.ClienteRepository;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.entity.DocumentoVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.DocumentoVeiculoRepository;
import com.locadora.frota.repository.VeiculoRepository;
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
    private final VeiculoRepository veiculoRepository;
    private final DocumentoVeiculoRepository documentoVeiculoRepository;

    public AlertaService(AlertaRepository repository,
                         ClienteRepository clienteRepository,
                         VeiculoRepository veiculoRepository,
                         DocumentoVeiculoRepository documentoVeiculoRepository) {
        this.repository = repository;
        this.clienteRepository = clienteRepository;
        this.veiculoRepository = veiculoRepository;
        this.documentoVeiculoRepository = documentoVeiculoRepository;
    }

    @Transactional(readOnly = true)
    public List<AlertaResponse> obterPendentes() {
        return repository.findByLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc().stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Transactional(readOnly = true)
    public List<AlertaResponse> obterTodos() {
        return repository.findByDeletedAtIsNullOrderByDataAlertaDesc().stream()
                .map(this::mapToResponse)
                .toList();
    }

    @Transactional
    public void marcarComoLido(UUID id) {
        Alerta alerta = repository.findByIdAndDeletedAtIsNull(id)
                .orElseThrow(() -> new ResourceNotFoundException("Alerta", "id", id));
        alerta.setLido(true);
        repository.save(alerta);
        log.info("Alerta {} marcado como lido.", id);
    }

    @Transactional
    public void marcarTodosComoLidos() {
        List<Alerta> pendentes = repository.findByLidoFalseAndDeletedAtIsNullOrderByDataAlertaDesc();
        pendentes.forEach(alerta -> alerta.setLido(true));
        repository.saveAll(pendentes);
        log.info("Todos os alertas pendentes foram marcados como lidos.");
    }

    @Transactional
    public void criarAlerta(TipoAlerta tipo, String titulo, String descricao, UUID entidadeId) {
        if (repository.existsByTipoAndEntidadeIdAndLidoFalseAndDeletedAtIsNull(tipo, entidadeId)) {
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
        log.info("Iniciando varredura automatizada para geração de alertas...");

        LocalDate limite30Dias = LocalDate.now().plusDays(30);

        // 1. Verificar CNH de Clientes
        List<Cliente> clientes = clienteRepository.findByDeletedAtIsNull(org.springframework.data.domain.Pageable.unpaged()).getContent();
        for (Cliente c : clientes) {
            if (c.getCnhValidade() != null && c.getCnhValidade().isBefore(limite30Dias)) {
                String desc = "A CNH do cliente " + c.getNome() + " vence em " + c.getCnhValidade();
                criarAlerta(TipoAlerta.CNH, "CNH Próxima ao Vencimento", desc, c.getId());
            }
        }

        // 2. Verificar Documentos de Veículos (IPVA, Seguro, Licenciamento)
        List<DocumentoVeiculo> documentos = documentoVeiculoRepository.findByDeletedAtIsNullAndValidadeBetween(LocalDate.now().minusYears(1), limite30Dias);
        for (DocumentoVeiculo doc : documentos) {
            String desc = "O documento de " + doc.getTipo() + " do veículo de placa " + doc.getVeiculo().getPlaca() + " vence em " + doc.getValidade();
            criarAlerta(TipoAlerta.valueOf(doc.getTipo().name()), "Vencimento de Documento de Veículo", desc, doc.getVeiculo().getId());
        }

        log.info("Varredura de alertas concluída.");
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
