package com.locadora.shared.tenant;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Testes de isolamento multi-tenant.
 * Conforme SKILL 01 — Multi-Tenant Enforcement.
 */
class TenantContextTest {

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    @DisplayName("deve definir e recuperar tenant_id corretamente")
    void deveDefinirERecuperarTenantId() {
        UUID tenantId = UUID.randomUUID();
        TenantContext.setTenantId(tenantId);

        assertEquals(tenantId, TenantContext.getTenantId());
    }

    @Test
    @DisplayName("deve retornar null quando tenant não definido")
    void deveRetornarNullQuandoNaoDefinido() {
        assertNull(TenantContext.getTenantId());
    }

    @Test
    @DisplayName("deve limpar tenant do contexto")
    void deveLimparTenantDoContexto() {
        UUID tenantId = UUID.randomUUID();
        TenantContext.setTenantId(tenantId);
        TenantContext.clear();

        assertNull(TenantContext.getTenantId());
    }

    @Test
    @DisplayName("deve lançar exceção quando requireTenantId sem tenant definido")
    void deveLancarExcecaoQuandoSemTenant() {
        assertThrows(IllegalStateException.class, TenantContext::requireTenantId);
    }

    @Test
    @DisplayName("deve isolar tenants entre threads diferentes")
    void deveIsolarTenantsEntreThreads() throws InterruptedException {
        UUID tenant1 = UUID.randomUUID();
        UUID tenant2 = UUID.randomUUID();

        TenantContext.setTenantId(tenant1);

        Thread otherThread = new Thread(() -> {
            TenantContext.setTenantId(tenant2);
            assertEquals(tenant2, TenantContext.getTenantId());
            TenantContext.clear();
        });

        otherThread.start();
        otherThread.join();

        // Thread principal mantém seu próprio tenant
        assertEquals(tenant1, TenantContext.getTenantId());
    }
}
