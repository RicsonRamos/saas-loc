package com.locadora.manutencao.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.manutencao.dto.ConclusaoManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoResponse;
import com.locadora.manutencao.service.ManutencaoService;
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

@RestController
@RequestMapping("/api/v1/manutencoes")
@Tag(name = "Manutenção", description = "Controle de despesas de oficina e revisões preventivas/corretivas")
public class ManutencaoController {

    private final ManutencaoService manutencaoService;

    public ManutencaoController(ManutencaoService manutencaoService) {
        this.manutencaoService = manutencaoService;
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Enviar para oficina", description = "Registra o envio do carro, bloqueando seu status para locação")
    public ResponseEntity<ApiResponse<ManutencaoResponse>> iniciar(@Valid @RequestBody ManutencaoRequest request) {
        ManutencaoResponse response = manutencaoService.iniciar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Carro enviado para manutenção com sucesso."));
    }

    @PutMapping("/{id}/concluir")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Concluir serviço", description = "Libera o veículo de volta à frota e gera uma despesa no financeiro")
    public ResponseEntity<ApiResponse<ManutencaoResponse>> concluir(@PathVariable UUID id, 
                                                                    @Valid @RequestBody ConclusaoManutencaoRequest request) {
        ManutencaoResponse response = manutencaoService.concluir(id, request);
        return ResponseEntity.ok(ApiResponse.of(response, "Manutenção concluída e veículo liberado."));
    }

    @GetMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Listar manutenções", description = "Lista o diário de manutenções de toda a frota")
    public ResponseEntity<PagedResponse<ManutencaoResponse>> listar(@PageableDefault(size = 20) Pageable pageable) {
        return ResponseEntity.ok(manutencaoService.listar(pageable));
    }

    @GetMapping("/veiculo/{veiculoId}")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE', 'OPERADOR')")
    @Operation(summary = "Histórico do veículo", description = "Busca manutenções de um veículo específico")
    public ResponseEntity<PagedResponse<ManutencaoResponse>> listarPorVeiculo(@PathVariable UUID veiculoId, 
                                                                              @PageableDefault(size = 20) Pageable pageable) {
        return ResponseEntity.ok(manutencaoService.listarPorVeiculo(veiculoId, pageable));
    }
}
