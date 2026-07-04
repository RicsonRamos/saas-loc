-- V3: Tabela de Roles dos Usuários
-- RBAC conforme RF-010 e 07-segurança.md.

CREATE TABLE usuario_roles (
    usuario_id  UUID NOT NULL,
    role        VARCHAR(50) NOT NULL,

    CONSTRAINT fk_usuario_roles_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE RESTRICT,
    CONSTRAINT uk_usuario_role UNIQUE (usuario_id, role)
);

CREATE INDEX idx_usuario_roles_usuario_id ON usuario_roles (usuario_id);
