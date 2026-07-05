package com.locadora.contrato.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.contrato.dto.ChecklistRequest;
import com.locadora.contrato.dto.ChecklistResponse;
import com.locadora.contrato.service.ChecklistService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Tag(name = "Checklists", description = "Vistoria e check de saída/devolução de veículos")
@RestController
@RequestMapping("/api/v1/contratos")
public class ChecklistController {

    private final ChecklistService service;

    public ChecklistController(ChecklistService service) {
        this.service = service;
    }

    @Operation(summary = "Salva um checklist de vistorias (saída ou devolução)")
    @PostMapping("/checklists")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ChecklistResponse>> salvar(@Valid @RequestBody ChecklistRequest request) {
        ChecklistResponse response = service.salvar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Checklist registrado com sucesso"));
    }

    @Operation(summary = "Obtém todos os checklists registrados para um contrato")
    @GetMapping("/{contratoId}/checklists")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<List<ChecklistResponse>> buscarPorContrato(@PathVariable UUID contratoId) {
        return ResponseEntity.ok(service.buscarPorContrato(contratoId));
    }

    @Operation(summary = "Compara automaticamente vistorias de Retirada e Devolução de um contrato")
    @GetMapping("/{contratoId}/checklists/comparar")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<Map<String, String>>> comparar(@PathVariable UUID contratoId) {
        Map<String, String> divergencias = service.compararRetiradaEDevolucao(contratoId);
        return ResponseEntity.ok(ApiResponse.of(divergencias));
    }
}
