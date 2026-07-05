package com.locadora.alerta.controller;

import com.locadora.alerta.dto.AlertaResponse;
import com.locadora.alerta.service.AlertaService;
import com.locadora.common.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@Tag(name = "Alertas", description = "Central de notificações operacionais e alertas de compliance")
@RestController
@RequestMapping("/api/v1/alertas")
public class AlertaController {

    private final AlertaService service;

    public AlertaController(AlertaService service) {
        this.service = service;
    }

    @Operation(summary = "Obtém os alertas pendentes (não lidos)")
    @GetMapping("/pendentes")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<List<AlertaResponse>> obterPendentes() {
        return ResponseEntity.ok(service.obterPendentes());
    }

    @Operation(summary = "Obtém o histórico de todos os alertas")
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<List<AlertaResponse>> obterTodos() {
        return ResponseEntity.ok(service.obterTodos());
    }

    @Operation(summary = "Marca um alerta específico como lido")
    @PutMapping("/{id}/ler")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<ApiResponse<Void>> marcarComoLido(@PathVariable UUID id) {
        service.marcarComoLido(id);
        return ResponseEntity.ok(ApiResponse.message("Alerta marcado como lido"));
    }

    @Operation(summary = "Marca todos os alertas pendentes como lidos")
    @PutMapping("/ler-todos")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<ApiResponse<Void>> marcarTodosComoLidos() {
        service.marcarTodosComoLidos();
        return ResponseEntity.ok(ApiResponse.message("Todos os alertas foram marcados como lidos"));
    }

    @Operation(summary = "Dispara manualmente a varredura de compliance e vencimentos")
    @PostMapping("/verificar")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    public ResponseEntity<ApiResponse<Void>> verificarManualmente() {
        service.verificarEPontuarAlertas();
        return ResponseEntity.ok(ApiResponse.message("Varredura de alertas iniciada com sucesso"));
    }
}
