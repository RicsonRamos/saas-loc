package com.locadora.upload.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "uploads")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Upload {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    @Column(updatable = false, nullable = false)
    private UUID id;

    @Column(name = "uuid_arquivo", nullable = false, unique = true)
    private UUID uuidArquivo;

    @Column(name = "hash_sha256", nullable = false, length = 64)
    private String hashSha256;

    @Column(name = "mime_type", nullable = false, length = 100)
    private String mimeType;

    @Column(name = "nome_original", nullable = false, length = 255)
    private String nomeOriginal;

    @Column(nullable = false)
    private Long tamanho;

    private Integer altura;
    private Integer largura;

    @Column(name = "usuario_id")
    private UUID usuarioId;

    @Column(name = "relacionamento_tipo", nullable = false, length = 50)
    private String relacionamentoTipo;

    @Column(name = "relacionamento_id", nullable = false)
    private UUID relacionamentoId;

    @Column(name = "caminho_arquivo", nullable = false, length = 500)
    private String caminhoArquivo;

    @Column(name = "created_at", nullable = false, updatable = false)
    @Builder.Default
    private LocalDateTime createdAt = LocalDateTime.now();
}
