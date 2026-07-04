-- V5: Tabela de Clientes
-- Conforme 05-modelo-dominio.md e 06-modelo-fisico.md

CREATE TABLE clientes (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    nome            VARCHAR(200) NOT NULL,
    tipo            VARCHAR(20) NOT NULL,
    documento       VARCHAR(20) NOT NULL,
    email           VARCHAR(200),
    telefone        VARCHAR(20),
    cnh             VARCHAR(20),
    cnh_validade    DATE,
    
    -- Endereço
    cep             VARCHAR(10),
    logradouro      VARCHAR(200),
    numero          VARCHAR(20),
    complemento     VARCHAR(100),
    bairro          VARCHAR(100),
    cidade          VARCHAR(100),
    uf              VARCHAR(2),
    
    -- URLs
    cnh_url         VARCHAR(500),
    comprovante_residencia_url VARCHAR(500),
    
    -- Colunas base
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by      UUID,
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by      UUID,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    deleted_by      UUID,
    version         BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_clientes_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT uk_clientes_documento_tenant UNIQUE (documento, tenant_id)
);

-- Índices obrigatórios
CREATE INDEX idx_clientes_tenant_id ON clientes (tenant_id);
CREATE INDEX idx_clientes_documento ON clientes (documento);
CREATE INDEX idx_clientes_nome ON clientes (nome);
