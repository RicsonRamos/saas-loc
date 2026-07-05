-- V18: Enriquecimento de campos em Clientes, Veículos, Contratos e Financeiro (Single-Tenant)

-- 1. Clientes
ALTER TABLE clientes ADD COLUMN cnh_categoria VARCHAR(5);
ALTER TABLE clientes ADD COLUMN bloqueado BOOLEAN NOT NULL DEFAULT FALSE;
ALTER TABLE clientes ADD COLUMN observacoes TEXT;

-- 2. Veículos
ALTER TABLE veiculos ADD COLUMN combustivel VARCHAR(20);
ALTER TABLE veiculos ADD COLUMN cambio VARCHAR(20);
ALTER TABLE veiculos ADD COLUMN capacidade_tanque INTEGER;
ALTER TABLE veiculos ADD COLUMN proxima_revisao DATE;
ALTER TABLE veiculos ADD COLUMN proxima_troca_oleo DATE;
ALTER TABLE veiculos ADD COLUMN seguro VARCHAR(100);
ALTER TABLE veiculos ADD COLUMN ipva VARCHAR(100);
ALTER TABLE veiculos ADD COLUMN crlv VARCHAR(100);
ALTER TABLE veiculos ADD COLUMN licenciamento VARCHAR(100);
ALTER TABLE veiculos ADD COLUMN categoria VARCHAR(50);

-- 3. Contratos
ALTER TABLE contratos ADD COLUMN checklist_retirada_id UUID;
ALTER TABLE contratos ADD COLUMN checklist_devolucao_id UUID;
ALTER TABLE contratos ADD COLUMN multas DECIMAL(19,4) NOT NULL DEFAULT 0;
ALTER TABLE contratos ADD COLUMN combustivel VARCHAR(20);
ALTER TABLE contratos ADD COLUMN acessorios TEXT;
ALTER TABLE contratos ADD COLUMN observacoes TEXT;
ALTER TABLE contratos ADD COLUMN assinatura_url VARCHAR(500);

-- 4. Lançamentos Financeiros
ALTER TABLE lancamentos_financeiros ADD COLUMN centro_custo VARCHAR(100);
ALTER TABLE lancamentos_financeiros ADD COLUMN forma_pagamento VARCHAR(50);
ALTER TABLE lancamentos_financeiros ADD COLUMN parcelas INTEGER DEFAULT 1;
ALTER TABLE lancamentos_financeiros ADD COLUMN comprovante_url VARCHAR(500);
