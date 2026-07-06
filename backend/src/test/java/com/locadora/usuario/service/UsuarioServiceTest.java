package com.locadora.usuario.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.entity.Role;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.mapper.UsuarioMapper;
import com.locadora.usuario.repository.UsuarioRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

/**
 * Testes unitários do serviço de usuários.
 * Valida criação com sucesso e rejeição de e-mail duplicado.
 */
@ExtendWith(MockitoExtension.class)
class UsuarioServiceTest {

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private UsuarioMapper usuarioMapper;
    @Mock private PasswordEncoder passwordEncoder;
    @InjectMocks private UsuarioService usuarioService;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    /**
     * Cenário feliz: criação de usuário com dados válidos retorna response não-nulo.
     */
    @Test
    void deveCriarUsuarioComSucesso() {
        // Usa AllArgsConstructor — DTO não possui setters
        UsuarioRequest request = new UsuarioRequest(
                "Admin", "admin@locadora.com", "Senha@1234", Set.of(Role.ADMIN)
        );

        Usuario usuario = new Usuario();
        usuario.setEmail("admin@locadora.com");

        when(usuarioRepository.existsByEmailAndDeletedAtIsNull("admin@locadora.com")).thenReturn(false);
        when(usuarioMapper.toEntity(request)).thenReturn(usuario);
        when(passwordEncoder.encode("Senha@1234")).thenReturn("hashed");
        when(usuarioRepository.save(any())).thenReturn(usuario);
        when(usuarioMapper.toResponse(usuario)).thenReturn(new UsuarioResponse());

        UsuarioResponse response = usuarioService.criar(request);
        assertNotNull(response);
    }

    /**
     * Regra de negócio: e-mail duplicado deve ser rejeitado com BusinessException.
     */
    @Test
    void naoDeveCriarUsuarioComEmailDuplicado() {
        UsuarioRequest request = new UsuarioRequest(
                "Admin", "admin@locadora.com", "Senha@1234", Set.of(Role.ADMIN)
        );

        when(usuarioRepository.existsByEmailAndDeletedAtIsNull("admin@locadora.com")).thenReturn(true);

        assertThrows(BusinessException.class, () -> usuarioService.criar(request));
    }
}
