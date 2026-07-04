# Agent Router

## Objetivo

Definir como o agente deve selecionar e aplicar Skills automaticamente com base no contexto.

O roteamento é obrigatório e determinístico.

---

# Regra Base

Para qualquer tarefa:

1. Analisar contexto
2. Identificar categoria da mudança
3. Aplicar Skills correspondentes
4. Executar regras combinadas sem conflito
5. Priorizar segurança > arquitetura > funcionalidade

---

# Mapeamento de Contexto → Skills

## API / Endpoints

Aplicar:
- API Consistency Enforcement
- Security Hardening
- Data Safety Guard
- Code Review Intelligence

---

## Regras de Negócio

Aplicar:
- Domain-First Thinking
- Test-First Execution
- Clean Architecture Guard
- ADR-Driven Refactoring (se estrutural)

---

## Banco de Dados / Persistência

Aplicar:
- Multi-Tenant Enforcement
- Clean Architecture Guard
- Data Safety Guard
- Debt Detection

---

## Autenticação / Segurança

Aplicar:
- Security Hardening
- Data Safety Guard
- Multi-Tenant Enforcement
- Code Review Intelligence

---

## Criação de novas features

Aplicar SEMPRE:

- Test-First Execution
- Domain-First Thinking
- API Consistency Enforcement
- Security Hardening
- Clean Architecture Guard
- Simplicity Bias

---

## Refatoração

Aplicar:

- ADR-Driven Refactoring
- Debt Detection
- Clean Architecture Guard
- Simplicity Bias

---

## Pull Requests

Aplicar:

- Code Review Intelligence
- Debt Detection
- Security Hardening
- API Consistency Enforcement

---

## CI/CD / Deploy

Aplicar:

- CI/CD Enforcement
- Security Hardening
- Data Safety Guard

---

# Conflito de Skills

Quando houver conflito:

1. Segurança prevalece
2. Integridade de dados prevalece
3. Arquitetura prevalece
4. Funcionalidade prevalece

---

# Regra Final

Nenhuma skill pode ser ignorada quando aplicável.