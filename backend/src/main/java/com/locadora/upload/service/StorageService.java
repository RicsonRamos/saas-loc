package com.locadora.upload.service;

import com.locadora.upload.entity.Upload;
import java.io.InputStream;
import java.util.List;
import java.util.UUID;

public interface StorageService {

    Upload salvar(InputStream inputStream, String nomeOriginal, String mimeType, 
                  String relacionamentoTipo, UUID relacionamentoId, UUID usuarioId);

    byte[] obter(UUID uuidArquivo);

    void deletar(UUID uuidArquivo);

    List<Upload> listarPorRelacionamento(String relacionamentoTipo, UUID relacionamentoId);
}
