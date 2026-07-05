package com.locadora.auditoria.controller;

import com.locadora.auditoria.dto.AuditoriaResponse;
import com.locadora.auditoria.service.AuditoriaService;
import com.locadora.common.dto.PagedResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Auditoria", description = "Visualização de logs de auditoria detalhados de conformidade")
@RestController
@RequestMapping("/api/v1/auditoria")
public class AuditoriaController {

    private final AuditoriaService service;

    public AuditoriaController(AuditoriaService service) {
        this.service = service;
    }

    @Operation(summary = "Retorna o extrato de auditoria de conformidade (Apenas ADMIN)")
    @GetMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<PagedResponse<AuditoriaResponse>> listar(@PageableDefault(size = 30) Pageable pageable) {
        return ResponseEntity.ok(service.listar(pageable));
    }
}
