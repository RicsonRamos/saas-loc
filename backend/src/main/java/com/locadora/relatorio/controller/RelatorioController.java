package com.locadora.relatorio.controller;

import com.locadora.relatorio.service.RelatorioService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDate;

@RestController
@RequestMapping("/api/v1/relatorios")
@Tag(name = "Relatórios", description = "Exportação de relatórios físicos (PDF, CSV)")
public class RelatorioController {

    private final RelatorioService relatorioService;

    public RelatorioController(RelatorioService relatorioService) {
        this.relatorioService = relatorioService;
    }

    @GetMapping("/fluxo-caixa/csv")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Exportar Excel (CSV)", description = "Baixa o extrato financeiro do mês em CSV.")
    public ResponseEntity<byte[]> baixarCsvFluxoCaixa(
            @RequestParam(required = false) Integer ano,
            @RequestParam(required = false) Integer mes) {

        if (ano == null || mes == null) {
            LocalDate hoje = LocalDate.now();
            ano = hoje.getYear();
            mes = hoje.getMonthValue();
        }

        byte[] arquivo = relatorioService.gerarCsvFluxoCaixa(ano, mes);
        String nomeArquivo = String.format("extrato_%d_%d.csv", ano, mes);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + nomeArquivo)
                .contentType(MediaType.parseMediaType("text/csv"))
                .body(arquivo);
    }

    @GetMapping("/fluxo-caixa/pdf")
    @PreAuthorize("hasAnyRole('ADMIN', 'GERENTE')")
    @Operation(summary = "Exportar PDF", description = "Baixa o extrato financeiro do mês formatado em PDF para impressão.")
    public ResponseEntity<byte[]> baixarPdfFluxoCaixa(
            @RequestParam(required = false) Integer ano,
            @RequestParam(required = false) Integer mes) {

        if (ano == null || mes == null) {
            LocalDate hoje = LocalDate.now();
            ano = hoje.getYear();
            mes = hoje.getMonthValue();
        }

        byte[] arquivo = relatorioService.gerarPdfFluxoCaixa(ano, mes);
        String nomeArquivo = String.format("extrato_%d_%d.pdf", ano, mes);

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + nomeArquivo)
                .contentType(MediaType.APPLICATION_PDF)
                .body(arquivo);
    }
}
