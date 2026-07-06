package com.locadora.financeiro.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.contrato.repository.ContratoRepository;
import com.locadora.financeiro.dto.LancamentoRequest;
import com.locadora.financeiro.dto.LancamentoResponse;
import com.locadora.financeiro.entity.CategoriaFinanceira;
import com.locadora.financeiro.entity.LancamentoFinanceiro;
import com.locadora.financeiro.entity.StatusPagamento;
import com.locadora.financeiro.entity.TipoTransacao;
import com.locadora.financeiro.mapper.LancamentoMapper;
import com.locadora.financeiro.repository.LancamentoFinanceiroRepository;
import com.locadora.frota.repository.VeiculoRepository;
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
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class FinanceiroServiceTest {

    @Mock private LancamentoFinanceiroRepository repository;
    @Mock private LancamentoMapper lancamentoMapper;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private ContratoRepository contratoRepository;
    @InjectMocks private FinanceiroService financeiroService;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private LancamentoFinanceiro lancamento;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        lancamento = new LancamentoFinanceiro();
        lancamento.setId(UUID.randomUUID());
        lancamento.setValor(new BigDecimal("100.00"));
        lancamento.setStatus(StatusPagamento.PENDENTE);
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    @Test
    void deveCriarLancamento() {
        LancamentoRequest request = LancamentoRequest.builder()
                .tipo(TipoTransacao.RECEITA)
                .categoria(CategoriaFinanceira.ALUGUEL)
                .descricao("Teste")
                .valor(new BigDecimal("150.00"))
                .dataVencimento(LocalDate.now())
                .build();

        when(lancamentoMapper.toEntity(request)).thenReturn(lancamento);
        when(repository.save(any())).thenReturn(lancamento);
        when(lancamentoMapper.toResponse(any())).thenReturn(new LancamentoResponse());

        financeiroService.criarLancamento(request);
        verify(repository).save(any());
    }

    @Test
    void devePagarLancamento() {
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(lancamento.getId(), TENANT_ID))
                .thenReturn(Optional.of(lancamento));

        financeiroService.pagarLancamento(lancamento.getId());

        assertEquals(StatusPagamento.PAGO, lancamento.getStatus());
        assertEquals(LocalDate.now(), lancamento.getDataPagamento());
        verify(repository).save(lancamento);
    }

    @Test
    void naoDevePagarLancamentoJaPago() {
        lancamento.setStatus(StatusPagamento.PAGO);
        when(repository.findByIdAndTenantIdAndDeletedAtIsNull(lancamento.getId(), TENANT_ID))
                .thenReturn(Optional.of(lancamento));
        assertThrows(BusinessException.class, () -> financeiroService.pagarLancamento(lancamento.getId()));
    }
}
