package com.locadora.cliente.controller;

import com.locadora.cliente.dto.ClienteRequest;
import com.locadora.cliente.dto.ClienteResponse;
import com.locadora.cliente.service.ClienteService;
import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.security.jwt.JwtTokenProvider;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
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
 * Controller de Clientes.
 */
@RestController
@RequestMapping("/api/v1/clientes")
@Tag(name = "Clientes", description = "Gestão de locatários (PF/PJ) da locadora")
public class ClienteController {

    private final ClienteService clienteService;
    private final JwtTokenProvider jwtTokenProvider;

    public ClienteController(ClienteService clienteService, JwtTokenProvider jwtTokenProvider) {
        this.clienteService = clienteService;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Criar cliente", description = "Cadastra um novo cliente PF/PJ")
    public ResponseEntity<ApiResponse<ClienteResponse>> criar(@Valid @RequestBody ClienteRequest request) {
        ClienteResponse response = clienteService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Cliente criado com sucesso"));
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Listar clientes", description = "Lista todos os clientes com paginação")
    public ResponseEntity<PagedResponse<ClienteResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        PagedResponse<ClienteResponse> response = clienteService.listar(pageable);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR', 'FINANCEIRO')")
    @Operation(summary = "Buscar cliente", description = "Busca os detalhes de um cliente pelo ID")
    public ResponseEntity<ApiResponse<ClienteResponse>> buscarPorId(@PathVariable UUID id) {
        ClienteResponse response = clienteService.buscarPorId(id);
        return ResponseEntity.ok(ApiResponse.of(response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Atualizar cliente", description = "Atualiza os dados de um cliente existente")
    public ResponseEntity<ApiResponse<ClienteResponse>> atualizar(@PathVariable UUID id, 
                                                                  @Valid @RequestBody ClienteRequest request) {
        ClienteResponse response = clienteService.atualizar(id, request);
        return ResponseEntity.ok(ApiResponse.of(response, "Cliente atualizado com sucesso"));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Excluir cliente", description = "Realiza soft-delete de um cliente")
    public ResponseEntity<ApiResponse<Void>> excluir(@PathVariable UUID id, HttpServletRequest request) {
        String token = request.getHeader("Authorization").substring(7);
        UUID currentUserId = jwtTokenProvider.getUserIdFromToken(token);
        
        clienteService.excluir(id, currentUserId);
        return ResponseEntity.ok(ApiResponse.message("Cliente excluído com sucesso"));
    }
}
