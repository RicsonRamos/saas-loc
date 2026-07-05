package com.locadora.frota.entity;

import com.locadora.common.entity.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "documentos_veiculos")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class DocumentoVeiculo extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "veiculo_id", nullable = false)
    private Veiculo veiculo;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private TipoDocumentoVeiculo tipo;

    @Column(length = 100)
    private String numero;

    @Column(name = "data_emissao")
    private LocalDate dataEmissao;

    @Column(nullable = false)
    private LocalDate validade;

    @Column(name = "upload_id")
    private UUID uploadId;

    @Column(columnDefinition = "TEXT")
    private String observacoes;
}
