-- V17: Tabela de Checklists Dinâmicos (Single-Tenant)
CREATE TABLE checklists (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contrato_id             UUID NOT NULL,
    tipo                    VARCHAR(20) NOT NULL, -- RETIRADA, DEVOLUCAO
    itens_json              TEXT NOT NULL,        -- Estrutura JSON com itens dinâmicos ([{"item": "Estepe", "estado": "OK"}, ...])
    fotos_json              TEXT,                 -- Estrutura JSON com lista de URLs ou UUIDs de fotos
    assinatura_cliente_url  VARCHAR(500),
    assinatura_operador_url VARCHAR(500),
    
    -- Colunas base
    created_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by              UUID,
    updated_at              TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by              UUID,
    deleted_at              TIMESTAMP WITH TIME ZONE,
    deleted_by              UUID,
    version                 BIGINT NOT NULL DEFAULT 0,
    
    CONSTRAINT fk_checklists_contrato FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON DELETE CASCADE
);

CREATE INDEX idx_checklists_contrato ON checklists (contrato_id);
