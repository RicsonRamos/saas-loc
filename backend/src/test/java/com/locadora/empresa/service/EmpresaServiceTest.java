package com.locadora.empresa.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.empresa.dto.EmpresaResponse;
import com.locadora.empresa.dto.RegistroEmpresaRequest;
import com.locadora.empresa.entity.Empresa;
import com.locadora.empresa.mapper.EmpresaMapper;
import com.locadora.empresa.repository.EmpresaRepository;
import com.locadora.usuario.repository.UsuarioRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

/**
 * Testes do EmpresaService.
 * Conforme SKILL 05 — Test-First Execution.
 */
@ExtendWith(MockitoExtension.class)
class EmpresaServiceTest {

    @Mock
    private EmpresaRepository empresaRepository;

    @Mock
    private UsuarioRepository usuarioRepository;

    @Mock
    private EmpresaMapper empresaMapper;

    @Mock
    private PasswordEncoder passwordEncoder;

    @InjectMocks
    private EmpresaService empresaService;

    private RegistroEmpresaRequest request;

    @BeforeEach
    void setUp() {
        request = new RegistroEmpresaRequest(
                "Locadora ABC",
                "ABC Locações LTDA",
                "12345678000100",
                "Admin User",
                "admin@locadora.com",
                "senha12345"
        );
    }

    @Test
    @DisplayName("deve registrar empresa com sucesso")
    void deveRegistrarEmpresaComSucesso() {
        UUID empresaId = UUID.randomUUID();
        Empresa empresa = Empresa.builder()
                .nomeFantasia("Locadora ABC")
                .razaoSocial("ABC Locações LTDA")
                .cnpj("12345678000100")
                .build();
        empresa.setId(empresaId);
        empresa.setTenantId(empresaId);

        EmpresaResponse expectedResponse = EmpresaResponse.builder()
                .id(empresaId)
                .nomeFantasia("Locadora ABC")
                .build();

        when(empresaRepository.existsByCnpj(anyString())).thenReturn(false);
        when(usuarioRepository.existsByEmail(anyString())).thenReturn(false);
        when(empresaRepository.save(any(Empresa.class))).thenReturn(empresa);
        when(passwordEncoder.encode(anyString())).thenReturn("encoded-password");
        when(empresaMapper.toResponse(any(Empresa.class))).thenReturn(expectedResponse);

        EmpresaResponse result = empresaService.registrar(request);

        assertNotNull(result);
        assertEquals("Locadora ABC", result.getNomeFantasia());
        verify(empresaRepository, times(2)).save(any(Empresa.class));
        verify(usuarioRepository).save(any());
    }

    @Test
    @DisplayName("deve rejeitar CNPJ duplicado")
    void deveRejeitarCnpjDuplicado() {
        when(empresaRepository.existsByCnpj("12345678000100")).thenReturn(true);

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> empresaService.registrar(request)
        );

        assertEquals("CNPJ já cadastrado", exception.getMessage());
        verify(empresaRepository, never()).save(any());
    }

    @Test
    @DisplayName("deve rejeitar email duplicado")
    void deveRejeitarEmailDuplicado() {
        when(empresaRepository.existsByCnpj(anyString())).thenReturn(false);
        when(usuarioRepository.existsByEmail("admin@locadora.com")).thenReturn(true);

        BusinessException exception = assertThrows(
                BusinessException.class,
                () -> empresaService.registrar(request)
        );

        assertEquals("E-mail já cadastrado", exception.getMessage());
        verify(empresaRepository, never()).save(any());
    }
}
