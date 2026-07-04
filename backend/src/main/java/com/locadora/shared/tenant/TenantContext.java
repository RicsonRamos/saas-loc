package com.locadora.shared.tenant;

import java.util.UUID;

/**
 * Contexto do tenant usando ThreadLocal.
 * Conforme 07-segurança.md: o tenant é obtido exclusivamente do usuário autenticado.
 * Nunca confiar no tenant enviado pelo frontend.
 */
public final class TenantContext {

    private static final ThreadLocal<UUID> CURRENT_TENANT = new ThreadLocal<>();

    private TenantContext() {
        // Utility class
    }

    public static void setTenantId(UUID tenantId) {
        CURRENT_TENANT.set(tenantId);
    }

    public static UUID getTenantId() {
        return CURRENT_TENANT.get();
    }

    public static void clear() {
        CURRENT_TENANT.remove();
    }

    public static UUID requireTenantId() {
        UUID tenantId = CURRENT_TENANT.get();
        if (tenantId == null) {
            throw new IllegalStateException("Tenant ID não definido no contexto");
        }
        return tenantId;
    }
}
