package com.locadora.upload.repository;

import com.locadora.upload.entity.Upload;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface UploadRepository extends JpaRepository<Upload, UUID> {

    Optional<Upload> findByUuidArquivo(UUID uuidArquivo);

    List<Upload> findByRelacionamentoTipoAndRelacionamentoId(String relacionamentoTipo, UUID relacionamentoId);
}
