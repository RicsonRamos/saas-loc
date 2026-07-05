package com.locadora.cliente.entity;

import com.locadora.common.entity.BaseEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/**
 * Aggregate Root: Cliente.
 * Conforme 05-modelo-dominio.md.
 */
@Entity
@Table(name = "clientes", uniqueConstraints = {
        @UniqueConstraint(name = "uk_clientes_documento", columnNames = {"documento"})
})
@Getter
@Setter
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Cliente extends BaseEntity {

    @Column(nullable = false, length = 200)
    private String nome;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TipoCliente tipo;

    @Column(nullable = false, length = 20)
    private String documento; // CPF ou CNPJ

    @Column(length = 200)
    private String email;

    @Column(length = 20)
    private String telefone;

    @Column(length = 20)
    private String cnh;

    @Column(name = "cnh_validade")
    private java.time.LocalDate cnhValidade;

    // Endereço integrado para simplificação do MVP
    @Column(length = 10)
    private String cep;

    @Column(length = 200)
    private String logradouro;

    @Column(length = 20)
    private String numero;

    @Column(length = 100)
    private String complemento;

    @Column(length = 100)
    private String bairro;

    @Column(length = 100)
    private String cidade;

    @Column(length = 2)
    private String uf;

    // URLs de documentos (CNH, Comprovante Residência)
    @Column(name = "cnh_url", length = 500)
    private String cnhUrl;

    @Column(name = "comprovante_residencia_url", length = 500)
    private String comprovanteResidenciaUrl;
}
