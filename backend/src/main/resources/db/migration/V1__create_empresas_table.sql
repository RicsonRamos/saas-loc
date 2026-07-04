-- V1: Tabela de Empresas (Tenant Root)
-- Conforme 06-modelo-fisico.md: todas as tabelas possuem colunas obrigatórias.
-- Chaves primárias: UUID. Datas: TIMESTAMP WITH TIME ZONE. Soft Delete obrigatório.

CREATE TABLE empresas (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    nome_fantasia   VARCHAR(200) NOT NULL,
    razao_social    VARCHAR(300) NOT NULL,
    cnpj            VARCHAR(18) NOT NULL,
    endereco        VARCHAR(500),
    telefone        VARCHAR(20),
    email           VARCHAR(200),
    logo_url        VARCHAR(500),
    ativo           BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by      UUID,
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by      UUID,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    deleted_by      UUID,
    version         BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT uk_empresas_cnpj UNIQUE (cnpj)
);

-- Índices obrigatórios conforme 06-modelo-fisico.md
CREATE INDEX idx_empresas_tenant_id ON empresas (tenant_id);
CREATE INDEX idx_empresas_cnpj ON empresas (cnpj);

-- Para a empresa, o tenant_id é o próprio id (self-referencing tenant)
-- Isso será enforced pela aplicação no momento do cadastro.
