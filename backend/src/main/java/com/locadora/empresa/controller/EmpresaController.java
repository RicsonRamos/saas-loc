package com.locadora.empresa.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.empresa.dto.EmpresaResponse;
import com.locadora.empresa.dto.RegistroEmpresaRequest;
import com.locadora.empresa.service.EmpresaService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller de Empresa.
 * Conforme 08-guard-rails.md: apenas recebe, valida, chama service, retorna.
 */
@RestController
@RequestMapping("/api/v1/empresas")
@Tag(name = "Empresas", description = "Gestão de empresas (tenants)")
public class EmpresaController {

    private final EmpresaService empresaService;

    public EmpresaController(EmpresaService empresaService) {
        this.empresaService = empresaService;
    }

    @PostMapping("/registro")
    @Operation(summary = "Registrar nova empresa",
               description = "Cria uma nova empresa (tenant) com o primeiro usuário administrador")
    public ResponseEntity<ApiResponse<EmpresaResponse>> registrar(@Valid @RequestBody RegistroEmpresaRequest request) {
        EmpresaResponse response = empresaService.registrar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Empresa registrada com sucesso"));
    }
}
