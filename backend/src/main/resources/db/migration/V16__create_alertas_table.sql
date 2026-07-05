-- V16: Tabela de Central de Alertas e Notificações (Single-Tenant)
CREATE TABLE alertas (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo                VARCHAR(50) NOT NULL, -- CNH, IPVA, SEGURO, LICENCIAMENTO, REVISAO, OLEO, RESERVA, CONTRATO
    titulo              VARCHAR(255) NOT NULL,
    descricao           VARCHAR(500) NOT NULL,
    entidade_id         UUID NOT NULL,        -- ID do Veículo, Cliente, Contrato, etc.
    lido                BOOLEAN NOT NULL DEFAULT FALSE,
    data_alerta         DATE NOT NULL DEFAULT CURRENT_DATE,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0
);

CREATE INDEX idx_alertas_lido ON alertas (lido);
CREATE INDEX idx_alertas_data ON alertas (data_alerta);
