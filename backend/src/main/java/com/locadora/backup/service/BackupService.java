package com.locadora.backup.service;

import com.locadora.common.exception.BusinessException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Serviço de backup local para o banco de dados SQLite.
 */
@Service
public class BackupService {

    private static final Logger log = LoggerFactory.getLogger(BackupService.class);
    private static final String DATABASE_PATH = "database/locadora.db";
    private static final String BACKUP_DIR = "backup";

    public String criarBackup() {
        Path source = Paths.get(DATABASE_PATH);
        if (!Files.exists(source)) {
            throw new BusinessException("Banco de dados local não encontrado para realizar o backup.");
        }

        // Criar pasta de backup se não existir
        Path backupDirPath = Paths.get(BACKUP_DIR);
        try {
            if (!Files.exists(backupDirPath)) {
                Files.createDirectories(backupDirPath);
            }
        } catch (IOException e) {
            log.error("Erro ao criar diretório de backups: {}", e.getMessage());
            throw new BusinessException("Não foi possível criar o diretório de backups.");
        }

        // Definir nome do arquivo com timestamp: locadora-yyyy-MM-dd-HH-mm.db
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd-HH-mm"));
        String backupFileName = String.format("locadora-%s.db", timestamp);
        Path target = backupDirPath.resolve(backupFileName);

        try {
            Files.copy(source, target);
            log.info("Backup do SQLite criado com sucesso em: {}", target.toAbsolutePath());
            return backupFileName;
        } catch (IOException e) {
            log.error("Falha ao copiar arquivo do banco para backup: {}", e.getMessage());
            throw new BusinessException("Erro de I/O ao gerar o backup do banco de dados.");
        }
    }
}
