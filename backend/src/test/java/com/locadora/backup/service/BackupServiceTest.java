package com.locadora.backup.service;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BackupServiceTest {

    private BackupService service;
    private Path tempDbFile;

    @BeforeEach
    void setUp(@TempDir Path tempDir) throws IOException {
        service = new BackupService();
        
        // Crie pasta fake 'database' e 'backup' no diretório de execução do teste
        Files.createDirectories(Paths.get("database"));
        Files.createDirectories(Paths.get("backup"));
        
        tempDbFile = Paths.get("database/locadora.db");
        Files.writeString(tempDbFile, "fake sqlite content");
    }

    @AfterEach
    void tearDown() throws IOException {
        Files.deleteIfExists(tempDbFile);
        Files.deleteIfExists(Paths.get("database"));
        
        // Limpar backups gerados
        Files.walk(Paths.get("backup"))
                .filter(Files::isRegularFile)
                .forEach(path -> {
                    try {
                        Files.delete(path);
                    } catch (IOException ignored) {}
                });
        Files.deleteIfExists(Paths.get("backup"));
    }

    @Test
    void deveCriarBackupComSucesso() {
        String filename = service.criarBackup();
        assertNotNull(filename);
        assertTrue(filename.startsWith("locadora-"));
        assertTrue(Files.exists(Paths.get("backup").resolve(filename)));
    }
}
