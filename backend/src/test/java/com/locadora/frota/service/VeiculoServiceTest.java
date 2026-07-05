package com.locadora.frota.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.frota.dto.VeiculoRequest;
import com.locadora.frota.dto.VeiculoResponse;
import com.locadora.frota.entity.StatusVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.VeiculoMapper;
import com.locadora.frota.repository.VeiculoRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class VeiculoServiceTest {

    @Mock private VeiculoRepository veiculoRepository;
    @Mock private VeiculoMapper veiculoMapper;
    @InjectMocks private VeiculoService veiculoService;

    @Test
    void deveCriarVeiculoComSucesso() {
        VeiculoRequest request = new VeiculoRequest();
        request.setPlaca("ABC-1234");
        request.setChassi("CHASSI123");

        Veiculo veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setPlaca("ABC-1234");
        veiculo.setChassi("CHASSI123");

        when(veiculoMapper.toEntity(request)).thenReturn(veiculo);
        when(veiculoRepository.save(any())).thenReturn(veiculo);
        when(veiculoMapper.toResponse(veiculo)).thenReturn(new VeiculoResponse());

        VeiculoResponse response = veiculoService.criar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveExcluirVeiculoLocado() {
        UUID id = UUID.randomUUID();
        Veiculo veiculo = new Veiculo();
        veiculo.setId(id);
        veiculo.setStatus(StatusVeiculo.LOCADO);

        when(veiculoRepository.findByIdAndDeletedAtIsNull(id)).thenReturn(Optional.of(veiculo));

        assertThrows(BusinessException.class, () -> veiculoService.excluir(id, UUID.randomUUID()));
    }

    @Test
    void deveLancarExcecaoAoBuscarVeiculoInexistente() {
        UUID id = UUID.randomUUID();
        when(veiculoRepository.findByIdAndDeletedAtIsNull(id)).thenReturn(Optional.empty());
        assertThrows(ResourceNotFoundException.class, () -> veiculoService.buscarPorId(id));
    }
}
