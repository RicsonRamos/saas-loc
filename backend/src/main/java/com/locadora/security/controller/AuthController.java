package com.locadora.security.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.security.dto.LoginRequest;
import com.locadora.security.dto.RefreshTokenRequest;
import com.locadora.security.dto.TokenResponse;
import com.locadora.security.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller de autenticação.
 * Conforme 08-guard-rails.md: controllers apenas recebem, validam, chamam service, retornam.
 */
@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Autenticação", description = "Endpoints de autenticação")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/login")
    @Operation(summary = "Realizar login", description = "Autentica usuário e retorna tokens JWT")
    public ResponseEntity<ApiResponse<TokenResponse>> login(@Valid @RequestBody LoginRequest request) {
        TokenResponse token = authService.login(request);
        return ResponseEntity.ok(ApiResponse.of(token));
    }

    @PostMapping("/refresh")
    @Operation(summary = "Renovar token", description = "Gera novo access token usando refresh token")
    public ResponseEntity<ApiResponse<TokenResponse>> refresh(@Valid @RequestBody RefreshTokenRequest request) {
        TokenResponse token = authService.refreshToken(request);
        return ResponseEntity.ok(ApiResponse.of(token));
    }
}
