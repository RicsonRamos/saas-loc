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
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockedStatic;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mockStatic;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class DocumentoVeiculoServiceTest {

    @Mock private DocumentoVeiculoRepository repository;
    @Mock private DocumentoVeiculoMapper mapper;
    @Mock private VeiculoRepository veiculoRepository;
    @InjectMocks private DocumentoVeiculoService service;

    private MockedStatic<TenantContext> tenantContextMock;
    private final UUID TENANT_ID = UUID.randomUUID();

    private Veiculo veiculo;

    @BeforeEach
    void setUp() {
        tenantContextMock = mockStatic(TenantContext.class);
        tenantContextMock.when(TenantContext::getTenantId).thenReturn(TENANT_ID);

        veiculo = new Veiculo();
        veiculo.setId(UUID.randomUUID());
        veiculo.setPlaca("ABC-1234");
    }

    @AfterEach
    void tearDown() {
        tenantContextMock.close();
    }

    @Test
    void deveCriarDocumentoComSucesso() {
        DocumentoVeiculoRequest request = DocumentoVeiculoRequest.builder()
                .veiculoId(veiculo.getId())
                .tipo(TipoDocumentoVeiculo.IPVA)
                .validade(LocalDate.now().plusMonths(6))
                .build();

        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TENANT_ID)).thenReturn(Optional.of(veiculo));
        when(repository.findByVeiculoIdAndTipoAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TipoDocumentoVeiculo.IPVA, TENANT_ID)).thenReturn(Optional.empty());
        when(mapper.toEntity(request)).thenReturn(new DocumentoVeiculo());
        when(repository.save(any())).thenReturn(new DocumentoVeiculo());
        when(mapper.toResponse(any())).thenReturn(new DocumentoVeiculoResponse());

        DocumentoVeiculoResponse response = service.criar(request);
        assertNotNull(response);
    }

    @Test
    void naoDeveCriarDocumentoTipoDuplicado() {
        DocumentoVeiculoRequest request = DocumentoVeiculoRequest.builder()
                .veiculoId(veiculo.getId())
                .tipo(TipoDocumentoVeiculo.IPVA)
                .build();

        when(veiculoRepository.findByIdAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TENANT_ID)).thenReturn(Optional.of(veiculo));
        when(repository.findByVeiculoIdAndTipoAndTenantIdAndDeletedAtIsNull(veiculo.getId(), TipoDocumentoVeiculo.IPVA, TENANT_ID)).thenReturn(Optional.of(new DocumentoVeiculo()));

        assertThrows(BusinessException.class, () -> service.criar(request));
    }
}
