package com.locadora.relatorio.service;

import com.lowagie.text.Document;
import com.lowagie.text.Element;
import com.lowagie.text.Font;
import com.lowagie.text.Paragraph;
import com.lowagie.text.Phrase;
import com.lowagie.text.pdf.PdfPCell;
import com.lowagie.text.pdf.PdfPTable;
import com.lowagie.text.pdf.PdfWriter;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

import com.locadora.shared.tenant.TenantContext;

/**
 * Serviço de Relatórios — Multi-Tenant.
 * Compila dados do banco em arquivos físicos (CSV, PDF).
 */
@Service
public class RelatorioService {

    private final LancamentoFinanceiroRepository lancamentoRepository;

    public RelatorioService(LancamentoFinanceiroRepository lancamentoRepository) {
        this.lancamentoRepository = lancamentoRepository;
    }

    public byte[] gerarCsvFluxoCaixa(int ano, int mes) {
        List<LancamentoFinanceiro> lancamentos = buscarLancamentos(ano, mes);

        StringBuilder csv = new StringBuilder();
        csv.append("Data;Tipo;Categoria;Descricao;Valor\n");

        for (LancamentoFinanceiro l : lancamentos) {
            String data = l.getDataPagamento() != null ? l.getDataPagamento().toString() : l.getDataVencimento().toString();
            csv.append(String.format("%s;%s;%s;%s;%.2f\n",
                    data,
                    l.getTipo().name(),
                    l.getCategoria().name(),
                    l.getDescricao().replace(";", ","),
                    l.getValor()
            ));
        }
        return csv.toString().getBytes();
    }

    public byte[] gerarPdfFluxoCaixa(int ano, int mes) {
        List<LancamentoFinanceiro> lancamentos = buscarLancamentos(ano, mes);

        try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
            Document document = new Document();
            PdfWriter.getInstance(document, out);
            document.open();

            Font fontTitulo = new Font(Font.HELVETICA, 18, Font.BOLD);
            Paragraph titulo = new Paragraph("Extrato Financeiro - " + mes + "/" + ano, fontTitulo);
            titulo.setAlignment(Element.ALIGN_CENTER);
            document.add(titulo);
            document.add(new Paragraph(" "));

            PdfPTable table = new PdfPTable(5);
            table.setWidthPercentage(100);
            table.setWidths(new float[]{1.5f, 1.5f, 2f, 3f, 1.5f});

            Font fontHeader = new Font(Font.HELVETICA, 12, Font.BOLD);
            adicionarCelula(table, "Data", fontHeader);
            adicionarCelula(table, "Tipo", fontHeader);
            adicionarCelula(table, "Categoria", fontHeader);
            adicionarCelula(table, "Descrição", fontHeader);
            adicionarCelula(table, "Valor (R$)", fontHeader);

            BigDecimal saldo = BigDecimal.ZERO;

            for (LancamentoFinanceiro l : lancamentos) {
                String data = l.getDataPagamento() != null
                    ? l.getDataPagamento().format(DateTimeFormatter.ofPattern("dd/MM/yyyy"))
                    : "-";

                table.addCell(data);
                table.addCell(l.getTipo().name());
                table.addCell(l.getCategoria().name());
                table.addCell(l.getDescricao());
                table.addCell(l.getValor().toString());

                if (l.getTipo().name().equals("RECEITA")) {
                    saldo = saldo.add(l.getValor());
                } else {
                    saldo = saldo.subtract(l.getValor());
                }
            }

            document.add(table);
            document.add(new Paragraph(" "));

            Font fontSaldo = new Font(Font.HELVETICA, 14, Font.BOLD);
            Paragraph pSaldo = new Paragraph("Saldo Líquido do Período: R$ " + saldo, fontSaldo);
            pSaldo.setAlignment(Element.ALIGN_RIGHT);
            document.add(pSaldo);

            document.close();
            return out.toByteArray();
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar relatório PDF", e);
        }
    }

    private void adicionarCelula(PdfPTable table, String texto, Font font) {
        PdfPCell cell = new PdfPCell(new Phrase(texto, font));
        cell.setHorizontalAlignment(Element.ALIGN_CENTER);
        table.addCell(cell);
    }

    private List<LancamentoFinanceiro> buscarLancamentos(int ano, int mes) {
        LocalDate inicio = LocalDate.of(ano, mes, 1);
        LocalDate fim = inicio.withDayOfMonth(inicio.lengthOfMonth());
        return lancamentoRepository.findByTenantIdAndDataPagamentoBetweenAndDeletedAtIsNullOrderByDataPagamentoDesc(
                TenantContext.getTenantId(), inicio, fim);
    }
}
