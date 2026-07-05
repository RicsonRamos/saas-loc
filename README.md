# 🚗 Locadora ERP Desktop (Local)

**Sistema ERP Desktop/Local multi-tenant para gestão de locadoras de veículos.**

Plataforma unificada executada localmente usando **SQLite** como banco de dados embarcado e servindo o frontend **React** diretamente a partir do próprio servidor **Spring Boot**.

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura Local](#-arquitetura-local)
- [Stack Tecnológica](#-stack-tecnológica)
- [Pré-requisitos](#-pré-requisitos)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instalação e Execução](#-instalação-e-execução)
- [Configuração Local](#-configuração-local)
- [Backup Automatizado](#-backup-automatizado)
- [Empacotamento Desktop (Locadora.exe)](#-empacotamento-desktop-locadoraexe)
- [Segurança](#-segurança)
- [Licença](#-licença)

---

## 🎯 Visão Geral

O **Locadora ERP Desktop** é um sistema completo projetado para rodar em computadores locais sem a necessidade de instalar servidores de banco de dados pesados, Docker ou proxies reversos como Nginx. 

Toda a infraestrutura é empacotada no executável Java: o banco de dados é um arquivo SQLite local e as páginas React são servidas diretamente pelo Spring Boot.

### Diferenciais Operacionais
- **Lucro por veículo** — saiba exatamente quanto cada carro rende.
- **Custo por quilômetro** — controle granular de despesas.
- **Payback do investimento** — tempo estimado de retorno por veículo.
- **Comparação FIPE vs valor pago** — decisões de compra/venda embasadas.
- **Taxa de ocupação** — otimize sua frota.
- **Multi-tenant** — suporte a múltiplas filiais ou empresas isoladas por `tenant_id` no mesmo banco local.

---

## ✨ Funcionalidades

| Módulo | Descrição |
|--------|-----------|
| **Usuários** | Cadastro, login, RBAC granular com permissões e profiles (Admin, Gerente, Financeiro, Operador) |
| **Clientes** | Pessoa física/jurídica, CNH categoria, bloqueio de clientes, observações |
| **Veículos** | Frota completa (placa, chassi, Renavam, quilometragem, combustível, câmbio, capacidade do tanque, revisões, IPVA, licenciamento, CRLV) |
| **Contratos** | Locação com período, caução, km inicial/final, vistoria de devolução, multas e assinatura |
| **Reservas** | Módulo de agendamentos com validação de sobreposição de frota e conversão para contrato |
| **Uploads** | Armazenamento de arquivos no diretório local seguro com validação de mime-type e hash SHA-256 |
| **Checklists** | Vistorias dinâmicas em JSON para Retirada e Devolução com comparação automática de avarias |
| **Financeiro** | Caixa com despesas/receitas, centro de custo, formas de pagamento, parcelas e comprovantes |
| **Manutenção** | Cadastro de oficinas, peças, custos e desvio automático de despesa para o financeiro |
| **Alertas** | Notificação automática de CNHs vencendo em 30 dias e prazos de seguros/IPVA de veículos |
| **Auditoria** | Registro de alterações de registros com Correlation ID, old/new data em JSON, IP e User-Agent |

---

## 🏗 Arquitetura Local

```
┌──────────────────────────────────────┐
│             Locadora.exe             │
│  ┌──────────────┐     ┌───────────┐  │
│  │   Frontend   │◀───▶│  Backend  │  │
│  │ React Static │     │Spring Boot│  │
│  └──────────────┘     └─────┬─────┘  │
│                             │        │
│                       ┌─────▼─────┐  │
│                       │  SQLite   │  │
│                       │locadora.db│  │
│                       └───────────┘  │
└──────────────────────────────────────┘
```

A arquitetura preserva os princípios de **Clean Architecture** e isolamento por submódulos (Controller, Service, Repository, DTO). A persistência é realizada em um arquivo SQLite localizado em `./database/locadora.db` utilizando o dialeto do Hibernate para SQLite.

---

## 🛠 Stack Tecnológica

### Backend
- **Java 21 LTS**
- **Spring Boot 3.3.0** (Spring Security, Data JPA, Actuator)
- **SQLite JDBC Driver**
- **Hibernate ORM / Dialeto de Comunidade SQLite**
- **MapStruct 1.5** (Mapeamento DTO ↔ Entity)
- **Lombok**
- **JJWT 0.12** (Segurança Stateless JWT)
- **SpringDoc OpenAPI 2.5** (Swagger)

### Frontend
- **React 18**
- **TypeScript 5.5**
- **Vite 5.3** (Build pipeline)
- **Tailwind CSS & Shadcn/UI** (Interface)
- **React Router 6**

---

## 📦 Pré-requisitos

Para rodar ou construir o projeto em ambiente de desenvolvimento:
- **Java JDK 21**
- **Node.js 20 LTS**
- **Maven 3.9+**

---

## 📁 Estrutura do Projeto

```
saas_locadora/
├── backend/                  # Código Spring Boot
│   └── src/main/resources/   # Configurações e estáticos embarcados
├── frontend/                 # Código React + Vite
├── database/                 # Pasta criada automaticamente com o SQLite (locadora.db)
├── logs/                     # Pasta criada automaticamente contendo logs diários
├── backup/                   # Backups gerados pelo sistema (.db)
└── config/                   # Configurações locais (application.properties)
```

---

## 🚀 Instalação e Execução

### 1. Build do Frontend
Compile o frontend para que os arquivos estáticos sejam transferidos para o backend:
```bash
cd frontend
npm install
npm run build
```
*O build do Vite exporta os arquivos estáticos compilados para `backend/src/main/resources/static/` automaticamente.*

### 2. Executar o Backend
Inicie a aplicação Spring Boot usando o profile `desktop`:
```bash
cd ../backend
mvn clean package
java -jar target/locadora-backend-0.1.0-SNAPSHOT.jar --spring.profiles.active=desktop
```

### 3. Acessar a aplicação
Abra o navegador e acesse:
```
http://localhost:8080
```

---

## ⚙ Configuração Local

Na primeira execução, o diretório `./config` e o arquivo `./config/application.properties` serão criados automaticamente com as seguintes propriedades padrão:
```properties
# Configurações Locais - Locadora ERP Desktop
server.port=8080
app.company.name=Locadora Local
app.language=pt-BR
app.timezone=America/Sao_Paulo
```
Você pode alterar a porta de execução ou o fuso horário modificando diretamente esse arquivo e reiniciando a aplicação.

---

## 💾 Backup Automatizado

O sistema possui um módulo nativo de backup físico do arquivo SQLite. O backup pode ser disparado a qualquer momento enviando uma requisição HTTP POST para `/api/v1/backups` (acesso restrito aos perfis `ADMIN` e `GERENTE`).

O backup é gerado na pasta `./backup` no seguinte formato:
```
backup/locadora-AAAA-MM-DD-HH-mm.db
```

---

## 📦 Empacotamento Desktop (Locadora.exe)

O projeto está estruturado para permitir a geração de uma imagem nativa empacotada usando a ferramenta `jpackage` do JDK 21.

Exemplo de comando de geração do instalador nativo no Windows:
```bash
jpackage --name "LocadoraERP" \
         --input backend/target \
         --main-jar locadora-backend-0.1.0-SNAPSHOT.jar \
         --main-class com.locadora.Application \
         --type exe \
         --win-shortcut \
         --win-menu
```

---

## 🔒 Segurança

Toda a segurança corporativa foi mantida:
- **Criptografia de Senhas**: As senhas dos usuários são salvas com hash BCrypt.
- **Autorização por Perfil/Permissão**: O acesso às ações é validado no backend através de anotações `@PreAuthorize("hasAuthority('...')")`.
- **Sessões Isoladas**: Autenticação feita via JWT contendo informações do usuário e do Tenant ID ao qual pertence.
- **Isolamento de Dados**: O banco de dados local SQLite possui suporte multi-tenant, permitindo separar filiais por `tenant_id`.

---

## 📄 Licença

Este projeto é desenvolvido sob licença comercial privada. Uso não autorizado é proibido.
