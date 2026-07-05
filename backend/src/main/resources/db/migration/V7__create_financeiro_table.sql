-- V7: Tabela de Lançamentos Financeiros
-- Conforme Planejamento EPIC 5

CREATE TABLE lancamentos_financeiros (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id           UUID NOT NULL,
    tipo                VARCHAR(20) NOT NULL,
    valor               DECIMAL(19,4) NOT NULL,
    categoria           VARCHAR(50) NOT NULL,
    descricao           VARCHAR(500) NOT NULL,
    status              VARCHAR(20) NOT NULL DEFAULT 'PAGO',
    data_vencimento     DATE NOT NULL,
    data_pagamento      DATE,
    
    veiculo_id          UUID,
    contrato_id         UUID,
    
    -- Colunas base
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by          UUID,
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by          UUID,
    deleted_at          TIMESTAMP WITH TIME ZONE,
    deleted_by          UUID,
    version             BIGINT NOT NULL DEFAULT 0,

    CONSTRAINT fk_financeiro_empresa FOREIGN KEY (tenant_id) REFERENCES empresas(id) ON DELETE RESTRICT,
    CONSTRAINT fk_financeiro_veiculo FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE SET NULL,
    CONSTRAINT fk_financeiro_contrato FOREIGN KEY (contrato_id) REFERENCES contratos(id) ON DELETE SET NULL
);

-- Índices para relatórios e dashboards (otimização de filtros temporais e isolamento multi-tenant)
CREATE INDEX idx_financeiro_tenant_id ON lancamentos_financeiros (tenant_id);
CREATE INDEX idx_financeiro_data_venc ON lancamentos_financeiros (data_vencimento);
CREATE INDEX idx_financeiro_data_pag ON lancamentos_financeiros (data_pagamento);
CREATE INDEX idx_financeiro_tipo ON lancamentos_financeiros (tipo);
