-- V2: Tabela de Usuários
-- Conforme RF-006 a RF-010 e 06-modelo-fisico.md.
-- Todo usuário pertence obrigatoriamente a um tenant.

CREATE TABLE usuarios (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    nome            VARCHAR(200) NOT NULL,
    email           VARCHAR(200) NOT NULL,
    senha           VARCHAR(255) NOT NULL,
    ativo           BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by      UUID,
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by      UUID,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    deleted_by      UUID,
    version         BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_usuarios_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT uk_usuarios_email UNIQUE (email)
);

-- Índices obrigatórios
CREATE INDEX idx_usuarios_tenant_id ON usuarios (tenant_id);
CREATE INDEX idx_usuarios_email ON usuarios (email);
