package com.locadora.usuario.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.security.jwt.JwtTokenProvider;
import com.locadora.usuario.dto.UsuarioRequest;
import com.locadora.usuario.dto.UsuarioResponse;
import com.locadora.usuario.dto.UsuarioUpdateRequest;
import com.locadora.usuario.service.UsuarioService;
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
 * Controller de Usuários.
 * Conforme 08-guard-rails.md: apenas delega chamadas, aplica RBAC.
 */
@RestController
@RequestMapping("/api/v1/usuarios")
@Tag(name = "Usuários", description = "Gestão de usuários da empresa (tenant)")
public class UsuarioController {

    private final UsuarioService usuarioService;
    private final JwtTokenProvider jwtTokenProvider;

    public UsuarioController(UsuarioService usuarioService, JwtTokenProvider jwtTokenProvider) {
        this.usuarioService = usuarioService;
        this.jwtTokenProvider = jwtTokenProvider;
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Criar usuário", description = "Cria um novo usuário na empresa (Apenas ADMIN)")
    public ResponseEntity<ApiResponse<UsuarioResponse>> criar(@Valid @RequestBody UsuarioRequest request) {
        UsuarioResponse response = usuarioService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Usuário criado com sucesso"));
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Listar usuários", description = "Lista usuários da empresa com paginação (ADMIN, GERENTE)")
    public ResponseEntity<PagedResponse<UsuarioResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        PagedResponse<UsuarioResponse> response = usuarioService.listar(pageable);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Buscar usuário", description = "Busca um usuário pelo ID (ADMIN, GERENTE)")
    public ResponseEntity<ApiResponse<UsuarioResponse>> buscarPorId(@PathVariable UUID id) {
        UsuarioResponse response = usuarioService.buscarPorId(id);
        return ResponseEntity.ok(ApiResponse.of(response));
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Atualizar usuário", description = "Atualiza dados de um usuário (Apenas ADMIN)")
    public ResponseEntity<ApiResponse<UsuarioResponse>> atualizar(@PathVariable UUID id, 
                                                                  @Valid @RequestBody UsuarioUpdateRequest request) {
        UsuarioResponse response = usuarioService.atualizar(id, request);
        return ResponseEntity.ok(ApiResponse.of(response, "Usuário atualizado com sucesso"));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Excluir usuário", description = "Realiza soft-delete de um usuário (Apenas ADMIN)")
    public ResponseEntity<ApiResponse<Void>> excluir(@PathVariable UUID id, HttpServletRequest request) {
        // Extrair o ID do usuário atual do header Authorization (já validado pelo filtro)
        String token = request.getHeader("Authorization").substring(7);
        UUID currentUserId = jwtTokenProvider.getUserIdFromToken(token);
        
        usuarioService.excluir(id, currentUserId);
        return ResponseEntity.ok(ApiResponse.message("Usuário excluído com sucesso"));
    }
}
