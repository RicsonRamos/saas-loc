# Stack Tecnológica

## Objetivo

Definir todas as tecnologias oficiais utilizadas no projeto, suas versões, responsabilidades e critérios de adoção.

---

# Princípios

A stack deverá priorizar:

- Estabilidade
- LTS (Long Term Support)
- Comunidade ativa
- Boa documentação
- Ecossistema consolidado
- Facilidade de manutenção
- Escalabilidade

Não serão adotadas tecnologias experimentais em ambiente de produção.

---

# Backend

## Linguagem

Java 21 (LTS)

Motivos:

- Suporte de longo prazo
- Excelente desempenho
- Ecossistema maduro
- Forte tipagem
- Ampla adoção corporativa

---

## Framework

Spring Boot

Responsabilidades:

- API REST
- Injeção de Dependência
- Configuração
- Validação
- Segurança
- Persistência

---

## Build Tool

Maven

---

# Persistência

## Banco de Dados

PostgreSQL

Motivos:

- Open Source
- Excelente desempenho
- Confiabilidade
- Recursos avançados
- Escalabilidade

---

## ORM

Hibernate

Utilizado através do Spring Data JPA.

---

## Versionamento do Banco

Flyway

Obrigatório para todas as alterações estruturais.

É proibido alterar tabelas manualmente.

---

# Frontend

## Framework

React

---

## Linguagem

TypeScript

---

## Build

Vite

---

# Segurança

Spring Security

JWT

BCrypt

HTTPS obrigatório.

---

# Documentação

OpenAPI

Swagger

Toda API deverá ser documentada automaticamente.

---

# Testes

JUnit 5

Mockito

Testcontainers

Objetivos:

- Testes unitários
- Testes de integração
- Testes da camada de persistência

---

# Containers

Docker

Docker Compose

Todo ambiente deverá executar através de containers.

---

# Proxy Reverso

NGINX

Responsabilidades:

- HTTPS
- Proxy reverso
- Compressão
- Cache estático

---

# Cache

Redis

Utilização:

- Cache
- Sessões
- Rate Limiting

Não utilizar Redis como banco principal.

---

# Storage

Inicialmente:

Supabase Storage

Arquivos armazenados:

- CNH
- Contratos
- Fotos
- Documentos

A aplicação armazenará apenas os metadados.

A implementação deverá permitir migração futura para armazenamento compatível com S3 sem alterações na regra de negócio.

---

# Banco em Nuvem

Inicialmente:

Supabase PostgreSQL

Motivos:

- Plano gratuito
- Rapidez para MVP
- PostgreSQL nativo
- Fácil migração futura

O sistema nunca deverá depender de funcionalidades proprietárias do Supabase além do banco e armazenamento.

---

# Hospedagem

MVP

Frontend:

Vercel

Backend:

Render ou Railway

Banco:

Supabase

---

Produção

Servidor VPS

Docker

NGINX

PostgreSQL

Redis

---

# Versionamento

Git

GitHub

Estratégia:

main

develop

feature/*

hotfix/*

release/*

---

# CI/CD

GitHub Actions

Responsabilidades:

- Build
- Testes
- Análise estática
- Deploy

---

# Qualidade

Checkstyle

SpotBugs

SonarQube (futuro)

---

# Logs

SLF4J

Logback

Logs estruturados.

---

# Mapeamento

MapStruct

Proibido realizar conversões repetitivas manualmente.

---

# Utilitários

Lombok

Utilização restrita para reduzir código boilerplate.

Não utilizar anotações que escondam comportamento complexo.

---

# Validação

Jakarta Validation

Obrigatório em todos os DTOs de entrada.

---

# Comunicação

REST

JSON

UTF-8

HTTPS

---

# Ferramentas de Desenvolvimento

IntelliJ IDEA

Visual Studio Code

Postman

Insomnia

DBeaver

---

# Monitoramento (Futuro)

Spring Boot Actuator

Prometheus

Grafana

---

# Dependências Permitidas

As dependências deverão:

- possuir manutenção ativa
- possuir licença compatível
- possuir documentação
- possuir comunidade consolidada

---

# Dependências Proibidas

Bibliotecas abandonadas.

Frameworks experimentais.

Dependências sem manutenção.

Dependências duplicadas.

---

# Política de Atualização

Atualizações deverão priorizar versões LTS.

Atualizações maiores deverão ser precedidas de testes completos.

---

# Tecnologias Não Adotadas

Não serão utilizadas inicialmente:

- Microsserviços
- Kubernetes
- Kafka
- RabbitMQ
- GraphQL
- MongoDB
- Cassandra
- Elasticsearch
- CQRS
- Event Sourcing

Essas tecnologias poderão ser avaliadas futuramente mediante necessidade comprovada e documentação em ADR.

---

# Princípio Final

A escolha de uma tecnologia deve ser motivada por necessidade técnica ou de negócio.

Nenhuma biblioteca ou framework poderá ser incorporado ao projeto apenas por tendência, preferência pessoal ou novidade tecnológica.