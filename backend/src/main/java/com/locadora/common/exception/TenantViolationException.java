package com.locadora.common.exception;

/**
 * Exceção lançada quando ocorre violação de isolamento multi-tenant.
 */
public class TenantViolationException extends RuntimeException {

    public TenantViolationException() {
        super("Violação de acesso: operação entre tenants não permitida");
    }

    public TenantViolationException(String message) {
        super(message);
    }
}
