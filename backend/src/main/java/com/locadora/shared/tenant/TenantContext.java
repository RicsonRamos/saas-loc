package com.locadora.shared.tenant;

import java.util.UUID;

/**
 * Armazena e expõe o tenantId do contexto da requisição atual usando ThreadLocal.
 */
public class TenantContext {

    private static final ThreadLocal<UUID> CONTEXT = new ThreadLocal<>();

    public static void setTenantId(UUID tenantId) {
        CONTEXT.set(tenantId);
    }

    public static UUID getTenantId() {
        return CONTEXT.get();
    }

    public static void clear() {
        CONTEXT.remove();
    }
}
