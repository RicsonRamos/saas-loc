# Risk Engine

## Objetivo

Avaliar o risco de qualquer mudança antes da implementação ou merge.

O Risk Engine é obrigatório para todas as decisões críticas.

---

# Classificação de Risco

## LOW

- ajustes de UI
- refatoração interna sem impacto externo
- melhorias de performance locais

---

## MEDIUM

- novos endpoints
- mudanças em services
- ajustes em regras de negócio

---

## HIGH

- mudanças em autenticação
- mudanças em multi-tenant
- alterações em contratos ou financeiro
- mudanças em schema de banco

---

## CRITICAL

- alterações arquiteturais
- mudanças no modelo de dados
- alterações em segurança
- remoção de constraints de tenant
- mudanças em CI/CD

---

# Avaliação Obrigatória

Toda mudança deve ser avaliada por:

- impacto em dados
- impacto em segurança
- impacto em multi-tenant
- impacto em performance
- impacto em testes
- impacto em deploy

---

# Regras por Nível de Risco

## LOW

- revisão normal
- testes básicos suficientes

---

## MEDIUM

- testes obrigatórios
- code review IA obrigatório
- validação de API

---

## HIGH

- aprovação obrigatória da IA reviewer
- testes de integração obrigatórios
- validação de segurança
- validação de multi-tenant

---

## CRITICAL

- exige ADR obrigatório
- exige revisão completa de arquitetura
- exige validação manual e automática
- exige rollback plan

---

# Bloqueios Automáticos

O sistema deve bloquear automaticamente:

- risco CRITICAL sem ADR
- risco HIGH sem testes
- qualquer mudança que viole multi-tenant
- qualquer mudança de segurança sem validação

---

# Output do Risk Engine

Para cada mudança:

- nível de risco
- justificativa
- áreas afetadas
- recomendações
- bloqueios (se houver)

---

# Integração com CI/CD

Risk Engine deve rodar em:

- Pull Requests
- pipeline CI
- pré-deploy

---

# Integração com Code Review IA

Risk Engine alimenta o code review com:

- severidade
- contexto
- áreas sensíveis

---

# Regra Final

Nenhuma mudança crítica pode ser implementada sem avaliação de risco explícita.

Ignorar o Risk Engine é falha de segurança.