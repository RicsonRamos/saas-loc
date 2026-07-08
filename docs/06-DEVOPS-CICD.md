# 06 · DevOps, CI/CD e Infraestrutura

## Prompt de Alto Nível
Monte uma esteira simples e confiável para um time pequeno: lint, testes, build e deploy direto. Não adicione canary, blue/green, SBOM ou múltiplos ambientes de homologação — é custo sem retorno neste estágio do projeto.

## Ambientes
| Ambiente | Uso |
|---|---|
| Local | Docker Compose com Postgres local |
| Produção | Ambiente único, com backup automático do banco |

Um ambiente de staging simples (mesma infra, banco separado) é opcional — adicione apenas se o time sentir necessidade real antes de liberar uma mudança arriscada.

## Pipeline CI (GitHub Actions)
```text
lint -> testes -> build
```

Gates mínimos: `ruff`/`eslint`, `pytest`, `tsc --noEmit`. Scan de segredos (`gitleaks`) é barato e vale a pena manter desde o início.

## Deploy
Deploy direto após merge em `main` (Railway, Render, Fly.io ou VPS com Docker Compose). Sem canary — se algo quebrar, o rollback é reverter para o deploy anterior.

## Migrações
Rodar `alembic upgrade head` como passo explícito do deploy, antes de subir a nova versão da aplicação.

## Backup
Backup diário automático do PostgreSQL (a maioria dos provedores gerenciados já oferece isso pronto). Teste um restore pelo menos uma vez antes de operar com dados reais do cliente.

## Critérios de Aceite
Uma mudança operacional está pronta quando:

- passa no pipeline de lint + testes;
- não introduz segredo hardcoded (verificado por `gitleaks`);
- roda a migração antes do deploy da aplicação;
- tem backup ativo, com restore validado ao menos uma vez.
