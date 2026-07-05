package com.locadora.upload.service;

import com.locadora.common.exception.BusinessException;
import com.locadora.common.exception.ResourceNotFoundException;
import com.locadora.upload.entity.Upload;
import com.locadora.upload.repository.UploadRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.List;
import java.util.Set;
import java.util.UUID;

@Service
public class LocalStorageService implements StorageService {

    private static final Set<String> ALLOWED_MIME_TYPES = Set.of(
            "application/pdf",
            "image/png",
            "image/jpeg",
            "image/webp"
    );

    private final Path uploadRootPath;
    private final UploadRepository repository;

    public LocalStorageService(@Value("${app.upload.dir:uploads}") String uploadDir,
                               UploadRepository repository) {
        this.uploadRootPath = Paths.get(uploadDir).toAbsolutePath().normalize();
        this.repository = repository;
        try {
            Files.createDirectories(this.uploadRootPath);
        } catch (IOException e) {
            throw new RuntimeException("Não foi possível criar o diretório de uploads.", e);
        }
    }

    @Override
    @Transactional
    public Upload salvar(InputStream inputStream, String nomeOriginal, String mimeType,
                         String relacionamentoTipo, UUID relacionamentoId, UUID usuarioId) {
        
        if (!ALLOWED_MIME_TYPES.contains(mimeType.toLowerCase())) {
            throw new BusinessException("Mime type não suportado. Apenas PDF, PNG, JPEG e WEBP são permitidos.");
        }

        UUID fileUuid = UUID.randomUUID();
        String extensao = obterExtensao(nomeOriginal);
        String nomeArquivoFisico = fileUuid + (extensao.isEmpty() ? "" : "." + extensao);
        
        // Define sub-pasta com base no relacionamento (ex: CLIENTES -> clientes)
        String subPasta = relacionamentoTipo.toLowerCase().trim();
        Path pastaDestino = this.uploadRootPath.resolve(subPasta);
        
        try {
            Files.createDirectories(pastaDestino);
        } catch (IOException e) {
            throw new BusinessException("Erro ao criar sub-pasta do upload: " + subPasta);
        }

        Path caminhoFisico = pastaDestino.resolve(nomeArquivoFisico);

        // Copiar o input stream para byte array para calcular hash e ler imagem
        ByteArrayOutputStream buffer = new ByteArrayOutputStream();
        byte[] data;
        try {
            byte[] temp = new byte[4096];
            int read;
            while ((read = inputStream.read(temp, 0, temp.length)) != -1) {
                buffer.write(temp, 0, read);
            }
            data = buffer.toByteArray();
        } catch (IOException e) {
            throw new BusinessException("Erro ao ler dados do arquivo enviado.");
        }

        // 1. Gravar arquivo físico
        try {
            Files.copy(new ByteArrayInputStream(data), caminhoFisico, StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            throw new BusinessException("Erro ao salvar arquivo no disco local.");
        }

        // 2. Calcular hash SHA-256
        String hashSha256 = calcularHash(data);

        // 3. Obter dimensões se for imagem
        Integer largura = null;
        Integer altura = null;
        if (mimeType.toLowerCase().startsWith("image/")) {
            try {
                BufferedImage img = ImageIO.read(new ByteArrayInputStream(data));
                if (img != null) {
                    largura = img.getWidth();
                    altura = img.getHeight();
                }
            } catch (Exception e) {
                // Silencia se não for possível ler (ex: formato webp sem suporte nativo em JDK antigo)
            }
        }

        // 4. Salvar registro no banco
        Upload upload = Upload.builder()
                .uuidArquivo(fileUuid)
                .hashSha256(hashSha256)
                .mimeType(mimeType)
                .nomeOriginal(nomeOriginal)
                .tamanho((long) data.length)
                .largura(largura)
                .altura(altura)
                .usuarioId(usuarioId)
                .relacionamentoTipo(relacionamentoTipo.toUpperCase())
                .relacionamentoId(relacionamentoId)
                .caminhoArquivo(caminhoFisico.toString())
                .build();

        return repository.save(upload);
    }

    @Override
    @Transactional(readOnly = true)
    public byte[] obter(UUID uuidArquivo) {
        Upload upload = repository.findByUuidArquivo(uuidArquivo)
                .orElseThrow(() -> new ResourceNotFoundException("Upload", "uuid", uuidArquivo));

        Path path = Paths.get(upload.getCaminhoArquivo());
        try {
            return Files.readAllBytes(path);
        } catch (IOException e) {
            throw new BusinessException("Erro ao ler arquivo físico no disco.");
        }
    }

    @Override
    @Transactional
    public void deletar(UUID uuidArquivo) {
        Upload upload = repository.findByUuidArquivo(uuidArquivo)
                .orElseThrow(() -> new ResourceNotFoundException("Upload", "uuid", uuidArquivo));

        Path path = Paths.get(upload.getCaminhoArquivo());
        try {
            Files.deleteIfExists(path);
        } catch (IOException e) {
            // Logar o erro mas prosseguir com a remoção lógica/banco
        }

        repository.delete(upload);
    }

    @Override
    @Transactional(readOnly = true)
    public List<Upload> listarPorRelacionamento(String relacionamentoTipo, UUID relacionamentoId) {
        return repository.findByRelacionamentoTipoAndRelacionamentoId(relacionamentoTipo.toUpperCase(), relacionamentoId);
    }

    private String obterExtensao(String nome) {
        if (nome == null || !nome.contains(".")) return "";
        return nome.substring(nome.lastIndexOf(".") + 1);
    }

    private String calcularHash(byte[] data) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] encodedHash = digest.digest(data);
            StringBuilder hexString = new StringBuilder(2 * encodedHash.length);
            for (byte b : encodedHash) {
                String hex = Integer.toHexString(0xff & b);
                if (hex.length() == 1) {
                    hexString.append('0');
                }
                hexString.append(hex);
            }
            return hexString.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 não disponível no Java.", e);
        }
    }
}
