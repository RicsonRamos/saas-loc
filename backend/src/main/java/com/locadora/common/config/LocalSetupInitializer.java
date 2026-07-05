package com.locadora.common.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

/**
 * Inicializador do ambiente local/desktop.
 * Garante que os diretórios necessários (database, logs, backup, config)
 * e o arquivo de configuração local estejam presentes antes do uso.
 */
@Component
public class LocalSetupInitializer implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(LocalSetupInitializer.class);

    @Override
    public void run(String... args) throws Exception {
        log.info("Inicializando verificação do ambiente local...");

        // 1. Criar pastas necessárias
        criarDiretorioSeNaoExistir("database");
        criarDiretorioSeNaoExistir("logs");
        criarDiretorioSeNaoExistir("backup");
        criarDiretorioSeNaoExistir("config");
        criarDiretorioSeNaoExistir("uploads");

        // 2. Criar config/application.properties se não existir
        Path configFilePath = Paths.get("config/application.properties");
        if (!Files.exists(configFilePath)) {
            List<String> defaultLines = List.of(
                    "# Configurações Locais - Locadora ERP Desktop",
                    "server.port=8080",
                    "app.company.name=Locadora Local",
                    "app.language=pt-BR",
                    "app.timezone=America/Sao_Paulo"
            );
            try {
                Files.write(configFilePath, defaultLines);
                log.info("Arquivo de configuração padrão criado em 'config/application.properties'.");
            } catch (IOException e) {
                log.error("Não foi possível criar o arquivo 'config/application.properties': {}", e.getMessage());
            }
        } else {
            log.info("Arquivo 'config/application.properties' detectado.");
        }
    }

    private void criarDiretorioSeNaoExistir(String nomePasta) {
        Path path = Paths.get(nomePasta);
        if (!Files.exists(path)) {
            try {
                Files.createDirectories(path);
                log.info("Diretório '{}' criado com sucesso.", nomePasta);
            } catch (IOException e) {
                log.error("Erro ao criar diretório '{}': {}", nomePasta, e.getMessage());
            }
        }
    }
}
