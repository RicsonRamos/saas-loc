package com.locadora.frota.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.frota.dto.VeiculoRequest;
import com.locadora.frota.dto.VeiculoResponse;
import com.locadora.frota.service.VeiculoService;
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
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

/**
 * Controller de Veículos (Frota).
 */
@RestController
@RequestMapping("/api/v1/veiculos")
@Tag(name = "Frota", description = "Gestão de veículos da locadora (tenant)")
public class VeiculoController {

    private final VeiculoService veiculoService;

    public VeiculoController(VeiculoService veiculoService) {
        this.veiculoService = veiculoService;
    }

    @PostMapping
    @PreAuthorize("hasAuthority('VEICULO_CADASTRAR')")
    @Operation(summary = "Criar veículo", description = "Cadastra um novo veículo na frota")
    public ResponseEntity<ApiResponse<VeiculoResponse>> criar(@Valid @RequestBody VeiculoRequest request) {
        VeiculoResponse response = veiculoService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Veículo criado com sucesso"));
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Listar veículos", description = "Lista todos os veículos da locadora com paginação")
    public ResponseEntity<PagedResponse<VeiculoResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        PagedResponse<VeiculoResponse> response = veiculoService.listar(pageable);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Buscar veículo", description = "Busca os detalhes de um veículo pelo ID")
    public ResponseEntity<ApiResponse<VeiculoResponse>> buscarPorId(@PathVariable UUID id) {
        VeiculoResponse response = veiculoService.buscarPorId(id);
        return ResponseEntity.ok(ApiResponse.of(response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAuthority('VEICULO_CADASTRAR')")
    @Operation(summary = "Atualizar veículo", description = "Atualiza os dados de um veículo existente")
    public ResponseEntity<ApiResponse<VeiculoResponse>> atualizar(@PathVariable UUID id, 
                                                                  @Valid @RequestBody VeiculoRequest request) {
        VeiculoResponse response = veiculoService.atualizar(id, request);
        return ResponseEntity.ok(ApiResponse.of(response, "Veículo atualizado com sucesso"));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAuthority('VEICULO_EXCLUIR')")
    @Operation(summary = "Excluir veículo", description = "Realiza soft-delete de um veículo (se não estiver locado)")
    public ResponseEntity<ApiResponse<Void>> excluir(@PathVariable UUID id) {
        String name = SecurityContextHolder.getContext().getAuthentication().getName();
        UUID currentUserId = null;
        try {
            currentUserId = UUID.fromString(name);
        } catch (Exception e) {}
        
        veiculoService.excluir(id, currentUserId);
        return ResponseEntity.ok(ApiResponse.message("Veículo excluído com sucesso"));
    }
}
