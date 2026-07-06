package com.locadora.frota.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.frota.dto.DocumentoVeiculoRequest;
import com.locadora.frota.dto.DocumentoVeiculoResponse;
import com.locadora.frota.service.DocumentoVeiculoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
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
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.UUID;

@Tag(name = "Documentos dos Veículos", description = "Gestão e controle de compliance e prazos de seguros, IPVA, CRLV")
@RestController
@RequestMapping("/api/v1/veiculos")
public class DocumentoVeiculoController {

    private final DocumentoVeiculoService service;

    public DocumentoVeiculoController(DocumentoVeiculoService service) {
        this.service = service;
    }

    @Operation(summary = "Cadastra um novo documento para um veículo")
    @PostMapping("/documentos")
    @PreAuthorize("hasAuthority('DOCUMENTO_GERENCIAR')")
    public ResponseEntity<ApiResponse<DocumentoVeiculoResponse>> criar(@Valid @RequestBody DocumentoVeiculoRequest request) {
        DocumentoVeiculoResponse response = service.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Documento cadastrado com sucesso"));
    }

    @Operation(summary = "Atualiza as informações de um documento")
    @PutMapping("/documentos/{id}")
    @PreAuthorize("hasAuthority('DOCUMENTO_GERENCIAR')")
    public ResponseEntity<ApiResponse<DocumentoVeiculoResponse>> atualizar(@PathVariable UUID id, @Valid @RequestBody DocumentoVeiculoRequest request) {
        return ResponseEntity.ok(ApiResponse.of(service.atualizar(id, request), "Documento atualizado com sucesso"));
    }

    @Operation(summary = "Lista todos os documentos vinculados a um veículo")
    @GetMapping("/{veiculoId}/documentos")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<List<DocumentoVeiculoResponse>> listarPorVeiculo(@PathVariable UUID veiculoId) {
        return ResponseEntity.ok(service.listarPorVeiculo(veiculoId));
    }

    @Operation(summary = "Obtém os detalhes de um documento pelo ID")
    @GetMapping("/documentos/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<ApiResponse<DocumentoVeiculoResponse>> buscarPorId(@PathVariable UUID id) {
        return ResponseEntity.ok(ApiResponse.of(service.buscarPorId(id)));
    }

    @Operation(summary = "Realiza a exclusão lógica de um documento")
    @DeleteMapping("/documentos/{id}")
    @PreAuthorize("hasAuthority('DOCUMENTO_GERENCIAR')")
    public ResponseEntity<ApiResponse<Void>> excluir(@PathVariable UUID id) {
        String name = SecurityContextHolder.getContext().getAuthentication().getName();
        UUID currentUserId = null;
        try {
            currentUserId = UUID.fromString(name);
        } catch (Exception e) {}
        service.excluir(id, currentUserId);
        return ResponseEntity.ok(ApiResponse.message("Documento excluído com sucesso"));
    }
}
