# Refactor Playbooks

## Objetivo

Padronizar refatorações recorrentes no sistema.

Toda refatoração deve seguir um playbook existente ou ser baseada em ADR.

---

# Playbook 01 — Controller Anemic Fix

## Problema

Controller com lógica de negócio.

## Passos

1. mover lógica para Service
2. manter Controller apenas como entrada/saída
3. criar testes para Service
4. validar endpoints

---

# Playbook 02 — Service God Class Split

## Problema

Service muito grande (>500 linhas)

## Passos

1. identificar responsabilidades
2. dividir por domínio
3. criar novos services menores
4. manter compatibilidade via facade se necessário
5. atualizar testes

---

# Playbook 03 — Repository Pollution Fix

## Problema

Repository com lógica de negócio

## Passos

1. remover regras do repository
2. mover para service/domain
3. manter apenas queries
4. adicionar testes de integração

---

# Playbook 04 — Multi-Tenant Leak Fix

## Problema

Query sem filtro tenant_id

## Passos

1. identificar endpoint afetado
2. adicionar filtro tenant_id
3. criar teste de isolamento
4. validar segurança

---

# Playbook 05 — DTO Explosion Fix

## Problema

Muitos DTOs duplicados

## Passos

1. consolidar DTOs por contexto
2. separar Request/Response corretamente
3. eliminar redundância
4. atualizar mappers

---

# Playbook 06 — Performance Bottleneck Fix

## Problema

Consulta lenta ou N+1

## Passos

1. identificar query problemática
2. adicionar fetch join ou índice
3. revisar paginação
4. validar impacto

---

# Playbook 07 — Circular Dependency Fix

## Problema

Dependência circular entre módulos

## Passos

1. identificar ciclo
2. introduzir interface ou abstraction layer
3. inverter dependência
4. garantir isolamento de módulos

---

# Playbook 08 — Security Leak Fix

## Problema

Exposição de dados sensíveis

## Passos

1. identificar endpoint/log
2. remover dados sensíveis
3. aplicar DTO seguro
4. adicionar teste de segurança

---

# Playbook 09 — Code Duplication Removal

## Problema

Código duplicado

## Passos

1. identificar duplicação
2. extrair método comum
3. ou criar service compartilhado
4. garantir testes

---

# Playbook 10 — Legacy Cleanup

## Problema

Código obsoleto

## Passos

1. verificar uso
2. remover gradualmente
3. garantir cobertura de testes
4. atualizar documentação

---

# Regra Final

Refatoração só pode ocorrer:

- com base em playbook
- ou via ADR aprovado

Refatoração sem controle é proibida.