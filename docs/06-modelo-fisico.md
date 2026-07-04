# Modelo Físico

## Objetivo

Definir como o domínio será persistido no PostgreSQL.

---

# Banco Oficial

PostgreSQL

---

# Convenções

## Chaves Primárias

UUID

---

## Datas

TIMESTAMP WITH TIME ZONE

UTC

---

## Valores Monetários

DECIMAL(19,4)

---

## Booleanos

BOOLEAN

---

## Quilometragem

INTEGER

---

## Texto

VARCHAR

TEXT quando necessário.

---

# Convenção de Nomes

Tabelas:

snake_case

Colunas:

snake_case

Índices:

idx_

Foreign Keys:

fk_

Unique:

uk_

Check:

ck_

---

# Colunas Obrigatórias

Todas as tabelas possuirão:

id

tenant_id

created_at

created_by

updated_at

updated_by

deleted_at

deleted_by

version

---

# Soft Delete

Implementação obrigatória.

Nenhum DELETE físico será utilizado na aplicação.

---

# Controle de Concorrência

Optimistic Lock

Campo:

version

---

# Índices Obrigatórios

Toda FK deverá possuir índice.

tenant_id sempre indexado.

Campos frequentemente pesquisados deverão possuir índices.

---

# Constraints

Toda FK obrigatória.

Toda regra de unicidade implementada via UNIQUE.

Validações críticas implementadas via CHECK.

---

# Relacionamentos

empresa

↓

usuarios

clientes

veiculos

contratos

receitas

despesas

---

contratos

↓

pagamentos

---

veiculos

↓

manutencoes

documentos

despesas

---

clientes

↓

contratos

documentos

---

# Migrations

Flyway

Toda alteração estrutural deverá gerar migration.

É proibido alterar banco manualmente.

---

# Paginação

OFFSET

LIMIT

Implementação padrão Spring Data.

---

# Auditoria

Campos de auditoria obrigatórios.

Logs não substituem auditoria.

---

# Multi-Tenant

Toda tabela de negócio possui:

tenant_id

Toda consulta obrigatoriamente filtra tenant_id.

---

# Integridade

ON DELETE RESTRICT

Evitar CASCADE sempre que possível.

A regra de negócio deve controlar exclusões.

---

# Performance

Evitar SELECT *

Evitar consultas N+1

Utilizar paginação

Criar índices apenas quando justificados

---

# Backup

Responsabilidade da infraestrutura.

A modelagem deve permitir restauração consistente.

---

# Evolução

Novas tabelas devem seguir todas as convenções deste documento.

Alterações incompatíveis deverão ser evitadas.

Quando inevitáveis, deverão possuir estratégia de migração.

---

# Princípios

Persistência é um detalhe de implementação.

O modelo físico existe para suportar o domínio.

Toda otimização deve preservar a consistência dos dados.

A simplicidade tem prioridade sobre otimizações prematuras.