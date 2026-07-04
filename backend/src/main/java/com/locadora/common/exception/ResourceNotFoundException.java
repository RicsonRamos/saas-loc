package com.locadora.common.exception;

public class ResourceNotFoundException extends RuntimeException {

    public ResourceNotFoundException(String resource, String field, Object value) {
        super(String.format("%s não encontrado com %s: %s", resource, field, value));
    }

    public ResourceNotFoundException(String message) {
        super(message);
    }
}
