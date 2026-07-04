# Failure Recovery

## Objetivo

Definir como o sistema e o agente devem reagir a falhas durante:

- CI/CD
- execução de testes
- deploy
- runtime
- validação de código

---

# Tipos de Falha

## Falha de Testes

### Ação obrigatória

- identificar teste quebrado
- identificar causa raiz
- não alterar teste para “passar”
- corrigir código, não o teste

---

## Falha de Build

### Ação obrigatória

- verificar dependências
- verificar compilação
- verificar versões
- corrigir incompatibilidades

Nunca ignorar erro de build.

---

## Falha de Lint / Qualidade

### Ação obrigatória

- corrigir estilo
- remover código morto
- reduzir complexidade
- ajustar padrões

---

## Falha de Segurança

### Ação imediata (BLOCKER)

- interromper pipeline
- não permitir deploy
- remover exposição de dados sensíveis
- corrigir vulnerabilidade antes de continuar

---

## Falha de Multi-Tenant

### Ação crítica

- bloquear merge/deploy
- identificar fuga de tenant_id
- corrigir query ou service
- adicionar teste de isolamento

---

## Falha de Deploy

### Ação obrigatória

- rollback automático ou manual
- identificar diferença entre ambientes
- validar variáveis de ambiente
- verificar Docker build

---

## Falha de Testes Flaky

### Ação obrigatória

- isolar instabilidade
- tornar teste determinístico
- nunca remover teste instável sem análise

---

# Estratégia de Correção

Ordem obrigatória:

1. Identificar causa raiz
2. Criar hipótese
3. Corrigir código
4. Rodar testes
5. Validar CI
6. Documentar se recorrente

---

# Proibições

- nunca ignorar erro
- nunca desativar teste para passar pipeline
- nunca desativar regra de segurança
- nunca fazer bypass de CI

---

# Regra Final

Falha não é exceção.

Falha é parte do processo de controle de qualidade.