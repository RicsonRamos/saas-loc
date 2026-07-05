package com.locadora.financeiro.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.shared.tenant.TenantContext;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class FinanceiroServiceTest {

    @Mock
    private LancamentoFinanceiroRepository repository;

    @InjectMocks
    private FinanceiroService financeiroService;

    private final UUID tenantId = UUID.randomUUID();
    private LancamentoFinanceiro lancamento;

    @BeforeEach
    void setUp() {
        TenantContext.setTenantId(tenantId);
        
        lancamento = new LancamentoFinanceiro();
        lancamento.setId(UUID.randomUUID());
        lancamento.setTenantId(tenantId);
        lancamento.setValor(new BigDecimal("100.00"));
        lancamento.setStatus(StatusPagamento.PENDENTE);
    }

    @AfterEach
    void tearDown() {
        TenantContext.clear();
    }

    @Test
    void deveCriarLancamentoPendente() {
        LancamentoRequest request = new LancamentoRequest();
        request.setTipo(TipoTransacao.RECEITA);
        request.setCategoria(CategoriaFinanceira.LOCACAO);
        request.setDescricao("Teste");
        request.setValor(new BigDecimal("150.00"));
        request.setDataVencimento(LocalDate.now());

        when(repository.save(any())).thenAnswer(i -> i.getArgument(0));

        financeiroService.criarLancamento(request);
        verify(repository).save(any());
    }

    @Test
    void devePagarLancamentoEAtualizarDataPagamento() {
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(lancamento.getId(), tenantId))
                .thenReturn(Optional.of(lancamento));
                
        financeiroService.pagarLancamento(lancamento.getId());
        
        assertEquals(StatusPagamento.PAGO, lancamento.getStatus());
        assertEquals(LocalDate.now(), lancamento.getDataPagamento());
        verify(repository).save(lancamento);
    }

    @Test
    void naoDevePagarLancamentoJaPago() {
        lancamento.setStatus(StatusPagamento.PAGO);
        
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(lancamento.getId(), tenantId))
                .thenReturn(Optional.of(lancamento));
                
        assertThrows(BusinessException.class, () -> financeiroService.pagarLancamento(lancamento.getId()));
    }
}
