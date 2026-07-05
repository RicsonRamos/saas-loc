package com.locadora.contrato.entity;

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

@Entity
@Table(name = "checklists")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Checklist extends BaseEntity {

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "contrato_id", nullable = false)
    private Contrato contrato;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TipoChecklist tipo;

    @Column(name = "itens_json", nullable = false, columnDefinition = "TEXT")
    private String itensJson; // Ex: [{"item": "Estepe", "estado": "OK"}, ...]

    @Column(name = "fotos_json", columnDefinition = "TEXT")
    private String fotosJson; // Ex: ["url1", "url2"]

    @Column(name = "assinatura_cliente_url", length = 500)
    private String assinaturaClienteUrl;

    @Column(name = "assinatura_operador_url", length = 500)
    private String assinaturaOperadorUrl;
}
