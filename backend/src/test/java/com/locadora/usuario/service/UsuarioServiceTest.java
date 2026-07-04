package com.locadora.usuario.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.shared.tenant.TenantContext;
import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.entity.Role;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.mapper.UsuarioMapper;
import com.locadora.usuario.repository.UsuarioRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.Optional;
import java.util.Set;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Testes do UsuarioService.
 * Conforme SKILL 05 — Test-First Execution.
 * Garante que o isolamento do tenant está sendo respeitado.
 */
@ExtendWith(MockitoExtension.class)
class UsuarioServiceTest {

    @Mock
    private UsuarioRepository usuarioRepository;

    @Mock
    private UsuarioMapper usuarioMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private UsuarioService usuarioService;

    private UUID tenantId;
    private UsuarioRequest request;

    @BeforeEach
    void setUp() {
        tenantId = UUID.randomUUID();
        TenantContext.setTenantId(tenantId);

        request = new UsuarioRequest(
                "João Operador",
                "joao@locadora.com",
                "senhaForte123",
                Set.of(Role.OPERADOR)
        );
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    @DisplayName("deve criar usuário garantindo o tenantId do contexto")
    void deveCriarUsuarioGarantindoTenant() {
        Usuario usuario = new Usuario();
        
        UsuarioResponse expectedResponse = UsuarioResponse.builder()
                .nome("João Operador")
                .email("joao@locadora.com")
                .build();

        when(usuarioRepository.existsByEmail(anyString())).thenReturn(false);
        when(usuarioMapper.toEntity(any(UsuarioRequest.class))).thenReturn(usuario);
        when(passwordEncoder.encode(anyString())).thenReturn("hashed-pwd");
        when(usuarioRepository.save(any(Usuario.class))).thenAnswer(i -> {
            Usuario saved = i.getArgument(0);
            assertEquals(tenantId, saved.getTenantId(), "Tenant ID não foi configurado corretamente");
            assertEquals("hashed-pwd", saved.getSenha());
            return saved;
        });
        when(usuarioMapper.toResponse(any(Usuario.class))).thenReturn(expectedResponse);

        UsuarioResponse result = usuarioService.criar(request);

        assertNotNull(result);
        assertEquals("João Operador", result.getNome());
        verify(usuarioRepository).save(any(Usuario.class));
    }

    @Test
    @DisplayName("deve rejeitar e-mail duplicado na criação")
    void deveRejeitarEmailDuplicado() {
        when(usuarioRepository.existsByEmail(anyString())).thenReturn(true);

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> usuarioService.criar(request)
        );

        assertEquals("E-mail já cadastrado", exception.getMessage());
        verify(usuarioRepository, never()).save(any());
    }

    @Test
    @DisplayName("deve buscar usuário apenas se pertencer ao tenant atual")
    void deveBuscarApenasNoTenantAtual() {
        UUID usuarioId = UUID.randomUUID();
        Usuario usuario = new Usuario();
        usuario.setId(usuarioId);
        usuario.setTenantId(tenantId);
        
        UsuarioResponse expectedResponse = UsuarioResponse.builder().id(usuarioId).build();

        when(usuarioRepository.findByIdAndTenantIdAndDeletedAtIsNull(usuarioId, tenantId))
                .thenReturn(Optional.of(usuario));
        when(usuarioMapper.toResponse(usuario)).thenReturn(expectedResponse);

        UsuarioResponse result = usuarioService.buscarPorId(usuarioId);

        assertNotNull(result);
        assertEquals(usuarioId, result.getId());
    }

    @Test
    @DisplayName("deve lançar erro se usuário for de outro tenant ou não existir")
    void deveLancarErroParaOutroTenant() {
        UUID usuarioId = UUID.randomUUID();
        
        // Simula que o repositório não encontrou porque filtrou pelo tenant_id
        when(usuarioRepository.findByIdAndTenantIdAndDeletedAtIsNull(usuarioId, tenantId))
                .thenReturn(Optional.empty());

        assertThrows(
                ResourceNotFoundException.class,
                () -> usuarioService.buscarPorId(usuarioId)
        );
    }

    @Test
    @DisplayName("deve realizar soft delete e impedir exclusão do próprio usuário")
    void deveRealizarSoftDelete() {
        UUID usuarioIdParaExcluir = UUID.randomUUID();
        UUID currentUserId = UUID.randomUUID(); // Diferente
        
        Usuario usuario = new Usuario();
        usuario.setId(usuarioIdParaExcluir);
        usuario.setTenantId(tenantId);

        when(usuarioRepository.findByIdAndTenantIdAndDeletedAtIsNull(usuarioIdParaExcluir, tenantId))
                .thenReturn(Optional.of(usuario));

        usuarioService.excluir(usuarioIdParaExcluir, currentUserId);

        assertTrue(usuario.isDeleted());
        assertEquals(currentUserId, usuario.getDeletedBy());
        verify(usuarioRepository).save(usuario);
    }

    @Test
    @DisplayName("deve impedir exclusão do próprio usuário")
    void deveImpedirExclusaoDoProprioUsuario() {
        UUID currentUserId = UUID.randomUUID();
        
        Usuario usuario = new Usuario();
        usuario.setId(currentUserId);
        usuario.setTenantId(tenantId);

        when(usuarioRepository.findByIdAndTenantIdAndDeletedAtIsNull(currentUserId, tenantId))
                .thenReturn(Optional.of(usuario));

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> usuarioService.excluir(currentUserId, currentUserId)
        );

        assertEquals("Não é possível excluir o próprio usuário", exception.getMessage());
        verify(usuarioRepository, never()).save(any());
    }
}
