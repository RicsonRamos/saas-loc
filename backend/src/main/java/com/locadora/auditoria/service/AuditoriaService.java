package com.locadora.auditoria.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.locadora.auditoria.dto.AuditoriaResponse;
import com.locadora.auditoria.entity.Auditoria;
import com.locadora.auditoria.repository.AuditoriaRepository;
import com.locadora.common.dto.PagedResponse;
import jakarta.servlet.http.HttpServletRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import java.util.List;
import java.util.UUID;

import com.locadora.shared.tenant.TenantContext;

@Service
public class AuditoriaService {

    private static final Logger log = LoggerFactory.getLogger(AuditoriaService.class);

    private final AuditoriaRepository repository;
    private final ObjectMapper objectMapper;

    public AuditoriaService(AuditoriaRepository repository, ObjectMapper objectMapper) {
        this.repository = repository;
        this.objectMapper = objectMapper;
    }

    @Transactional
    public void registrar(String acao, String entidade, UUID entidadeId, Object oldData, Object newData) {
        // 1. Obter usuário autenticado
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String usuario = (auth != null && auth.isAuthenticated() && !auth.getPrincipal().equals("anonymousUser"))
                ? auth.getName()
                : "SISTEMA";

        // 2. Obter IP e User-Agent do RequestContext
        String ip = "0.0.0.0";
        String userAgent = "N/A";
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        if (attributes != null) {
            HttpServletRequest request = attributes.getRequest();
            ip = request.getRemoteAddr();
            userAgent = request.getHeader("User-Agent");
        }

        // 3. Obter ou criar Correlation ID
        String correlationId = MDC.get("correlationId");
        if (correlationId == null || correlationId.isEmpty()) {
            correlationId = UUID.randomUUID().toString().substring(0, 8);
        }

        // 4. Serializar JSONs
        String oldDataJson = null;
        String newDataJson = null;
        try {
            if (oldData != null) {
                oldDataJson = objectMapper.writeValueAsString(oldData);
            }
            if (newData != null) {
                newDataJson = objectMapper.writeValueAsString(newData);
            }
        } catch (Exception e) {
            log.warn("Erro ao serializar dados de auditoria para ação {}: {}", acao, e.getMessage());
        }

        Auditoria audit = Auditoria.builder()
                .usuario(usuario)
                .acao(acao)
                .entidade(entidade)
                .entidadeId(entidadeId)
                .oldData(oldDataJson)
                .newData(newDataJson)
                .ip(ip)
                .userAgent(userAgent)
                .correlationId(correlationId)
                .tenantId(TenantContext.getTenantId())
                .build();

        repository.save(audit);
        log.info("[AUDIT] Registro gravado: {} | Ação: {} | Por: {}", entidade, acao, usuario);
    }

    @Transactional(readOnly = true)
    public PagedResponse<AuditoriaResponse> listar(Pageable pageable) {
        Page<Auditoria> page = repository.findByTenantIdOrderByCreatedAtDesc(TenantContext.getTenantId(), pageable);
        List<AuditoriaResponse> data = page.getContent().stream()
                .map(this::mapToResponse)
                .toList();

        return PagedResponse.of(data, page.getNumber(), page.getSize(), page.getTotalElements(), page.getTotalPages());
    }

    private AuditoriaResponse mapToResponse(Auditoria entity) {
        return AuditoriaResponse.builder()
                .id(entity.getId())
                .usuario(entity.getUsuario())
                .acao(entity.getAcao())
                .entidade(entity.getEntidade())
                .entidadeId(entity.getEntidadeId())
                .oldData(entity.getOldData())
                .newData(entity.getNewData())
                .ip(entity.getIp())
                .userAgent(entity.getUserAgent())
                .correlationId(entity.getCorrelationId())
                .tenantId(entity.getTenantId())
                .createdAt(entity.getCreatedAt())
                .build();
    }
}
