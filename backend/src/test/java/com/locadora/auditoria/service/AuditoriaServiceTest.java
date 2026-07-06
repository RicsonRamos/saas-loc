package com.locadora.auditoria.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.locadora.auditoria.dto.AuditoriaResponse;
import com.locadora.auditoria.entity.Auditoria;
import com.locadora.auditoria.repository.AuditoriaRepository;
import com.locadora.common.dto.PagedResponse;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class AuditoriaServiceTest {

    @Mock private AuditoriaRepository repository;
    @Spy private ObjectMapper objectMapper = new ObjectMapper();
    @InjectMocks private AuditoriaService service;

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

    @Test
    void deveRegistrarLogComSucesso() {
        service.registrar("CRIAR_CLIENTE", "Cliente", UUID.randomUUID(), null, null);
        verify(repository).save(any(Auditoria.class));
    }

    @Test
    void deveListarLogsPaginados() {
        Auditoria logItem = new Auditoria();
        logItem.setUsuario("admin@locadora.com");
        logItem.setAcao("LOGIN");
        logItem.setIp("127.0.0.1");

        Page<Auditoria> page = new PageImpl<>(List.of(logItem));
        when(repository.findByTenantIdOrderByCreatedAtDesc(eq(TENANT_ID), any(PageRequest.class))).thenReturn(page);

        PagedResponse<AuditoriaResponse> response = service.listar(PageRequest.of(0, 10));

        assertNotNull(response);
        assertEquals(1, response.getData().size());
        assertEquals("LOGIN", response.getData().getFirst().getAcao());
    }
}
