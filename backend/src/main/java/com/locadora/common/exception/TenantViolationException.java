package com.locadora.common.exception;

/**
 * Violação de isolamento multi-tenant.
 * Conforme 07-segurança.md: é proibido permitir acesso cruzado entre empresas.
 */
public class TenantViolationException extends RuntimeException {

    public TenantViolationException() {
        super("Violação de acesso: operação entre tenants não permitida");
    }

    public TenantViolationException(String message) {
        super(message);
    }
}
