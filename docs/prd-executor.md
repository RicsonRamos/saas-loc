# PRD Executor

## Objetivo

Traduzir o PRD e o backlog técnico em execução incremental, controlada e verificável.

O PRD Executor define COMO o produto deve ser construído a partir dos documentos em /docs.

---

# Fonte de Verdade

O sistema deve seguir:

- /docs/backlog-tecnico.md
- /docs/05-modelo-dominio.md
- /docs/06-modelo-fisico.md
- /docs/03-arquitetura.md

Qualquer divergência é erro crítico.

---

# Princípio Base

Não existe desenvolvimento livre.

Existe apenas execução de backlog.

---

# Fluxo de Execução

Cada ciclo de desenvolvimento deve seguir:

1. Ler EPIC atual
2. Validar dependências
3. Criar testes primeiro
4. Implementar domínio
5. Implementar service
6. Implementar repository
7. Implementar controller
8. Validar API
9. Rodar CI/CD
10. Atualizar documentação

---

# Definição de Conclusão

Um EPIC só está concluído quando:

- testes passando
- CI verde
- API documentada
- multi-tenant validado
- segurança validada
- sem dívida técnica crítica
- code review IA aprovado

---

# Priorização

1. Segurança
2. Multi-tenant
3. Integridade de dados
4. Regras de negócio
5. Performance
6. UX

---

# Proibições

- pular EPIC
- implementar fora da ordem
- criar features não previstas
- improvisar endpoints
- ignorar testes
- ignorar CI

---

# Mudanças de Escopo

Qualquer mudança de escopo deve:

- ser registrada como ADR
- ser validada contra impacto no backlog
- ser aprovada antes de implementação

---

# Validação Contínua

Após cada EPIC:

- revisar arquitetura
- revisar dívida técnica
- validar segurança
- atualizar documentação

---

# Regra Final

O PRD não é sugestão.

É um contrato de execução.