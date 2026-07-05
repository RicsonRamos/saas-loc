package com.locadora.manutencao.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.financeiro.service.FinanceiroService;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.repository.VeiculoRepository;
import com.locadora.manutencao.dto.ConclusaoManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoRequest;
import com.locadora.manutencao.dto.ManutencaoResponse;
import com.locadora.manutencao.entity.Manutencao;
import com.locadora.manutencao.mapper.ManutencaoMapper;
import com.locadora.manutencao.repository.ManutencaoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.math.BigDecimal;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class ManutencaoServiceTest {

    @Mock private ManutencaoRepository manutencaoRepository;
    @Mock private ManutencaoMapper manutencaoMapper;
    @Mock private VeiculoRepository veiculoRepository;
    @Mock private FinanceiroService financeiroService;
    @InjectMocks private ManutencaoService manutencaoService;

    private Veiculo veiculo;
    private Manutencao manutencao;

    @BeforeEach
    void setUp() {
        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setStatus(StatusVeiculo.DISPONIVEL);
        veiculo.setQuilometragem(50000);

        manutencao = new Manutencao();
        manutencao.setId(UUID.randomUUID());
        manutencao.setVeiculo(veiculo);
        manutencao.setDescricao("Troca de óleo");
    }

    @Test
    void naoDeveRegistrarManutencaoSeVeiculoLocado() {
        veiculo.setStatus(StatusVeiculo.LOCADO);
        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));

        ManutencaoRequest request = new ManutencaoRequest();
        request.setVeiculoId(veiculo.getId());

        assertThrows(BusinessException.class, () -> manutencaoService.registrarManutencao(request));
    }

    @Test
    void deveConcluirManutencaoEDesbloquearVeiculo() {
        when(manutencaoRepository.findByIdAndDeletedAtIsNull(manutencao.getId())).thenReturn(Optional.of(manutencao));
        when(manutencaoMapper.toResponse(any())).thenReturn(new ManutencaoResponse());

        ConclusaoManutencaoRequest request = new ConclusaoManutencaoRequest();
        request.setCusto(new BigDecimal("500.00"));

        manutencaoService.concluirManutencao(manutencao.getId(), request);

        assertNotNull(manutencao.getDataFim());
        assertEquals(new BigDecimal("500.00"), manutencao.getCusto());
        assertEquals(StatusVeiculo.DISPONIVEL, veiculo.getStatus());

        verify(financeiroService).criarLancamento(any());
        verify(manutencaoRepository).save(manutencao);
    }
}
