-- V13: Tabela de Log de Auditoria Detalhada (Single-Tenant)
CREATE TABLE auditoria (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    usuario         VARCHAR(200) NOT NULL,
    acao            VARCHAR(100) NOT NULL, -- ex: LOGIN, LOGOUT, CRIAR_CLIENTE, EDITAR_CONFIG
    entidade        VARCHAR(100),
    entidade_id     UUID,
    old_data        TEXT,                  -- JSON string
    new_data        TEXT,                  -- JSON string
    ip              VARCHAR(45) NOT NULL,
    user_agent      VARCHAR(500),
    correlation_id  VARCHAR(50),
    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_auditoria_usuario ON auditoria (usuario);
CREATE INDEX idx_auditoria_acao ON auditoria (acao);
CREATE INDEX idx_auditoria_entidade ON auditoria (entidade, entidade_id);
CREATE INDEX idx_auditoria_correlation ON auditoria (correlation_id);
