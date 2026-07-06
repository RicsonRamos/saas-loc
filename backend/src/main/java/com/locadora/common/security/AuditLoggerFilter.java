package com.locadora.common.security;

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
 * Filtro de auditoria — Multi-Tenant.
 * Registra todas as requisições HTTP com usuário, tenant, método, rota e IP.
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

        log.info("[AUDIT] Usuário: {} | Rota: {} {} | IP: {} | User-Agent: {}",
                username, request.getMethod(), request.getRequestURI(), request.getRemoteAddr(),
                request.getHeader("User-Agent"));

        filterChain.doFilter(request, response);
    }
}
