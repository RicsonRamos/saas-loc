package com.locadora.common.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Filtro de Rate Limiting IN-MEMORY (MVP).
 * Limita o número de requisições por IP para prevenir ataques de negação de serviço e força bruta.
 */
@Component
public class RateLimitingFilter extends OncePerRequestFilter {

    private static final int MAX_REQUESTS_PER_MINUTE = 150;
    
    // Armazena [IP -> [Count, Timestamp]]
    private final ConcurrentHashMap<String, RateLimitTracker> buckets = new ConcurrentHashMap<>();

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain)
            throws ServletException, IOException {

        String ip = getClientIP(request);
        long currentTime = System.currentTimeMillis();

        buckets.compute(ip, (key, tracker) -> {
            if (tracker == null || currentTime - tracker.timestamp > 60000) {
                // Reseta se passou 1 minuto ou se é novo
                return new RateLimitTracker(1, currentTime);
            }
            tracker.count++;
            return tracker;
        });

        RateLimitTracker tracker = buckets.get(ip);
        if (tracker.count > MAX_REQUESTS_PER_MINUTE) {
            response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            response.getWriter().write("Too Many Requests. Rate limit exceeded.");
            return; // Bloqueia a request
        }

        filterChain.doFilter(request, response);
    }

    private String getClientIP(HttpServletRequest request) {
        String xfHeader = request.getHeader("X-Forwarded-For");
        if (xfHeader == null) {
            return request.getRemoteAddr();
        }
        return xfHeader.split(",")[0];
    }

    private static class RateLimitTracker {
        int count;
        long timestamp;

        RateLimitTracker(int count, long timestamp) {
            this.count = count;
            this.timestamp = timestamp;
        }
    }
}
