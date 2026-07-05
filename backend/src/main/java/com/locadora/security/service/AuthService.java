package com.locadora.security.service;

import com.locadora.auth.service.LoginAttemptService;
import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.UnauthorizedException;
import com.locadora.security.dto.LoginRequest;
import com.locadora.security.dto.RefreshTokenRequest;
import com.locadora.security.dto.TokenResponse;
import com.locadora.security.jwt.JwtTokenProvider;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.repository.UsuarioRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.AuthenticationException;
import org.springframework.stereotype.Service;

import java.util.UUID;

/**
 * Serviço de autenticação — Single-Tenant.
 * JWT Stateless, BCrypt, Access + Refresh Token.
 * Não gerencia mais tenantId.
 */
@Service
public class AuthService {

    private static final Logger log = LoggerFactory.getLogger(AuthService.class);

    private final AuthenticationManager authenticationManager;
    private final JwtTokenProvider jwtTokenProvider;
    private final UsuarioRepository usuarioRepository;
    private final LoginAttemptService loginAttemptService;
    private final long accessExpirationMs;

    public AuthService(AuthenticationManager authenticationManager,
                       JwtTokenProvider jwtTokenProvider,
                       UsuarioRepository usuarioRepository,
                       LoginAttemptService loginAttemptService,
                       @Value("${app.jwt.access-expiration-ms}") long accessExpirationMs) {
        this.authenticationManager = authenticationManager;
        this.jwtTokenProvider = jwtTokenProvider;
        this.usuarioRepository = usuarioRepository;
        this.loginAttemptService = loginAttemptService;
        this.accessExpirationMs = accessExpirationMs;
    }

    public TokenResponse login(LoginRequest request) {
        if (loginAttemptService.isBlocked(request.getEmail())) {
            throw new BusinessException("Conta bloqueada por excesso de tentativas falhas. Tente novamente em 15 minutos.");
        }

        try {
            authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(request.getEmail(), request.getSenha())
            );

            Usuario usuario = usuarioRepository.findByEmailAndDeletedAtIsNull(request.getEmail())
                    .orElseThrow(() -> new UnauthorizedException("Usuário não encontrado"));

            if (!usuario.getAtivo()) {
                throw new BusinessException("Usuário inativo");
            }

            String accessToken = jwtTokenProvider.generateAccessToken(usuario.getId(), usuario.getEmail());
            String refreshToken = jwtTokenProvider.generateRefreshToken(usuario.getId(), usuario.getEmail());

            log.info("Login realizado com sucesso para usuário: {}", usuario.getEmail());
            loginAttemptService.loginSucceeded(request.getEmail());

            return TokenResponse.builder()
                    .accessToken(accessToken)
                    .refreshToken(refreshToken)
                    .tokenType("Bearer")
                    .expiresIn(accessExpirationMs / 1000)
                    .build();

        } catch (AuthenticationException e) {
            log.warn("Tentativa de login inválida para: {}", request.getEmail());
            loginAttemptService.loginFailed(request.getEmail());
            throw new UnauthorizedException("Credenciais inválidas");
        }
    }

    public TokenResponse refreshToken(RefreshTokenRequest request) {
        String refreshToken = request.getRefreshToken();

        if (!jwtTokenProvider.validateToken(refreshToken)) {
            throw new UnauthorizedException("Refresh token inválido");
        }

        String tokenType = jwtTokenProvider.getTokenType(refreshToken);
        if (!"REFRESH".equals(tokenType)) {
            throw new UnauthorizedException("Token não é do tipo refresh");
        }

        String email = jwtTokenProvider.getEmailFromToken(refreshToken);
        Usuario usuario = usuarioRepository.findByEmailAndDeletedAtIsNull(email)
                .orElseThrow(() -> new UnauthorizedException("Usuário não encontrado"));

        String newAccessToken = jwtTokenProvider.generateAccessToken(usuario.getId(), usuario.getEmail());
        String newRefreshToken = jwtTokenProvider.generateRefreshToken(usuario.getId(), usuario.getEmail());

        return TokenResponse.builder()
                .accessToken(newAccessToken)
                .refreshToken(newRefreshToken)
                .tokenType("Bearer")
                .expiresIn(accessExpirationMs / 1000)
                .build();
    }
}
