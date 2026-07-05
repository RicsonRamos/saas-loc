package com.locadora.common.security;

import com.locadora.shared.tenant.TenantContext;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;

/**
 * Filtro responsável por auditar todas as requisições recebidas pela API,
 * logando qual usuário e de qual tenant executou qual operação.
 */
@Component
public class AuditLoggerFilter extends OncePerRequestFilter {

    private static final Logger log = LoggerFactory.getLogger("AUDIT");

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = (auth != null && auth.isAuthenticated() && !auth.getPrincipal().equals("anonymousUser")) 
                ? auth.getName() 
                : "ANONIMO";
                
        String tenant = TenantContext.getTenantId() != null ? TenantContext.getTenantId().toString() : "SEM_TENANT";

        log.info("[AUDIT] Usuário: {} | Tenant: {} | Rota: {} {} | IP: {}", 
                username, tenant, request.getMethod(), request.getRequestURI(), request.getRemoteAddr());

        filterChain.doFilter(request, response);
    }
}
