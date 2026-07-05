-- V9: Migração para Single-Tenant
-- Remove toda a infraestrutura multi-tenant (tenant_id, FKs, índices, tabela empresas).
-- O sistema passa a operar como uma única locadora.

-- 1. Remover Foreign Keys de tenant_id
ALTER TABLE usuarios DROP CONSTRAINT IF EXISTS fk_usuarios_empresa;
ALTER TABLE veiculos DROP CONSTRAINT IF EXISTS fk_veiculos_empresa;
ALTER TABLE clientes DROP CONSTRAINT IF EXISTS fk_clientes_empresa;
ALTER TABLE contratos DROP CONSTRAINT IF EXISTS fk_contratos_empresa;
ALTER TABLE lancamentos_financeiros DROP CONSTRAINT IF EXISTS fk_financeiro_empresa;
ALTER TABLE manutencoes DROP CONSTRAINT IF EXISTS fk_manutencao_empresa;

-- 2. Remover Unique Constraints compostas com tenant_id
ALTER TABLE veiculos DROP CONSTRAINT IF EXISTS uk_veiculos_placa_tenant;
ALTER TABLE veiculos DROP CONSTRAINT IF EXISTS uk_veiculos_chassi_tenant;
ALTER TABLE clientes DROP CONSTRAINT IF EXISTS uk_clientes_documento_tenant;

-- 3. Recriar Unique Constraints sem tenant_id
ALTER TABLE veiculos ADD CONSTRAINT uk_veiculos_placa UNIQUE (placa);
ALTER TABLE veiculos ADD CONSTRAINT uk_veiculos_chassi UNIQUE (chassi);
ALTER TABLE clientes ADD CONSTRAINT uk_clientes_documento UNIQUE (documento);

-- 4. Remover índices de tenant_id
DROP INDEX IF EXISTS idx_empresas_tenant_id;
DROP INDEX IF EXISTS idx_usuarios_tenant_id;
DROP INDEX IF EXISTS idx_veiculos_tenant_id;
DROP INDEX IF EXISTS idx_clientes_tenant_id;
DROP INDEX IF EXISTS idx_contratos_tenant_id;
DROP INDEX IF EXISTS idx_financeiro_tenant_id;
DROP INDEX IF EXISTS idx_manutencao_tenant_id;

-- 5. Remover coluna tenant_id de todas as tabelas
ALTER TABLE usuarios DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE veiculos DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE clientes DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE contratos DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE lancamentos_financeiros DROP COLUMN IF EXISTS tenant_id;
ALTER TABLE manutencoes DROP COLUMN IF EXISTS tenant_id;

-- 6. Dropar tabela empresas (o tenant root deixa de existir)
DROP TABLE IF EXISTS empresas CASCADE;

-- 7. Remover índice de CNPJ da tabela empresas (já dropada pelo CASCADE)
-- DROP INDEX IF EXISTS idx_empresas_cnpj; -- já removido pelo CASCADE
