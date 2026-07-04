# Architecture Decision Record (ADR)

## Objetivo

Registrar decisões arquiteturais importantes do sistema.

Toda decisão relevante que impacte estrutura, tecnologia ou comportamento do sistema deve gerar um ADR.

---

# Estrutura do ADR

Cada ADR deve seguir este padrão:

---

## Título

Ex: ADR-001 - Escolha do Banco de Dados

---

## Status

- Proposto
- Aceito
- Rejeitado
- Substituído

---

## Contexto

Descrever o problema que precisa ser resolvido.

---

## Decisão

Descrever claramente a decisão tomada.

---

## Alternativas Consideradas

Listar opções avaliadas.

Ex:

- PostgreSQL
- MySQL
- MongoDB

---

## Consequências

### Positivas

- benefícios da decisão

### Negativas

- custos ou limitações

---

## Impacto

Descrever impacto em:

- arquitetura
- código
- performance
- manutenção
- custos

---

## Relação com Outros ADRs

Referenciar decisões relacionadas.

---

## Data

Data da decisão.

---

## Responsáveis

Quem tomou a decisão.

---

# Regras

- Toda decisão relevante deve gerar ADR
- Não alterar arquitetura sem ADR
- Não alterar stack sem ADR
- Não alterar segurança sem ADR

---

# Exemplos de decisões que exigem ADR

- troca de banco de dados
- introdução de microsserviços
- mudança de autenticação
- introdução de mensageria
- mudança de arquitetura
- adoção de novo framework crítico

---

# Princípio Final

Nenhuma decisão arquitetural deve existir apenas no código.

Toda decisão importante deve ser registrada, rastreável e justificável.