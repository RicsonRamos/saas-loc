-- V15: Tabela de Controle de Documentos de Veículos (Single-Tenant)
CREATE TABLE documentos_veiculos (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    veiculo_id          UUID NOT NULL,
    tipo                VARCHAR(50) NOT NULL, -- SEGURO, IPVA, LICENCIAMENTO, CRLV, GARANTIA, INSPECAO, VISTORIA
    numero              VARCHAR(100),
    data_emissao        DATE,
    validade            DATE NOT NULL,
    upload_id           UUID,
    observacoes         TEXT,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_documentos_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE,
    CONSTRAINT fk_documentos_upload FOREIGN KEY (upload_id) REFERENCES uploads(id) ON DELETE SET NULL
);

CREATE INDEX idx_documentos_veiculo ON documentos_veiculos (veiculo_id);
CREATE INDEX idx_documentos_validade ON documentos_veiculos (validade);
