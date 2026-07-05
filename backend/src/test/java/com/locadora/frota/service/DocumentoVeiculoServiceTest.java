package com.locadora.frota.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.frota.dto.DocumentoVeiculoRequest;
import com.locadora.frota.dto.DocumentoVeiculoResponse;
import com.locadora.frota.entity.DocumentoVeiculo;
import com.locadora.frota.entity.TipoDocumentoVeiculo;
import com.locadora.frota.entity.Veiculo;
import com.locadora.frota.mapper.DocumentoVeiculoMapper;
import com.locadora.frota.repository.DocumentoVeiculoRepository;
import com.locadora.frota.repository.VeiculoRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DocumentoVeiculoServiceTest {

    @Mock private DocumentoVeiculoRepository repository;
    @Mock private DocumentoVeiculoMapper mapper;
    @Mock private VeiculoRepository veiculoRepository;
    @InjectMocks private DocumentoVeiculoService service;

    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setPlaca("ABC-1234");
    }

    @Test
    void deveCriarDocumentoComSucesso() {
        DocumentoVeiculoRequest request = new DocumentoVeiculoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setTipo(TipoDocumentoVeiculo.IPVA);
        request.setValidade(LocalDate.now().plusMonths(6));

        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));
        when(repository.findByVeiculoIdAndTipoAndDeletedAtIsNull(veiculo.getId(), TipoDocumentoVeiculo.IPVA)).thenReturn(Optional.empty());
        when(mapper.toEntity(request)).thenReturn(new DocumentoVeiculo());
        when(repository.save(any())).thenReturn(new DocumentoVeiculo());
        when(mapper.toResponse(any())).thenReturn(new DocumentoVeiculoResponse());

        DocumentoVeiculoResponse response = service.criar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveCriarDocumentoTipoDuplicado() {
        DocumentoVeiculoRequest request = new DocumentoVeiculoRequest();
        request.setVeiculoId(veiculo.getId());
        request.setTipo(TipoDocumentoVeiculo.IPVA);

        when(veiculoRepository.findByIdAndDeletedAtIsNull(veiculo.getId())).thenReturn(Optional.of(veiculo));
        when(repository.findByVeiculoIdAndTipoAndDeletedAtIsNull(veiculo.getId(), TipoDocumentoVeiculo.IPVA)).thenReturn(Optional.of(new DocumentoVeiculo()));

        assertThrows(BusinessException.class, () -> service.criar(request));
    }
}
