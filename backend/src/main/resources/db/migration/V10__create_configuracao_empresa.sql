-- V10: Tabela de Configurações da Empresa (Locadora Single-Tenant)
CREATE TABLE configuracao_empresa (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_fantasia           VARCHAR(200) NOT NULL,
    razao_social            VARCHAR(300) NOT NULL,
    cnpj                    VARCHAR(18) NOT NULL UNIQUE,
    inscricao_estadual      VARCHAR(30),
    endereco                VARCHAR(500),
    telefone                VARCHAR(20),
    email                   VARCHAR(200),
    logo_url                VARCHAR(500),
    horario_funcionamento   VARCHAR(200),
    politica_combustivel    TEXT,
    politica_quilometragem  TEXT,
    informacoes_fiscais     TEXT,
    
    -- Colunas base
    created_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by              UUID,
    updated_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by              UUID,
    deleted_at              TIMESTAMP WITH TIME ZONE,
    deleted_by              UUID,
    version                 BIGINT NOT NULL DEFAULT 0
);
