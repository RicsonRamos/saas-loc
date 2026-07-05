-- V6: Tabela de Contratos
-- Conforme 05-modelo-dominio.md e 06-modelo-fisico.md

CREATE TABLE contratos (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL,
    cliente_id          UUID NOT NULL,
    veiculo_id          UUID NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'RASCUNHO',
    data_inicio         TIMESTAMP WITH TIME ZONE NOT NULL,
    data_fim_prevista   TIMESTAMP WITH TIME ZONE NOT NULL,
    data_devolucao      TIMESTAMP WITH TIME ZONE,
    valor_total         DECIMAL(19,4) NOT NULL,
    caucao              DECIMAL(19,4),
    valor_adicional     DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
    km_inicial          INTEGER NOT NULL,
    km_final            INTEGER,
    km_excedente        INTEGER NOT NULL DEFAULT 0,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_contratos_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT fk_contratos_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    CONSTRAINT fk_contratos_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE RESTRICT
);

-- Índices obrigatórios para performance e consultas multi-tenant
CREATE INDEX idx_contratos_tenant_id ON contratos (tenant_id);
CREATE INDEX idx_contratos_cliente_id ON contratos (cliente_id);
CREATE INDEX idx_contratos_veiculo_id ON contratos (veiculo_id);
CREATE INDEX idx_contratos_status ON contratos (status);
