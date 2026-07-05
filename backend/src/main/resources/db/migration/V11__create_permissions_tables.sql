-- V11: Tabelas de Permissões Granulares
CREATE TABLE permissions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome        VARCHAR(100) NOT NULL UNIQUE,
    descricao   VARCHAR(300) NOT NULL
);

CREATE TABLE role_permissions (
    role           VARCHAR(50) NOT NULL,
    permission_id  UUID NOT NULL,
    
    CONSTRAINT fk_role_permissions_perm FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role, permission_id)
);

CREATE TABLE user_permissions (
    usuario_id     UUID NOT NULL,
    permission_id  UUID NOT NULL,
    
    CONSTRAINT fk_user_permissions_user FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_permissions_perm FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id, permission_id)
);

-- Seed de Permissões
INSERT INTO permissions (nome, descricao) VALUES
('CONTRATO_EXCLUIR', 'Permite excluir um contrato do sistema'),
('CONTRATO_CANCELAR', 'Permite cancelar um contrato ativo ou reservado'),
('FINANCEIRO_EDITAR', 'Permite alterar lançamentos financeiros e fluxo de caixa'),
('FINANCEIRO_EXCLUIR', 'Permite excluir lançamentos financeiros permanentes'),
('VALORES_EDITAR', 'Permite editar tarifas, valores de diárias e acréscimos'),
('VEICULO_CADASTRAR', 'Permite cadastrar ou atualizar veículos na frota'),
('VEICULO_EXCLUIR', 'Permite remover veículos do catálogo operacional'),
('USUARIO_CADASTRAR', 'Permite gerenciar operadores, gerentes e funcionários'),
('DOCUMENTO_GERENCIAR', 'Permite carregar e validar documentos de CRLV, IPVA, etc'),
('CONFIGURACAO_GERENCIAR', 'Permite alterar dados de contato, fiscais e logo da locadora');

-- Vinculação Padrão por Roles (Admins possuem tudo, Gerente possui quase tudo)
-- 1. ADMIN
INSERT INTO role_permissions (role, permission_id)
SELECT 'ADMIN', id FROM permissions;

-- 2. GERENTE (não pode excluir lançamentos financeiros ou contratos por padrão, apenas gerenciar frota/clientes/valores)
INSERT INTO role_permissions (role, permission_id)
SELECT 'GERENTE', id FROM permissions 
WHERE nome NOT IN ('FINANCEIRO_EXCLUIR', 'CONTRATO_EXCLUIR');

-- 3. FINANCEIRO
INSERT INTO role_permissions (role, permission_id)
SELECT 'FINANCEIRO', id FROM permissions 
WHERE nome IN ('FINANCEIRO_EDITAR', 'VALORES_EDITAR');

-- 4. OPERADOR
INSERT INTO role_permissions (role, permission_id)
SELECT 'OPERADOR', id FROM permissions 
WHERE nome IN ('VEICULO_CADASTRAR', 'DOCUMENTO_GERENCIAR', 'CONTRATO_CANCELAR');
