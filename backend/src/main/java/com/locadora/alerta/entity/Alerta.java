package com.locadora.alerta.entity;

import com.locadora.common.entity.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "alertas")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Alerta extends BaseEntity {

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private TipoAlerta tipo;

    @Column(nullable = false, length = 255)
    private String titulo;

    @Column(nullable = false, length = 500)
    private String descricao;

    @Column(name = "entidade_id", nullable = false)
    private UUID entidadeId;

    @Column(nullable = false)
    @Builder.Default
    private Boolean lido = false;

    @Column(name = "data_alerta", nullable = false)
    @Builder.Default
    private LocalDate dataAlerta = LocalDate.now();
}
