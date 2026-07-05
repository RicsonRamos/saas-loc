package com.locadora.contrato.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.contrato.dto.ContratoRequest;
import com.locadora.contrato.dto.ContratoResponse;
import com.locadora.contrato.dto.EncerramentoContratoRequest;
import com.locadora.contrato.service.ContratoService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.UUID;

/**
 * Controller REST de Contratos.
 * Expõe as rotas de faturamento e aluguel de carros.
 */
@RestController
@RequestMapping("/api/v1/contratos")
@Tag(name = "Contratos", description = "Gestão de locações, devoluções e orquestração de frota")
public class ContratoController {

    private final ContratoService contratoService;

    public ContratoController(ContratoService contratoService) {
        this.contratoService = contratoService;
    }

    /**
     * Cria um contrato e automaticamente altera o status do veículo para LOCADO.
     */
    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Criar contrato", description = "Inicia uma nova locação (Retirada de veículo)")
    public ResponseEntity<ApiResponse<ContratoResponse>> criar(@Valid @RequestBody ContratoRequest request) {
        ContratoResponse response = contratoService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Contrato gerado com sucesso. O veículo foi reservado."));
    }

    /**
     * Lista todos os contratos vigentes e históricos da empresa.
     */
    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Listar contratos", description = "Lista todos os contratos da locadora (com paginação)")
    public ResponseEntity<PagedResponse<ContratoResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        PagedResponse<ContratoResponse> response = contratoService.listar(pageable);
        return ResponseEntity.ok(response);
    }

    /**
     * Busca dados detalhados de uma locação por ID.
     */
    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Buscar contrato", description = "Busca detalhes estritos de um contrato pelo UUID")
    public ResponseEntity<ApiResponse<ContratoResponse>> buscarPorId(@PathVariable UUID id) {
        ContratoResponse response = contratoService.buscarPorId(id);
        return ResponseEntity.ok(ApiResponse.of(response));
    }

    /**
     * Encerra uma locação (Devolução), liberando o veículo e calculando o KM real.
     */
    @PutMapping("/{id}/encerrar")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Encerrar contrato", description = "Faz o checkout da locação, atualizando o hodômetro do veículo e mudando o status para DISPONÍVEL.")
    public ResponseEntity<ApiResponse<ContratoResponse>> encerrar(@PathVariable UUID id, 
                                                                  @Valid @RequestBody EncerramentoContratoRequest request) {
        ContratoResponse response = contratoService.encerrar(id, request);
        return ResponseEntity.ok(ApiResponse.of(response, "Contrato encerrado e veículo liberado para o pátio."));
    }
}
