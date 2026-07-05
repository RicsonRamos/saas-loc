-- V19: Seed de Configuração e Administrador Padrão
-- Adiciona a coluna must_change_password na tabela de usuários
ALTER TABLE usuarios ADD COLUMN must_change_password BOOLEAN NOT NULL DEFAULT FALSE;

-- Insere as configurações padrão da locadora
INSERT INTO configuracao_empresa (
    id, nome_fantasia, razao_social, cnpj, inscricao_estadual, endereco, telefone, email, logo_url, horario_funcionamento, politica_combustivel, politica_quilometragem, informacoes_fiscais
) VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'Locadora Local ERP',
    'Locadora de Veiculos Local LTDA',
    '12.345.678/0001-90',
    'ISENTO',
    'Av. Principal, 1000 - Centro',
    '(11) 99999-9999',
    'contato@locadoralocal.com',
    'https://locadoralocal.com/logo.png',
    'Segunda a Sexta das 08:00 às 18:00',
    'O veículo deve ser devolvido com o mesmo nível de combustível da retirada.',
    'Quilometragem livre para contratos mensais, 200km/dia para contratos diários.',
    'Regime tributário: Simples Nacional'
);

-- Insere o Administrador Padrão (E-mail: admin@locadora.com, Senha inicial: admin123, deve mudar no 1º acesso)
-- A senha 'admin123' encriptada com BCrypt: $2a$10$ExM2fSj.Z491eW3zBf1cxe.eG2tN1vK62wH7Qe9d4H1u9zZc3C2
INSERT INTO usuarios (
    id, nome, email, senha, ativo, must_change_password
) VALUES (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'Administrador',
    'admin@locadora.com',
    '$2a$10$ExM2fSj.Z491eW3zBf1cxe.eG2tN1vK62wH7Qe9d4H1u9zZc3C2',
    TRUE,
    TRUE
);

-- Vincula a role ADMIN ao administrador padrão
INSERT INTO usuario_roles (usuario_id, role) VALUES (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12',
    'ADMIN'
);
