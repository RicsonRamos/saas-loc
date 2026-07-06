package com.locadora.contrato.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.locadora.common.exception.BusinessException;
import com.locadora.contrato.dto.ChecklistRequest;
import com.locadora.contrato.dto.ChecklistResponse;
import com.locadora.contrato.entity.Checklist;
import com.locadora.contrato.entity.Contrato;
import com.locadora.contrato.entity.TipoChecklist;
import com.locadora.contrato.mapper.ChecklistMapper;
import com.locadora.contrato.repository.ChecklistRepository;
import com.locadora.contrato.repository.ContratoRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.Spy;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ChecklistServiceTest {

    @Mock private ChecklistRepository repository;
    @Mock private ChecklistMapper mapper;
    @Mock private ContratoRepository contratoRepository;
    @Spy private ObjectMapper objectMapper = new ObjectMapper();
    @InjectMocks private ChecklistService service;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private Contrato contrato;
    private Checklist checklistRetirada;
    private Checklist checklistDevolucao;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        contrato = new Contrato();
        contrato.setId(UUID.randomUUID());

        checklistRetirada = new Checklist();
        checklistRetirada.setContrato(contrato);
        checklistRetirada.setTipo(TipoChecklist.RETIRADA);
        checklistRetirada.setItensJson("[{\"item\":\"Estepe\",\"estado\":\"OK\"},{\"item\":\"Ar Condicionado\",\"estado\":\"OK\"}]");

        checklistDevolucao = new Checklist();
        checklistDevolucao.setContrato(contrato);
        checklistDevolucao.setTipo(TipoChecklist.DEVOLUCAO);
        checklistDevolucao.setItensJson("[{\"item\":\"Estepe\",\"estado\":\"FURADO\"},{\"item\":\"Ar Condicionado\",\"estado\":\"OK\"}]");
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    @Test
    void deveSalvarChecklistComSucesso() {
        ChecklistRequest request = ChecklistRequest.builder()
                .contratoId(contrato.getId())
                .tipo(TipoChecklist.RETIRADA)
                .itensJson("[]")
                .build();

        when(contratoRepository.findByIdAndTenantIdAndDeletedAtIsNull(contrato.getId(), TENANT_ID)).thenReturn(Optional.of(contrato));
        when(repository.findByContratoIdAndTipoAndTenantIdAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA, TENANT_ID)).thenReturn(Optional.empty());
        when(mapper.toEntity(request)).thenReturn(new Checklist());
        when(repository.save(any())).thenReturn(new Checklist());
        when(mapper.toResponse(any())).thenReturn(new ChecklistResponse());

        ChecklistResponse response = service.salvar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveSalvarChecklistDuplicado() {
        ChecklistRequest request = ChecklistRequest.builder()
                .contratoId(contrato.getId())
                .tipo(TipoChecklist.RETIRADA)
                .build();

        when(contratoRepository.findByIdAndTenantIdAndDeletedAtIsNull(contrato.getId(), TENANT_ID)).thenReturn(Optional.of(contrato));
        when(repository.findByContratoIdAndTipoAndTenantIdAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA, TENANT_ID)).thenReturn(Optional.of(new Checklist()));

        assertThrows(BusinessException.class, () -> service.salvar(request));
    }

    @Test
    void deveDetectarDivergenciasNaComparacao() {
        when(repository.findByContratoIdAndTipoAndTenantIdAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA, TENANT_ID)).thenReturn(Optional.of(checklistRetirada));
        when(repository.findByContratoIdAndTipoAndTenantIdAndDeletedAtIsNull(contrato.getId(), TipoChecklist.DEVOLUCAO, TENANT_ID)).thenReturn(Optional.of(checklistDevolucao));

        Map<String, String> divergencias = service.compararRetiradaEDevolucao(contrato.getId());

        assertNotNull(divergencias);
        assertEquals(1, divergencias.size());
        assertEquals("Divergência: Retirada = OK | Devolução = FURADO", divergencias.get("Estepe"));
    }
}
