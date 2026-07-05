-- V12: Tabela de Controle de Reservas (Single-Tenant)
CREATE TABLE reservas (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id          UUID NOT NULL,
    veiculo_id          UUID,
    categoria           VARCHAR(50) NOT NULL,
    status              VARCHAR(30) NOT NULL DEFAULT 'RESERVADO',
    data_inicio         TIMESTAMP WITH TIME ZONE NOT NULL,
    data_fim            TIMESTAMP WITH TIME ZONE NOT NULL,
    origem              VARCHAR(30) NOT NULL, -- TELEFONE, WHATSAPP, SITE, INSTAGRAM, INDICACAO
    observacoes         TEXT,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_reservas_cliente FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT,
    CONSTRAINT fk_reservas_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE SET NULL
);

-- Índices de busca e detecção de conflitos de data
CREATE INDEX idx_reservas_cliente ON reservas (cliente_id);
CREATE INDEX idx_reservas_veiculo ON reservas (veiculo_id);
CREATE INDEX idx_reservas_periodo ON reservas (data_inicio, data_fim);
CREATE INDEX idx_reservas_status ON reservas (status);
