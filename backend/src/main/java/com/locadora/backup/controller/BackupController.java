package com.locadora.backup.controller;

import com.locadora.backup.service.BackupService;
import com.locadora.common.dto.ApiResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Backups", description = "Endpoints para gerenciamento de backups locais do banco SQLite")
@RestController
@RequestMapping("/api/v1/backups")
public class BackupController {

    private final BackupService service;

    public BackupController(BackupService service) {
        this.service = service;
    }

    @Operation(summary = "Gera um backup instantâneo do banco de dados SQLite (Apenas ADMIN/GERENTE)")
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    public ResponseEntity<ApiResponse<String>> gerarBackup() {
        String filename = service.criarBackup();
        return ResponseEntity.ok(ApiResponse.of(filename, "Backup local gerado com sucesso: " + filename));
    }
}
