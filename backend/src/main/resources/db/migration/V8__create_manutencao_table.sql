-- V8: Tabela de Manutenção da Frota
-- Conforme Planejamento EPIC 6

CREATE TABLE manutencoes (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL,
    veiculo_id          UUID NOT NULL,
    tipo                VARCHAR(20) NOT NULL,
    descricao           VARCHAR(1000) NOT NULL,
    km_manutencao       INTEGER NOT NULL,
    data_inicio         DATE NOT NULL,
    data_fim            DATE,
    custo               DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
    concluida           BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_manutencao_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT fk_manutencao_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE RESTRICT
);

CREATE INDEX idx_manutencao_tenant_id ON manutencoes (tenant_id);
CREATE INDEX idx_manutencao_veiculo_id ON manutencoes (veiculo_id);
CREATE INDEX idx_manutencao_concluida ON manutencoes (concluida);
