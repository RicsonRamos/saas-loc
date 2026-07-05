package com.locadora.relatorio.service;

import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RelatorioServiceTest {

    @Mock private LancamentoFinanceiroRepository repository;
    @InjectMocks private RelatorioService relatorioService;

    @Test
    void deveGerarCsvCorretamente() {
        LancamentoFinanceiro lancamento = new LancamentoFinanceiro();
        lancamento.setDataPagamento(LocalDate.of(2023, 10, 1));
        lancamento.setTipo(TipoTransacao.RECEITA);
        lancamento.setCategoria(CategoriaFinanceira.LOCACAO);
        lancamento.setDescricao("Contrato;123");
        lancamento.setValor(new BigDecimal("500.00"));

        when(repository.findByDataPagamentoBetweenAndDeletedAtIsNullOrderByDataPagamentoDesc(
                any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(List.of(lancamento));

        byte[] csvBytes = relatorioService.gerarCsvFluxoCaixa(2023, 10);
        String csvString = new String(csvBytes);

        assertTrue(csvString.contains("Data;Tipo;Categoria;Descricao;Valor"));
        assertTrue(csvString.contains("Contrato,123")); // ; substituído por , no CSV
    }
}
