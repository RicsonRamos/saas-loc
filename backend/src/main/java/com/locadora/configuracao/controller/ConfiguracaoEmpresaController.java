package com.locadora.configuracao.controller;

import com.locadora.configuracao.dto.ConfiguracaoEmpresaDTO;
import com.locadora.configuracao.service.ConfiguracaoEmpresaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Tag(name = "Configuração da Empresa", description = "Gestão de dados cadastrais e políticas da locadora")
@RestController
@RequestMapping("/api/v1/configuracao")
public class ConfiguracaoEmpresaController {

    private final ConfiguracaoEmpresaService service;

    public ConfiguracaoEmpresaController(ConfiguracaoEmpresaService service) {
        this.service = service;
    }

    @Operation(summary = "Obtém as configurações globais da empresa")
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    public ResponseEntity<ConfiguracaoEmpresaDTO> obter() {
        return ResponseEntity.ok(service.obter());
    }

    @Operation(summary = "Atualiza as configurações globais da empresa")
    @PutMapping
    @PreAuthorize("hasAuthority('CONFIGURACAO_GERENCIAR')")
    public ResponseEntity<ConfiguracaoEmpresaDTO> atualizar(@Valid @RequestBody ConfiguracaoEmpresaDTO dto) {
        return ResponseEntity.ok(service.atualizar(dto));
    }
}
