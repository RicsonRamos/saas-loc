# Arquitetura

## Objetivo

Definir a arquitetura oficial do sistema SaaS de gestão para locadoras de veículos.

Todas as implementações deverão seguir este documento.

---

# Filosofia

O projeto prioriza:

- Simplicidade
- Modularidade
- Baixo acoplamento
- Alta coesão
- Facilidade de manutenção
- Escalabilidade gradual
- Segurança
- Clareza

O sistema não será desenvolvido utilizando microsserviços.

A arquitetura adotada será um Monólito Modular.

---

# Estilo Arquitetural

Arquitetura:

Monólito Modular

Organização interna:

Clean Architecture

Comunicação:

REST

Frontend separado do Backend.

---

# Arquitetura Geral

Frontend

↓

REST API

↓

Controllers

↓

Application Services

↓

Domain

↓

Repositories

↓

PostgreSQL

---

# Organização em Camadas

## Presentation

Responsável por:

- Controllers
- DTOs
- Validações de entrada
- Tratamento HTTP

Não contém regra de negócio.

---

## Application

Responsável por:

- Casos de uso
- Orquestração
- Transações
- Comunicação entre módulos

---

## Domain

Responsável por:

- Entidades
- Value Objects
- Regras de negócio
- Serviços de domínio
- Interfaces

Esta camada não conhece Spring Boot.

---

## Infrastructure

Responsável por:

- Banco
- JPA
- Segurança
- Cache
- Storage
- Serviços externos

---

# Arquitetura Modular

Cada módulo deverá ser independente.

Exemplo:

empresa

usuario

cliente

veiculo

contrato

financeiro

manutencao

dashboard

auditoria

notificacao

Cada módulo deverá possuir suas próprias:

- entidades
- services
- repositories
- controllers
- DTOs
- exceptions

---

# Multi-Tenant

A aplicação será Multi-Tenant.

Estratégia:

Shared Database

Shared Schema

Tenant Column

Toda entidade deverá possuir:

tenant_id

Toda consulta deverá considerar obrigatoriamente o tenant.

Nenhuma operação poderá ignorar este filtro.

---

# Comunicação

Toda comunicação entre frontend e backend será REST.

Padrões:

JSON

HTTPS

UTF-8

Versionamento:

/api/v1/

---

# Banco de Dados

Banco oficial:

PostgreSQL

Toda alteração estrutural será realizada utilizando:

Flyway

Não será permitido alterar estrutura manualmente.

---

# Persistência

ORM oficial:

Hibernate

Framework:

Spring Data JPA

Repositories deverão conter apenas acesso a dados.

Não poderão conter regras de negócio.

---

# Injeção de Dependência

Será utilizada exclusivamente a injeção de dependência do Spring.

Não utilizar instâncias criadas manualmente.

---

# Estrutura do Projeto

src/main/java

config/

common/

empresa/

usuario/

cliente/

veiculo/

contrato/

financeiro/

manutencao/

dashboard/

auditoria/

security/

shared/

Cada módulo deverá possuir independência lógica.

---

# Estrutura Interna dos Módulos

controller/

dto/

entity/

repository/

service/

mapper/

validator/

exception/

---

# Tratamento de Erros

Será utilizado tratamento global.

Nenhum Controller deverá possuir try/catch para regras de negócio.

As exceções deverão ser convertidas em respostas HTTP padronizadas.

---

# DTOs

Entidades nunca serão expostas diretamente.

Toda comunicação utilizará DTOs.

Entrada:

Request DTO

Saída:

Response DTO

---

# Mapeamento

Será utilizado MapStruct.

Não realizar conversões manuais repetitivas.

---

# Segurança

Autenticação:

JWT

Autorização:

RBAC

Passwords:

BCrypt

---

# Auditoria

Toda alteração deverá registrar:

Usuário

Data

Tenant

Entidade

Operação

IP

---

# Logs

Logs deverão ser estruturados.

Nunca registrar:

Senhas

Tokens

Documentos completos

Dados bancários

---

# Cache

Redis poderá ser utilizado para:

Sessões

Cache de consultas

Rate Limiting

Nunca armazenar regras de negócio apenas em cache.

---

# Upload de Arquivos

Arquivos serão armazenados fora da aplicação.

A aplicação armazenará apenas metadados.

---

# Observabilidade

A aplicação deverá disponibilizar:

Health Check

Métricas

Logs

Tracing (futuro)

---

# Containers

Toda aplicação deverá executar via Docker.

Desenvolvimento:

Docker Compose

Produção:

Docker

---

# Escalabilidade

A arquitetura deverá permitir:

Adicionar novas instâncias da API

Separar banco futuramente

Adicionar cache

Adicionar CDN

Sem alteração da regra de negócio.

---

# Integrações Futuras

A arquitetura deverá suportar:

Gateway de pagamento

WhatsApp

E-mail

Assinatura digital

Consulta FIPE

OCR

Integrações bancárias

---

# Princípios Obrigatórios

Nunca acessar banco diretamente pelo Controller.

Nunca colocar regra de negócio no Repository.

Nunca misturar responsabilidades.

Nunca utilizar SQL concatenado.

Nunca quebrar isolamento entre tenants.

Nunca retornar entidades JPA pela API.

Nunca depender diretamente de detalhes da infraestrutura.

Toda regra de negócio deverá estar no domínio ou na camada de aplicação.

---

# Decisões Arquiteturais

Microsserviços NÃO serão utilizados.

CQRS NÃO será utilizado inicialmente.

Event Sourcing NÃO será utilizado.

DDD completo NÃO será adotado.

Arquitetura Hexagonal NÃO será utilizada inicialmente.

A prioridade é simplicidade, manutenção e velocidade de evolução.

Caso alguma dessas decisões seja revista no futuro, deverá ser criada uma ADR justificando a alteração.