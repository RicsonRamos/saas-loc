package com.locadora.relatorio.service;

import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

/**
 * Testes unitários do serviço de relatórios.
 * Valida geração correta de CSV (cabeçalho + escape de delimitador).
 */
@ExtendWith(MockitoExtension.class)
class RelatorioServiceTest {

    @Mock private LancamentoFinanceiroRepository repository;
    @InjectMocks private RelatorioService relatorioService;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    /**
     * Verifica que o CSV gerado contém o cabeçalho correto e faz escape do delimitador
     * ponto-e-vírgula nas descrições (substituindo por vírgula).
     */
    @Test
    void deveGerarCsvCorretamente() {
        LancamentoFinanceiro lancamento = new LancamentoFinanceiro();
        lancamento.setDataPagamento(LocalDate.of(2023, 10, 1));
        lancamento.setTipo(TipoTransacao.RECEITA);
        // LOCACAO foi renomeado para ALUGUEL no enum CategoriaFinanceira
        lancamento.setCategoria(CategoriaFinanceira.ALUGUEL);
        lancamento.setDescricao("Contrato;123");
        lancamento.setValor(new BigDecimal("500.00"));

        // Método agora inclui tenantId como primeiro parâmetro
        when(repository.findByTenantIdAndDataPagamentoBetweenAndDeletedAtIsNullOrderByDataPagamentoDesc(
                eq(TENANT_ID), any(LocalDate.class), any(LocalDate.class)))
                .thenReturn(List.of(lancamento));

        byte[] csvBytes = relatorioService.gerarCsvFluxoCaixa(2023, 10);
        String csvString = new String(csvBytes);

        assertTrue(csvString.contains("Data;Tipo;Categoria;Descricao;Valor"));
        assertTrue(csvString.contains("Contrato,123")); // ; substituído por , no CSV
    }
}
