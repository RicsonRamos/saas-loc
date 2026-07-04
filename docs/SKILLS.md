# Skills do Agente

## Objetivo

Definir capacidades especializadas que o agente deve aplicar durante a geração de código, análise e manutenção do sistema.

As skills não são opcionais quando o contexto se aplica.

---

# SKILL 01 — Multi-Tenant Enforcement

## Quando aplicar

Sempre que houver acesso a dados de qualquer entidade.

## Regras

- Toda query deve filtrar tenant_id
- Nunca confiar em tenant vindo do cliente
- Validar tenant via usuário autenticado
- Proibir cross-tenant access em qualquer camada

## Validação obrigatória

- testes de isolamento por tenant
- verificação no service layer

---

# SKILL 02 — Domain-First Thinking

## Quando aplicar

Sempre ao criar ou alterar regras de negócio.

## Regras

- regra de negócio nunca fica no controller
- repository nunca contém regra
- domínio não depende de framework
- entidades são puras

## Output esperado

- lógica clara no service/domain
- ausência de acoplamento com infraestrutura

---

# SKILL 03 — API Consistency Enforcement

## Quando aplicar

Sempre que criar endpoints.

## Regras

- seguir /docs/10-api-conventions.md
- nunca criar endpoint fora do padrão REST
- sempre usar DTOs
- paginação obrigatória em listas
- respostas padronizadas

---

# SKILL 04 — Security Hardening

## Quando aplicar

Sempre em qualquer feature nova.

## Regras

- nunca expor stacktrace
- nunca logar dados sensíveis
- nunca hardcode de secrets
- validar input no backend
- bloquear acesso não autorizado
- aplicar RBAC sempre

---

# SKILL 05 — Test-First Execution

## Quando aplicar

Antes de implementar qualquer funcionalidade.

## Regras

- escrever testes antes do código
- cobrir service layer obrigatoriamente
- usar Testcontainers quando envolver banco
- testes devem validar regras de negócio

## Falha crítica se

- feature sem teste existir
- teste não validar regra de negócio

---

# SKILL 06 — Clean Architecture Guard

## Quando aplicar

Sempre que estruturar código.

## Regras

- controllers não têm lógica
- services não acessam HTTP
- repository não tem regra de negócio
- domínio não conhece infraestrutura
- dependências sempre apontam para dentro

---

# SKILL 07 — Debt Detection

## Quando aplicar

Durante qualquer análise de código ou PR.

## Detectar

- classes grandes
- métodos longos
- duplicação
- dependências circulares
- acoplamento excessivo
- ausência de testes
- violação de arquitetura

## Saída

- lista de problemas
- severidade
- recomendação de refatoração

---

# SKILL 08 — ADR-Driven Refactoring

## Quando aplicar

Quando houver mudança estrutural.

## Regras

- toda mudança arquitetural exige ADR
- refatoração sem ADR é proibida
- mudanças devem ser justificadas
- impacto deve ser analisado antes da execução

---

# SKILL 09 — CI/CD Enforcement

## Quando aplicar

Durante qualquer entrega ou pipeline.

## Regras

- build obrigatório
- testes obrigatórios
- lint obrigatório
- segurança obrigatória
- falha no pipeline bloqueia deploy

---

# SKILL 10 — Code Review Intelligence

## Quando aplicar

Em toda Pull Request.

## Avaliar

- arquitetura
- segurança
- multi-tenant
- qualidade de código
- testes
- duplicação
- complexidade
- dependências

## Output

- APPROVE ou REJECT
- lista de problemas
- severidade
- sugestão de correção

---

# SKILL 11 — Simplicity Bias

## Quando aplicar

Sempre que houver múltiplas soluções possíveis.

## Regras

- escolher solução mais simples
- evitar overengineering
- evitar micro abstrações desnecessárias
- evitar prematuridade arquitetural

---

# SKILL 12 — Data Safety Guard

## Quando aplicar

Sempre que lidar com dados sensíveis.

## Regras

- nunca expor dados pessoais
- nunca logar documentos
- nunca armazenar secrets em texto puro
- nunca enviar dados sensíveis para frontend sem necessidade

---

# PRINCÍPIO FINAL

Skills não são sugestões.

São regras de execução obrigatória sempre que o contexto se aplicar.