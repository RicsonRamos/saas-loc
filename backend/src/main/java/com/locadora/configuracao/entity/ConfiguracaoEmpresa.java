package com.locadora.configuracao.entity;

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
 * Entidade que armazena as configurações globais da locadora (Single-Tenant).
 */
@Entity
@Table(name = "configuracao_empresa")
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ConfiguracaoEmpresa extends BaseEntity {

    @Column(name = "nome_fantasia", nullable = false, length = 200)
    private String nomeFantasia;

    @Column(name = "razao_social", nullable = false, length = 300)
    private String razaoSocial;

    @Column(nullable = false, unique = true, length = 18)
    private String cnpj;

    @Column(name = "inscricao_estadual", length = 30)
    private String inscricaoEstadual;

    @Column(length = 500)
    private String endereco;

    @Column(length = 20)
    private String telefone;

    @Column(length = 200)
    private String email;

    @Column(name = "logo_url", length = 500)
    private String logoUrl;

    @Column(name = "horario_funcionamento", length = 200)
    private String horarioFuncionamento;

    @Column(name = "politica_combustivel", columnDefinition = "TEXT")
    private String politicaCombustivel;

    @Column(name = "politica_quilometragem", columnDefinition = "TEXT")
    private String politicaQuilometragem;

    @Column(name = "informacoes_fiscais", columnDefinition = "TEXT")
    private String informacoesFiscais;
}
