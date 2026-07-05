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
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
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
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ChecklistServiceTest {

    @Mock private ChecklistRepository repository;
    @Mock private ChecklistMapper mapper;
    @Mock private ContratoRepository contratoRepository;
    @Spy private ObjectMapper objectMapper = new ObjectMapper();
    @InjectMocks private ChecklistService service;

    private Contrato contrato;
    private Checklist checklistRetirada;
    private Checklist checklistDevolucao;

    @BeforeEach
    void setUp() {
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

    @Test
    void deveSalvarChecklistComSucesso() {
        ChecklistRequest request = new ChecklistRequest();
        request.setContratoId(contrato.getId());
        request.setTipo(TipoChecklist.RETIRADA);
        request.setItensJson("[]");

        when(contratoRepository.findByIdAndDeletedAtIsNull(contrato.getId())).thenReturn(Optional.of(contrato));
        when(repository.findByContratoIdAndTipoAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA)).thenReturn(Optional.empty());
        when(mapper.toEntity(request)).thenReturn(new Checklist());
        when(repository.save(any())).thenReturn(new Checklist());
        when(mapper.toResponse(any())).thenReturn(new ChecklistResponse());

        ChecklistResponse response = service.salvar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveSalvarChecklistDuplicado() {
        ChecklistRequest request = new ChecklistRequest();
        request.setContratoId(contrato.getId());
        request.setTipo(TipoChecklist.RETIRADA);

        when(contratoRepository.findByIdAndDeletedAtIsNull(contrato.getId())).thenReturn(Optional.of(contrato));
        when(repository.findByContratoIdAndTipoAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA)).thenReturn(Optional.of(new Checklist()));

        assertThrows(BusinessException.class, () -> service.salvar(request));
    }

    @Test
    void deveDetectarDivergenciasNaComparacao() {
        when(repository.findByContratoIdAndTipoAndDeletedAtIsNull(contrato.getId(), TipoChecklist.RETIRADA)).thenReturn(Optional.of(checklistRetirada));
        when(repository.findByContratoIdAndTipoAndDeletedAtIsNull(contrato.getId(), TipoChecklist.DEVOLUCAO)).thenReturn(Optional.of(checklistDevolucao));

        Map<String, String> divergencias = service.compararRetiradaEDevolucao(contrato.getId());

        assertNotNull(divergencias);
        assertEquals(1, divergencias.size());
        assertEquals("Divergência: Retirada = OK | Devolução = FURADO", divergencias.get("Estepe"));
    }
}
