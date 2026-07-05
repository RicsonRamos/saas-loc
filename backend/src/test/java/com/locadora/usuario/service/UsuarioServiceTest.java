package com.locadora.usuario.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.entity.Usuario;
import com.locadora.usuario.mapper.UsuarioMapper;
import com.locadora.usuario.repository.UsuarioRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class UsuarioServiceTest {

    @Mock private UsuarioRepository usuarioRepository;
    @Mock private UsuarioMapper usuarioMapper;
    @Mock private PasswordEncoder passwordEncoder;
    @InjectMocks private UsuarioService usuarioService;

    @Test
    void deveCriarUsuarioComSucesso() {
        UsuarioRequest request = new UsuarioRequest();
        request.setEmail("admin@locadora.com");
        request.setNome("Admin");
        request.setSenha("123456");

        Usuario usuario = new Usuario();
        usuario.setEmail("admin@locadora.com");

        when(usuarioRepository.existsByEmail("admin@locadora.com")).thenReturn(false);
        when(usuarioMapper.toEntity(request)).thenReturn(usuario);
        when(passwordEncoder.encode("123456")).thenReturn("hashed");
        when(usuarioRepository.save(any())).thenReturn(usuario);
        when(usuarioMapper.toResponse(usuario)).thenReturn(new UsuarioResponse());

        UsuarioResponse response = usuarioService.criar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveCriarUsuarioComEmailDuplicado() {
        UsuarioRequest request = new UsuarioRequest();
        request.setEmail("admin@locadora.com");

        when(usuarioRepository.existsByEmail("admin@locadora.com")).thenReturn(true);

        assertThrows(BusinessException.class, () -> usuarioService.criar(request));
    }
}
