package com.locadora.empresa.entity;

import com.locadora.common.entity.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Aggregate Root: Empresa (Locadora).
 * Conforme 05-modelo-dominio.md e RF-001 a RF-005.
 *
 * A empresa é o tenant root. O id da empresa É o tenant_id.
 */
@Entity
@Table(name = "empresas")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Empresa extends BaseEntity {

    @Column(name = "nome_fantasia", nullable = false, length = 200)
    private String nomeFantasia;

    @Column(name = "razao_social", nullable = false, length = 300)
    private String razaoSocial;

    @Column(nullable = false, unique = true, length = 18)
    private String cnpj;

    @Column(length = 500)
    private String endereco;

    @Column(length = 20)
    private String telefone;

    @Column(length = 200)
    private String email;

    @Column(name = "logo_url", length = 500)
    private String logoUrl;

    @Column(nullable = false)
    @Builder.Default
    private Boolean ativo = true;
}
