-- V4: Tabela de Veículos
-- Conforme 05-modelo-dominio.md e 06-modelo-fisico.md

CREATE TABLE veiculos (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       UUID NOT NULL,
    placa           VARCHAR(10) NOT NULL,
    chassi          VARCHAR(30) NOT NULL,
    renavam         VARCHAR(20),
    marca           VARCHAR(100) NOT NULL,
    modelo          VARCHAR(100) NOT NULL,
    ano_fabricacao  INTEGER NOT NULL,
    ano_modelo      INTEGER NOT NULL,
    cor             VARCHAR(50),
    quilometragem   INTEGER NOT NULL DEFAULT 0,
    status          VARCHAR(20) NOT NULL DEFAULT 'DISPONIVEL',
    valor_fipe      DECIMAL(19,4),
    valor_compra    DECIMAL(19,4),
    data_compra     DATE,
    documento_url   VARCHAR(500),
    
    -- Colunas base
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by      UUID,
    updated_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by      UUID,
    deleted_at      TIMESTAMP WITH TIME ZONE,
    deleted_by      UUID,
    version         BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_veiculos_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT uk_veiculos_placa_tenant UNIQUE (placa, tenant_id),
    CONSTRAINT uk_veiculos_chassi_tenant UNIQUE (chassi, tenant_id)
);

-- Índices obrigatórios
CREATE INDEX idx_veiculos_tenant_id ON veiculos (tenant_id);
CREATE INDEX idx_veiculos_status ON veiculos (status);
CREATE INDEX idx_veiculos_placa ON veiculos (placa);
