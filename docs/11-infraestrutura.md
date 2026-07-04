# Infraestrutura

## Objetivo

Definir como o sistema será executado, implantado, escalado e mantido em ambientes de desenvolvimento, homologação e produção.

---

# Ambientes

## Desenvolvimento

- Local ou containerizado
- Banco local ou Supabase
- Execução via Docker Compose
- Hot reload permitido

---

## Homologação

- Ambiente semelhante à produção
- Usado para validação de novas versões
- Dados simulados ou anonimizados

---

## Produção

- Ambiente estável
- Alta disponibilidade
- Backups obrigatórios
- Monitoramento ativo

---

# Arquitetura de Deploy

Inicial (MVP):

- VPS única
- Docker Compose
- NGINX como reverse proxy
- PostgreSQL externo ou gerenciado
- Redis opcional

---

Evolução:

- Separação de serviços
- Load balancer
- Múltiplas instâncias da API
- Banco gerenciado
- CDN para arquivos

---

# Containers

Todos os serviços deverão rodar em Docker.

Serviços:

- backend (Spring Boot)
- frontend (React build)
- database (PostgreSQL)
- cache (Redis)
- reverse proxy (NGINX)

---

# Orquestração

Inicialmente:

Docker Compose

Futuro:

Kubernetes (se necessário)

---

# Banco de Dados

Opções:

- Supabase PostgreSQL (MVP)
- PostgreSQL gerenciado (produção)
- PostgreSQL em VPS (fallback)

---

# Storage de Arquivos

Inicialmente:

Supabase Storage

Alternativa futura:

S3 compatível

---

# CI/CD

Utilizar GitHub Actions:

Pipeline:

- build
- testes
- análise estática
- build docker image
- deploy

---

# Deploy

Estratégia:

- Deploy automatizado via pipeline
- Rollback manual ou automatizado
- Versionamento por tag

---

# Configuração

Todas as configurações devem vir de variáveis de ambiente:

- banco
- autenticação
- storage
- API keys

Nunca hardcoded.

---

# Segurança

- HTTPS obrigatório
- Firewall ativo
- Portas expostas mínimas
- SSH restrito
- Secrets fora do código

---

# Backup

- Backup diário do banco
- Backup de arquivos
- Retenção configurável
- Testes de restore periódicos

---

# Escalabilidade

A infraestrutura deve suportar:

- múltiplas instâncias da API
- aumento de tráfego
- crescimento do banco
- aumento de armazenamento

---

# Monitoramento

- logs centralizados
- métricas básicas
- alertas de falha

---

# Custos

Infraestrutura deve ser otimizada para baixo custo inicial.

Evoluir conforme crescimento da base de clientes.

---

# Princípio Final

Infraestrutura deve ser simples no início e evoluir sob demanda.