# Convenções da API

## Objetivo

Padronizar todas as APIs REST da aplicação.

Toda nova API deverá seguir este documento.

---

# Arquitetura

REST

JSON

UTF-8

HTTPS

---

# Versionamento

/api/v1/

Exemplo:

/api/v1/clientes

/api/v1/veiculos

---

# Recursos

Utilizar substantivos.

Correto:

/clientes

/veiculos

/contratos

Errado:

/buscarCliente

/getCliente

/saveCliente

---

# Métodos HTTP

GET

Consultar

POST

Criar

PUT

Atualizar completamente

PATCH

Atualização parcial

DELETE

Exclusão lógica

---

# Respostas

200 OK

201 Created

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Unprocessable Entity

500 Internal Server Error

---

# Padrão de Resposta

Sucesso:

{
    "data": {}
}

Lista:

{
    "data": [],
    "page": 1,
    "size": 20,
    "totalElements": 150,
    "totalPages": 8
}

Erro:

{
    "timestamp": "...",
    "status": 400,
    "error": "...",
    "message": "...",
    "path": "..."
}

---

# Paginação

Obrigatória.

Parâmetros:

page

size

sort

---

# Ordenação

sort=nome,asc

sort=data,desc

---

# Filtros

Sempre via Query Parameters.

Exemplo:

?status=ATIVO

?placa=ABC1234

---

# IDs

UUID.

Nunca utilizar IDs sequenciais.

---

# Datas

ISO-8601

UTC

---

# Valores Monetários

JSON Number.

Nunca String.

---

# Upload

Multipart/form-data.

---

# Download

Content-Disposition.

---

# Erros

Mensagens claras.

Nunca expor:

SQL

Stack Trace

Framework interno

---

# Validação

Bean Validation.

Retornar lista completa de erros.

---

# Autenticação

Bearer Token.

Authorization:

Bearer <token>

---

# Tenant

Nunca recebido via Body.

Nunca recebido via Query.

Nunca recebido via Header público.

Obtido do usuário autenticado.

---

# Idempotência

GET

PUT

DELETE

Devem ser idempotentes.

---

# Convenção de Endpoints

GET /clientes

GET /clientes/{id}

POST /clientes

PUT /clientes/{id}

PATCH /clientes/{id}

DELETE /clientes/{id}

---

# Pesquisa

Utilizar Query Parameters.

Nunca criar endpoint específico para cada filtro.

---

# Relatórios

Utilizar:

/relatorios

---

# Dashboard

Utilizar:

/dashboard

---

# Health Check

/actuator/health

---

# Documentação

Swagger obrigatório.

Toda API documentada.

---

# Compatibilidade

Não quebrar APIs existentes.

Mudanças incompatíveis:

Nova versão.

---

# Performance

Paginação obrigatória.

Compressão HTTP.

Cache quando necessário.

---

# Segurança

HTTPS obrigatório.

JWT obrigatório.

RBAC obrigatório.

Rate Limiting.

---

# Princípio Final

Toda API deve ser:

Consistente.

Previsível.

Versionada.

Documentada.

Segura.

Simples.