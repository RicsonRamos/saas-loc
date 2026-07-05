package com.locadora.upload.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.upload.entity.Upload;
import com.locadora.upload.repository.UploadRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import java.nio.file.Path;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class LocalStorageServiceTest {

    @Mock private UploadRepository repository;
    private LocalStorageService storageService;

    @BeforeEach
    void setUp(@TempDir Path tempDir) {
        storageService = new LocalStorageService(tempDir.toString(), repository);
    }

    @Test
    void deveSalvarUploadDeImagemComSucesso() {
        InputStream stream = new ByteArrayInputStream("imagem_falsa_bytes".getBytes());
        UUID relacionamentoId = UUID.randomUUID();
        UUID usuarioId = UUID.randomUUID();

        Upload uploadMock = new Upload();
        uploadMock.setUuidArquivo(UUID.randomUUID());

        when(repository.save(any(Upload.class))).thenReturn(uploadMock);

        Upload upload = storageService.salvar(
                stream,
                "foto.png",
                "image/png",
                "CLIENTES",
                relacionamentoId,
                usuarioId
        );

        assertNotNull(upload);
    }

    @Test
    void naoDeveSalvarMimeTypeInvalido() {
        InputStream stream = new ByteArrayInputStream("bytes".getBytes());
        UUID relacionamentoId = UUID.randomUUID();

        assertThrows(BusinessException.class, () -> storageService.salvar(
                stream,
                "documento.zip",
                "application/zip",
                "CLIENTES",
                relacionamentoId,
                UUID.randomUUID()
        ));
    }
}
