-- V14: Tabela de Registro de Uploads de Arquivos
CREATE TABLE uploads (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    uuid_arquivo        UUID NOT NULL UNIQUE,
    hash_sha256         VARCHAR(64) NOT NULL,
    mime_type           VARCHAR(100) NOT NULL,
    nome_original       VARCHAR(255) NOT NULL,
    tamanho             BIGINT NOT NULL,
    altura              INTEGER,
    largura             INTEGER,
    usuario_id          UUID,
    relacionamento_tipo VARCHAR(50) NOT NULL, -- CLIENTES, VEICULOS, CONTRATOS, FINANCEIRO, MANUTENCAO
    relacionamento_id   UUID NOT NULL,        -- ID da entidade vinculada
    caminho_arquivo     VARCHAR(500) NOT NULL,
    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    CONSTRAINT fk_uploads_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE INDEX idx_uploads_relacionamento ON uploads (relacionamento_tipo, relacionamento_id);
CREATE INDEX idx_uploads_uuid ON uploads (uuid_arquivo);
