# 🚗 Locadora SaaS

**Sistema SaaS multi-tenant para gestão de locadoras de veículos.**

Plataforma web completa que permite que múltiplas locadoras utilizem uma única aplicação de forma segura, isolada e escalável, com assinatura mensal.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Stack Tecnológica](#-stack-tecnológica)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API](#-api)
- [Multi-Tenant](#-multi-tenant)
- [Segurança](#-segurança)
- [Testes](#-testes)
- [Deploy em Produção](#-deploy-em-produção)
- [Roadmap](#-roadmap)
- [Documentação Técnica](#-documentação-técnica)
- [Licença](#-licença)

---

## 🎯 Visão Geral

Grande parte das pequenas e médias locadoras ainda utiliza planilhas, sistemas desktop antigos ou controle manual. Isso gera falta de controle financeiro, perda de informações e baixa visibilidade da lucratividade.

O **Locadora SaaS** resolve esses problemas com uma plataforma web centralizada que controla toda a operação:

| Problema | Solução |
|----------|---------|
| Planilhas e processos manuais | Sistema web unificado |
| Falta de controle financeiro | Módulo financeiro com fluxo de caixa |
| Dados descentralizados | Banco centralizado por empresa |
| Sem indicadores de desempenho | Dashboard com KPIs avançados |
| Sem escalabilidade | Arquitetura multi-tenant SaaS |

### Diferenciais

- **Lucro por veículo** — saiba exatamente quanto cada carro rende
- **Custo por quilômetro** — controle granular de despesas
- **Payback do investimento** — tempo estimado de retorno por veículo
- **Comparação FIPE vs valor pago** — decisões de compra/venda embasadas
- **Taxa de ocupação** — otimize sua frota

---

## ✨ Funcionalidades

### MVP (Versão Atual)

| Módulo | Descrição |
|--------|-----------|
| **Empresas** | Cadastro de locadoras (tenants) com CNPJ, dados e logotipo |
| **Usuários** | Cadastro, login, recuperação de senha, RBAC (Admin, Gerente, Financeiro, Operador) |
| **Clientes** | Pessoa física/jurídica, documentos, condutores adicionais, histórico |
| **Veículos** | Frota completa, status (disponível/alugado/manutenção), documentação, quilometragem |
| **Contratos** | Locação com período, valores, caução, km inicial/final, devolução, danos |
| **Financeiro** | Receitas, despesas, categorias, contas a pagar/receber, fluxo de caixa |
| **Manutenção** | Preventiva/corretiva, oficinas, peças, custos, alertas |
| **Dashboard** | Indicadores financeiros, veículos mais rentáveis, taxa de ocupação |
| **Relatórios** | PDF, Excel, filtros por período/veículo/cliente |
| **Auditoria** | Registro de todas as alterações com usuário, data, ação e IP |

### Fora do Escopo Inicial

Aplicativo mobile nativo, integração bancária, emissão fiscal, telemetria, rastreamento GPS e inteligência artificial serão avaliados em versões futuras.

---

## 🏗 Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend  │────▶│   REST API   │────▶│  PostgreSQL  │
│  React/Vite │     │ Spring Boot  │     │   (Flyway)   │
└─────────────┘     └──────┬───────┘     └──────────────┘
                           │
                    ┌──────┴───────┐
                    │    Redis     │
                    │  (opcional)  │
                    └──────────────┘
```

| Decisão | Escolha | Justificativa |
|---------|---------|---------------|
| Estilo | Monólito Modular | Simplicidade, manutenção, velocidade de evolução |
| Organização | Clean Architecture | Baixo acoplamento, testabilidade, independência de framework |
| Multi-tenant | Shared DB + Tenant Column | Custo reduzido, simplicidade, isolamento por `tenant_id` |
| Comunicação | REST + JSON | Padrão consolidado, documentação automática |
| Persistência | JPA/Hibernate + Flyway | ORM maduro, migrations versionadas |
| Autenticação | JWT Stateless | Escalável, sem sessão no servidor |
| Autorização | RBAC | Papéis claros e previsíveis |

### Decisões Arquiteturais Explícitas (NÃO utilizados)

Microsserviços, CQRS, Event Sourcing, DDD completo, Arquitetura Hexagonal, Kubernetes, Kafka, GraphQL, MongoDB. Podem ser avaliados futuramente mediante ADR.

---

## 🛠 Stack Tecnológica

### Backend

| Tecnologia | Versão | Responsabilidade |
|------------|--------|------------------|
| Java | 21 LTS | Linguagem principal |
| Spring Boot | 3.3 | Framework web, DI, configuração |
| Spring Security | 6.x | Autenticação e autorização |
| Spring Data JPA | 3.x | Persistência |
| Hibernate | 6.x | ORM |
| Flyway | 10.x | Migrations de banco |
| MapStruct | 1.5 | Mapeamento Entity ↔ DTO |
| Lombok | Latest | Redução de boilerplate |
| JJWT | 0.12 | Geração e validação de JWT |
| SpringDoc OpenAPI | 2.5 | Swagger automático |
| Maven | 3.9 | Build tool |

### Frontend

| Tecnologia | Versão | Responsabilidade |
|------------|--------|------------------|
| React | 18 | UI |
| TypeScript | 5.5 | Tipagem estática |
| Vite | 5.3 | Build tool e dev server |
| Axios | 1.7 | HTTP client |
| React Router | 6.x | Roteamento SPA |

### Infraestrutura

| Tecnologia | Versão | Responsabilidade |
|------------|--------|------------------|
| Docker | Latest | Containerização |
| Docker Compose | v2 | Orquestração local |
| PostgreSQL | 16 | Banco de dados |
| NGINX | Alpine | Reverse proxy, servir frontend |
| Redis | Latest | Cache e rate limiting (opcional) |

### Testes

| Tecnologia | Responsabilidade |
|------------|------------------|
| JUnit 5 | Testes unitários |
| Mockito | Mocking |
| Testcontainers | Testes de integração com banco real |

---

## 📦 Pré-requisitos

### Para rodar via Docker (recomendado)

| Ferramenta | Versão mínima | Download |
|------------|---------------|----------|
| Docker | 24+ | [docker.com](https://www.docker.com/products/docker-desktop/) |
| Docker Compose | v2+ | Incluído no Docker Desktop |

### Para rodar localmente (desenvolvimento)

| Ferramenta | Versão mínima | Download |
|------------|---------------|----------|
| Java JDK | 21 LTS | [adoptium.net](https://adoptium.net/) |
| Maven | 3.9+ | [maven.apache.org](https://maven.apache.org/download.cgi) |
| Node.js | 20 LTS | [nodejs.org](https://nodejs.org/) |
| PostgreSQL | 16 | [postgresql.org](https://www.postgresql.org/download/) |

---

## 🚀 Instalação e Execução

### Opção 1: Docker Compose (Recomendado)

A forma mais rápida de subir todo o sistema.

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/saas_locadora.git
cd saas_locadora
```

**2. Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env` conforme necessário (as configurações padrão funcionam para desenvolvimento):

```env
# Banco de dados
DB_HOST=postgres
DB_PORT=5432
DB_NAME=locadora
DB_USER=locadora_user
DB_PASSWORD=changeme

# JWT (TROCAR em produção!)
JWT_SECRET=your-256-bit-secret-key-change-in-production
JWT_ACCESS_EXPIRATION_MS=900000       # 15 minutos
JWT_REFRESH_EXPIRATION_MS=604800000   # 7 dias

# Aplicação
APP_PORT=8080
SPRING_PROFILES_ACTIVE=dev
```

**3. Suba os containers**

```bash
docker compose up --build
```

**4. Acesse o sistema**

| Serviço | URL |
|---------|-----|
| 🖥️ Frontend | [http://localhost:3000](http://localhost:3000) |
| ⚙️ Backend API | [http://localhost:8080/api/v1](http://localhost:8080/api/v1) |
| 📖 Swagger UI | [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html) |
| 💚 Health Check | [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health) |

**5. Para parar**

```bash
docker compose down
```

Para remover também os dados do banco:

```bash
docker compose down -v
```

---

### Opção 2: Execução Local (Desenvolvimento)

**1. Inicie o PostgreSQL**

Se tiver Docker apenas para o banco:

```bash
docker run -d \
  --name locadora-pg \
  -e POSTGRES_DB=locadora \
  -e POSTGRES_USER=locadora_user \
  -e POSTGRES_PASSWORD=changeme \
  -p 5432:5432 \
  postgres:16-alpine
```

Ou use uma instalação local do PostgreSQL e crie o banco:

```sql
CREATE DATABASE locadora;
CREATE USER locadora_user WITH PASSWORD 'changeme';
GRANT ALL PRIVILEGES ON DATABASE locadora TO locadora_user;
```

**2. Inicie o Backend**

```bash
cd backend

# Compilar
mvn clean compile

# Rodar testes
mvn test

# Iniciar a aplicação
mvn spring-boot:run
```

O backend estará em `http://localhost:8080`.

**3. Inicie o Frontend**

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar o dev server
npm run dev
```

O frontend estará em `http://localhost:3000` (ou `http://localhost:5173` se a porta 3000 estiver ocupada).

---

### Primeiros Passos: Registrando uma Empresa

Após subir o sistema, registre sua primeira empresa (tenant) usando a API:

```bash
curl -X POST http://localhost:8080/api/v1/empresas/registro \
  -H "Content-Type: application/json" \
  -d '{
    "nomeFantasia": "Locadora ABC",
    "razaoSocial": "ABC Locações LTDA",
    "cnpj": "12345678000100",
    "nomeAdmin": "Administrador",
    "emailAdmin": "admin@locadora.com",
    "senhaAdmin": "senha12345"
  }'
```

Resposta esperada:

```json
{
  "data": {
    "id": "uuid-da-empresa",
    "nomeFantasia": "Locadora ABC",
    "razaoSocial": "ABC Locações LTDA",
    "cnpj": "12345678000100",
    "ativo": true,
    "createdAt": "2026-07-04T16:00:00"
  },
  "message": "Empresa registrada com sucesso"
}
```

Depois, faça login:

```bash
curl -X POST http://localhost:8080/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@locadora.com",
    "senha": "senha12345"
  }'
```

Resposta:

```json
{
  "data": {
    "accessToken": "eyJhbGci...",
    "refreshToken": "eyJhbGci...",
    "tokenType": "Bearer",
    "expiresIn": 900
  }
}
```

Use o `accessToken` em todas as requisições autenticadas:

```bash
curl -H "Authorization: Bearer eyJhbGci..." \
  http://localhost:8080/api/v1/algum-recurso
```

---

## 📂 Estrutura do Projeto

```
saas_locadora/
├── docs/                          # Documentação técnica (fonte de verdade)
│   ├── 00-visao-produto.md
│   ├── 01-requisitos-funcionais.md
│   ├── 02-requisitos-nao-funcionais.md
│   ├── 03-arquitetura.md
│   ├── 04-stack-tecnologica.md
│   ├── 05-modelo-dominio.md
│   ├── 06-modelo-fisico.md
│   ├── 07-seguranca.md
│   ├── 08-guard-rails.md
│   ├── 09-padroes-codigo.md
│   ├── 10-api-conventions.md
│   ├── 11-infraestrutura.md
│   ├── 12-observabilidade.md
│   ├── 13-adr-template.md
│   ├── backlog-tecnico.md
│   └── ...
│
├── backend/                       # API Spring Boot
│   ├── pom.xml
│   ├── Dockerfile
│   └── src/
│       ├── main/java/com/locadora/
│       │   ├── LocadoraApplication.java
│       │   ├── config/            # Configurações (Security, CORS, OpenAPI)
│       │   ├── common/            # Base compartilhada
│       │   │   ├── entity/        # BaseEntity (colunas obrigatórias)
│       │   │   ├── dto/           # ApiResponse, PagedResponse, ErrorResponse
│       │   │   └── exception/     # Exceções + GlobalExceptionHandler
│       │   ├── security/          # JWT, AuthService, AuthController
│       │   ├── empresa/           # Módulo Empresa (tenant)
│       │   ├── usuario/           # Módulo Usuário + Roles
│       │   └── shared/tenant/     # TenantContext (ThreadLocal)
│       └── main/resources/
│           ├── application.yml
│           ├── application-dev.yml
│           ├── application-prod.yml
│           └── db/migration/      # Flyway migrations
│               ├── V1__create_empresas_table.sql
│               ├── V2__create_usuarios_table.sql
│               └── V3__create_usuario_roles_table.sql
│
├── frontend/                      # SPA React
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── src/
│       ├── main.tsx
│       ├── App.tsx                # Rotas e layout
│       ├── pages/Login.tsx        # Tela de login
│       ├── services/api.ts        # Axios + interceptors JWT
│       └── hooks/useAuth.ts       # Hook de autenticação
│
├── docker-compose.yml             # Orquestração (PostgreSQL + Backend + Frontend)
├── .env.example                   # Template de variáveis de ambiente
├── .gitignore
└── README.md
```

### Estrutura Interna dos Módulos (Backend)

Cada módulo de negócio segue a mesma organização:

```
modulo/
├── controller/     # Entrada HTTP (thin controller)
├── dto/            # Request e Response DTOs
├── entity/         # Entidade JPA
├── repository/     # Acesso a dados (Spring Data)
├── service/        # Regras de negócio
├── mapper/         # MapStruct (Entity ↔ DTO)
├── validator/      # Validações customizadas
└── exception/      # Exceções do módulo
```

---

## 🔌 API

### Convenções

| Item | Padrão |
|------|--------|
| Base URL | `/api/v1/` |
| Formato | JSON (UTF-8) |
| Autenticação | Bearer Token (JWT) |
| IDs | UUID |
| Datas | ISO-8601 (UTC) |
| Valores monetários | JSON Number (`DECIMAL(19,4)`) |
| Paginação | `?page=0&size=20&sort=nome,asc` |

### Endpoints Disponíveis (EPIC 0)

| Método | Endpoint | Autenticação | Descrição |
|--------|----------|--------------|-----------|
| `POST` | `/api/v1/empresas/registro` | ❌ Público | Registrar nova empresa + admin |
| `POST` | `/api/v1/auth/login` | ❌ Público | Login (retorna JWT) |
| `POST` | `/api/v1/auth/refresh` | ❌ Público | Renovar access token |
| `GET` | `/actuator/health` | ❌ Público | Health check |
| `GET` | `/swagger-ui.html` | ❌ Público | Documentação interativa |

### Padrão de Resposta

**Sucesso (objeto):**
```json
{
  "data": { "id": "...", "nome": "..." },
  "message": "Operação realizada"
}
```

**Sucesso (lista paginada):**
```json
{
  "data": [ ... ],
  "page": 0,
  "size": 20,
  "totalElements": 150,
  "totalPages": 8
}
```

**Erro:**
```json
{
  "timestamp": "2026-07-04T16:00:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Dados inválidos",
  "path": "/api/v1/clientes",
  "fieldErrors": [
    { "field": "email", "message": "E-mail inválido" }
  ]
}
```

---

## 🏢 Multi-Tenant

O sistema utiliza a estratégia **Shared Database + Shared Schema + Tenant Column**:

- Toda tabela de negócio possui a coluna `tenant_id` (UUID)
- Toda consulta filtra obrigatoriamente por `tenant_id`
- O `tenant_id` é extraído do **JWT do usuário autenticado** (nunca do frontend)
- É **impossível** acessar dados de outra empresa

```
Empresa A (tenant_id = aaa-111)     Empresa B (tenant_id = bbb-222)
┌──────────────────────┐            ┌──────────────────────┐
│ Clientes da A        │            │ Clientes da B        │
│ Veículos da A        │            │ Veículos da B        │
│ Contratos da A       │   🔒 🔒   │ Contratos da B       │
│ Financeiro da A      │  ISOLADO   │ Financeiro da B      │
└──────────────────────┘            └──────────────────────┘
```

---

## 🔒 Segurança

| Mecanismo | Implementação |
|-----------|---------------|
| Autenticação | JWT (Access Token 15min + Refresh Token 7 dias) |
| Senhas | BCrypt (nunca texto puro) |
| Autorização | RBAC com `@PreAuthorize` |
| Multi-tenant | Isolamento por `tenant_id` em todas as queries |
| Transporte | HTTPS obrigatório em produção |
| Headers | HSTS, CSP, X-Content-Type-Options, Frame-Options |
| CORS | Apenas domínios autorizados (nunca `*` em produção) |
| SQL Injection | JPA parametrizado (nunca SQL concatenado) |
| Secrets | Variáveis de ambiente (nunca no código) |
| Erros | Nunca expõe stacktrace, SQL ou estrutura interna |
| Logs | Nunca registra senhas, tokens ou dados sensíveis |

### Papéis (RBAC)

| Role | Descrição |
|------|-----------|
| `ADMIN` | Acesso total à empresa |
| `GERENTE` | Gestão operacional |
| `FINANCEIRO` | Módulo financeiro e relatórios |
| `OPERADOR` | Operações de balcão (contratos, clientes) |

---

## 🧪 Testes

### Executar testes

```bash
cd backend
mvn test
```

### Testes implementados

| Classe | Testes | Cobertura |
|--------|--------|-----------|
| `JwtTokenProviderTest` | 6 | Geração, validação, tipos de token, tenant_id |
| `EmpresaServiceTest` | 3 | Registro, CNPJ duplicado, email duplicado |
| `TenantContextTest` | 5 | Set/get, clear, require, isolamento entre threads |

### Convenções de teste

```java
@Test
@DisplayName("deve fazer X quando Y")
void deveFazerXQuandoY() {
    // Arrange → Act → Assert
}
```

- Testes unitários: **JUnit 5 + Mockito**
- Testes de integração: **Testcontainers** (PostgreSQL real em container)
- Todo bug corrigido deve gerar teste de regressão

---

## 🌐 Deploy em Produção

### Pré-requisitos de Produção

- VPS com Docker instalado
- Domínio configurado
- Certificado SSL (Let's Encrypt / Certbot)

### Deploy com Docker

```bash
# 1. Clone no servidor
git clone https://github.com/seu-usuario/saas_locadora.git
cd saas_locadora

# 2. Configure as variáveis de produção
cp .env.example .env
nano .env  # TROCAR TODOS OS SECRETS!

# 3. Suba em produção
SPRING_PROFILES_ACTIVE=prod docker compose up -d --build

# 4. Verifique
docker compose ps
curl http://localhost:8080/actuator/health
```

### Checklist de Produção

- [ ] `JWT_SECRET` — gerar chave forte de 256+ bits
- [ ] `DB_PASSWORD` — senha forte e única
- [ ] HTTPS configurado (NGINX + Certbot)
- [ ] CORS restrito ao domínio real
- [ ] Backup automático do banco
- [ ] Monitoramento e alertas
- [ ] Logs centralizados

---

## 🗺 Roadmap

O desenvolvimento segue a ordem definida no [backlog técnico](docs/backlog-tecnico.md):

| # | EPIC | Status | Descrição |
|---|------|--------|-----------|
| 0 | Base do Projeto | ✅ Concluído | Estrutura, Docker, JWT, multi-tenant |
| 1 | Autenticação e Multi-tenant | 🔜 Próximo | RBAC completo, tenant resolution |
| 3 | Frota (Veículos) | ⏳ | CRUD veículos, status, documentação |
| 2 | Cadastro de Clientes | ⏳ | PF/PJ, documentos, histórico |
| 4 | Contratos | ⏳ | Locação, km, devolução, danos |
| 5 | Financeiro | ⏳ | Receitas, despesas, fluxo de caixa |
| 6 | Manutenção | ⏳ | Preventiva/corretiva, custos |
| 7 | Dashboard | ⏳ | KPIs, indicadores, gráficos |
| 8 | Relatórios | ⏳ | PDF, Excel, filtros |
| 9 | Segurança Reforçada | ⏳ | Auditoria, rate limiting, hardening |
| 10 | Infraestrutura e Deploy | ⏳ | CI/CD, HTTPS, monitoramento |

> **Nota:** EPICs 2 e 3 estão invertidos propositalmente — a frota é o núcleo do produto e deve existir antes dos clientes.

---

## 📚 Documentação Técnica

Toda a especificação do sistema está na pasta [`docs/`](docs/):

| Documento | Conteúdo |
|-----------|----------|
| [Visão do Produto](docs/00-visao-produto.md) | Objetivo, problema, solução, público-alvo |
| [Requisitos Funcionais](docs/01-requisitos-funcionais.md) | 80 requisitos funcionais (RF-001 a RF-080) |
| [Requisitos Não Funcionais](docs/02-requisitos-nao-funcionais.md) | 60 requisitos de qualidade (RNF-001 a RNF-060) |
| [Arquitetura](docs/03-arquitetura.md) | Clean Architecture, camadas, módulos |
| [Stack Tecnológica](docs/04-stack-tecnologica.md) | Todas as tecnologias e versões |
| [Modelo de Domínio](docs/05-modelo-dominio.md) | Agregados, Value Objects, regras |
| [Modelo Físico](docs/06-modelo-fisico.md) | Convenções do banco, tipos, índices |
| [Segurança](docs/07-seguranca.md) | Políticas de segurança completas |
| [Guard Rails](docs/08-guard-rails.md) | Regras obrigatórias para desenvolvimento |
| [Padrões de Código](docs/09-padroes-codigo.md) | Clean Code, SOLID, nomenclatura |
| [Convenções da API](docs/10-api-conventions.md) | REST, respostas, paginação, erros |
| [Infraestrutura](docs/11-infraestrutura.md) | Ambientes, deploy, containers |
| [Observabilidade](docs/12-observabilidade.md) | Logs, métricas, health checks |
| [ADR Template](docs/13-adr-template.md) | Template para decisões arquiteturais |
| [Backlog Técnico](docs/backlog-tecnico.md) | EPICs 0 a 10 com ordem de execução |

> A pasta `docs/` é a **fonte única de verdade** do sistema. Nenhuma funcionalidade é implementada sem documentação prévia.

---

## 📄 Licença

Este projeto é privado e proprietário. Todos os direitos reservados.

---

<p align="center">
  Feito com ☕ Java 21 + ⚛️ React + 🐘 PostgreSQL + 🐳 Docker
</p>
