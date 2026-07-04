package com.locadora.security.jwt;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Testes do JwtTokenProvider.
 * Conforme SKILL 05 — Test-First Execution.
 */
class JwtTokenProviderTest {

    private JwtTokenProvider jwtTokenProvider;

    private static final String SECRET = "test-secret-key-must-be-at-least-256-bits-long-for-hmac-sha256-algorithm";
    private static final long ACCESS_EXPIRATION = 900000L; // 15 min
    private static final long REFRESH_EXPIRATION = 604800000L; // 7 days

    @BeforeEach
    void setUp() {
        jwtTokenProvider = new JwtTokenProvider(SECRET, ACCESS_EXPIRATION, REFRESH_EXPIRATION);
    }

    @Test
    @DisplayName("deve gerar access token válido")
    void deveGerarAccessTokenValido() {
        UUID userId = UUID.randomUUID();
        UUID tenantId = UUID.randomUUID();
        String email = "admin@locadora.com";

        String token = jwtTokenProvider.generateAccessToken(userId, tenantId, email);

        assertNotNull(token);
        assertTrue(jwtTokenProvider.validateToken(token));
        assertEquals(userId, jwtTokenProvider.getUserIdFromToken(token));
        assertEquals(tenantId, jwtTokenProvider.getTenantIdFromToken(token));
        assertEquals(email, jwtTokenProvider.getEmailFromToken(token));
        assertEquals("ACCESS", jwtTokenProvider.getTokenType(token));
    }

    @Test
    @DisplayName("deve gerar refresh token válido")
    void deveGerarRefreshTokenValido() {
        UUID userId = UUID.randomUUID();
        UUID tenantId = UUID.randomUUID();
        String email = "admin@locadora.com";

        String token = jwtTokenProvider.generateRefreshToken(userId, tenantId, email);

        assertNotNull(token);
        assertTrue(jwtTokenProvider.validateToken(token));
        assertEquals("REFRESH", jwtTokenProvider.getTokenType(token));
    }

    @Test
    @DisplayName("deve retornar false para token inválido")
    void deveRetornarFalseParaTokenInvalido() {
        assertFalse(jwtTokenProvider.validateToken("token-invalido"));
    }

    @Test
    @DisplayName("deve retornar false para token nulo")
    void deveRetornarFalseParaTokenNulo() {
        assertFalse(jwtTokenProvider.validateToken(null));
    }

    @Test
    @DisplayName("deve conter tenant_id no token")
    void deveConterTenantIdNoToken() {
        UUID userId = UUID.randomUUID();
        UUID tenantId = UUID.randomUUID();
        String email = "test@test.com";

        String token = jwtTokenProvider.generateAccessToken(userId, tenantId, email);

        UUID extractedTenantId = jwtTokenProvider.getTenantIdFromToken(token);
        assertEquals(tenantId, extractedTenantId);
    }

    @Test
    @DisplayName("deve diferenciar access token de refresh token")
    void deveDiferenciarAccessDeRefresh() {
        UUID userId = UUID.randomUUID();
        UUID tenantId = UUID.randomUUID();
        String email = "test@test.com";

        String accessToken = jwtTokenProvider.generateAccessToken(userId, tenantId, email);
        String refreshToken = jwtTokenProvider.generateRefreshToken(userId, tenantId, email);

        assertEquals("ACCESS", jwtTokenProvider.getTokenType(accessToken));
        assertEquals("REFRESH", jwtTokenProvider.getTokenType(refreshToken));
        assertNotEquals(accessToken, refreshToken);
    }
}
