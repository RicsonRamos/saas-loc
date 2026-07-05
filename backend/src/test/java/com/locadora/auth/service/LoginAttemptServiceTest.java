package com.locadora.auth.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class LoginAttemptServiceTest {

    private LoginAttemptService loginAttemptService;

    @BeforeEach
    void setUp() {
        loginAttemptService = new LoginAttemptService();
    }

    @Test
    void devePermitirLoginComPoucasTentativas() {
        String email = "admin@locadora.com";
        loginAttemptService.loginFailed(email);
        loginAttemptService.loginFailed(email);
        
        assertFalse(loginAttemptService.isBlocked(email));
    }

    @Test
    void deveBloquearContaApos5TentativasFalhas() {
        String email = "hacker@locadora.com";
        
        // 5 tentativas erradas
        for (int i = 0; i < 5; i++) {
            loginAttemptService.loginFailed(email);
        }
        
        assertTrue(loginAttemptService.isBlocked(email));
    }

    @Test
    void deveResetarTentativasAoLogarComSucesso() {
        String email = "user@locadora.com";
        
        // 3 tentativas erradas
        for (int i = 0; i < 3; i++) {
            loginAttemptService.loginFailed(email);
        }
        assertFalse(loginAttemptService.isBlocked(email));
        
        // Acertou a senha
        loginAttemptService.loginSucceeded(email);
        
        // Errou mais 3 vezes
        for (int i = 0; i < 3; i++) {
            loginAttemptService.loginFailed(email);
        }
        
        // Não deve estar bloqueado pois zerou no acerto
        assertFalse(loginAttemptService.isBlocked(email));
    }
}
