package com.locadora.financeiro.controller;

import com.locadora.common.dto.ApiResponse;
import com.locadora.common.dto.PagedResponse;
import com.locadora.financeiro.dto.FluxoCaixaResponse;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.dto.LancamentoResponse;
import com.locadora.financeiro.service.FinanceiroService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.data.domain.Pageable;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/financeiro")
@Tag(name = "Financeiro", description = "Gestão de Caixa (Receitas, Despesas e Fluxo)")
public class FinanceiroController {

    private final FinanceiroService financeiroService;

    public FinanceiroController(FinanceiroService financeiroService) {
        this.financeiroService = financeiroService;
    }

    @PostMapping("/lancamentos")
    @PreAuthorize("hasAnyRole('ADMIN', 'FINANCEIRO')")
    @Operation(summary = "Criar lançamento", description = "Registra uma transação manual (Despesa de oficina, impostos, etc)")
    public ResponseEntity<ApiResponse<LancamentoResponse>> criarLancamento(@Valid @RequestBody LancamentoRequest request) {
        LancamentoResponse response = financeiroService.criar(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(ApiResponse.of(response, "Lançamento financeiro registrado"));
    }

    @GetMapping("/lancamentos")
    @PreAuthorize("hasAnyRole('ADMIN', 'FINANCEIRO', 'GERENTE')")
    @Operation(summary = "Listar lançamentos", description = "Lista o extrato paginado da locadora")
    public ResponseEntity<PagedResponse<LancamentoResponse>> listarLancamentos(@PageableDefault(size = 30) Pageable pageable) {
        PagedResponse<LancamentoResponse> response = financeiroService.listar(pageable);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/fluxo-caixa")
    @PreAuthorize("hasAnyRole('ADMIN', 'FINANCEIRO', 'GERENTE')")
    @Operation(summary = "Apuração mensal", description = "Retorna receitas, despesas e lucro bruto de um mês/ano")
    public ResponseEntity<ApiResponse<FluxoCaixaResponse>> obterFluxoMensal(
            @RequestParam(required = false) Integer ano,
            @RequestParam(required = false) Integer mes) {
        
        if (ano == null || mes == null) {
            LocalDate hoje = LocalDate.now();
            ano = hoje.getYear();
            mes = hoje.getMonthValue();
        }
        
        FluxoCaixaResponse response = financeiroService.obterFluxoMensal(ano, mes);
        return ResponseEntity.ok(ApiResponse.of(response));
    }
}
