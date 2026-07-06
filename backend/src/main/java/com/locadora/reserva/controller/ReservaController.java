package com.locadora.reserva.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.reserva.dto.ReservaRequest;
import com.locadora.reserva.dto.ReservaResponse;
import com.locadora.reserva.service.ReservaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.util.UUID;

@Tag(name = "Reservas", description = "Gestão de reservas de veículos e agendamento prévio")
@RestController
@RequestMapping("/api/v1/reservas")
public class ReservaController {

    private final ReservaService service;

    public ReservaController(ReservaService service) {
        this.service = service;
    }

    @Operation(summary = "Criar uma nova reserva")
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ReservaResponse>> criar(@Valid @RequestBody ReservaRequest request) {
        ReservaResponse response = service.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Reserva criada com sucesso"));
    }

    @Operation(summary = "Listar reservas paginadas")
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<PagedResponse<ReservaResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        return ResponseEntity.ok(service.listar(pageable));
    }

    @Operation(summary = "Obter detalhes de uma reserva pelo ID")
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ReservaResponse>> buscarPorId(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.of(service.buscarPorId(id)));
    }

    @Operation(summary = "Atualizar dados de uma reserva")
    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ReservaResponse>> atualizar(@PathVariable UUID id, @Valid @RequestBody ReservaRequest request) {
        return ResponseEntity.ok(ApiResponse.of(service.atualizar(id, request), "Reserva atualizada com sucesso"));
    }

    @Operation(summary = "Cancelar uma reserva ativa")
    @PutMapping("/{id}/cancelar")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ReservaResponse>> cancelar(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.of(service.cancelar(id), "Reserva cancelada com sucesso"));
    }

    @Operation(summary = "Confirmar uma reserva pendente")
    @PutMapping("/{id}/confirmar")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<ReservaResponse>> confirmar(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.of(service.confirmar(id), "Reserva confirmada com sucesso"));
    }

    @Operation(summary = "Converter uma reserva confirmada em Contrato de Locação")
    @PostMapping("/{id}/converter")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    public ResponseEntity<ApiResponse<UUID>> converter(@PathVariable UUID id, @RequestParam BigDecimal valorDiaria) {
        UUID contratoId = service.converterEmContrato(id, valorDiaria);
        return ResponseEntity.ok(ApiResponse.of(contratoId, "Reserva convertida em contrato com sucesso"));
    }

    @Operation(summary = "Realizar a exclusão lógica de uma reserva")
    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<ApiResponse<Void>> excluir(@PathVariable UUID id) {
        String name = SecurityContextHolder.getContext().getAuthentication().getName();
        UUID currentUserId = null;
        try {
            currentUserId = UUID.fromString(name);
        } catch (Exception e) {}
        service.excluir(id, currentUserId);
        return ResponseEntity.ok(ApiResponse.message("Reserva excluída com sucesso"));
    }
}
