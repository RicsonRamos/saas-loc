# Segurança

## Objetivo

Definir todas as políticas de segurança da aplicação.

Toda implementação deverá seguir obrigatoriamente este documento.

Segurança é responsabilidade de toda a aplicação, não apenas do módulo de autenticação.

---

# Princípios

Security by Design

Least Privilege

Zero Trust

Defense in Depth

Fail Secure

Secure Defaults

Nunca confiar em dados enviados pelo cliente.

Toda validação crítica deve ocorrer no backend.

---

# Autenticação

Será utilizada autenticação baseada em JWT.

Características:

- Access Token
- Refresh Token
- Expiração configurável
- Tokens assinados
- Stateless

Nunca armazenar sessões no servidor.

---

# Login

Autenticação por:

- E-mail
- Senha

Futuramente:

- MFA
- Login Social

---

# Senhas

Obrigatório:

BCrypt

Nunca armazenar senha em texto puro.

Nunca utilizar criptografia reversível.

Requisitos mínimos:

- mínimo 8 caracteres
- pelo menos uma letra
- pelo menos um número

---

# Autorização

Modelo:

RBAC

Papéis iniciais:

Administrador

Gerente

Financeiro

Operador

Cada endpoint deverá validar permissões.

---

# Multi-Tenant

Todo usuário pertence a apenas um tenant.

Todo recurso pertence a apenas um tenant.

Toda consulta deve filtrar tenant_id.

É proibido permitir acesso cruzado entre empresas.

---

# Validação

Toda entrada deve ser validada.

Nunca confiar em:

- IDs
- Valores monetários
- Datas
- Tenant enviado pelo frontend

O tenant será obtido exclusivamente do usuário autenticado.

---

# Transporte

HTTPS obrigatório.

TLS obrigatório em produção.

Não aceitar conexões inseguras.

---

# Headers HTTP

Adicionar obrigatoriamente:

Strict-Transport-Security

Content-Security-Policy

X-Content-Type-Options

Referrer-Policy

Permissions-Policy

Frame-Options

---

# CORS

Permitir apenas domínios autorizados.

Nunca utilizar:

*

em produção.

---

# CSRF

Como a API utilizará JWT Stateless:

CSRF não será necessário para endpoints autenticados.

Caso cookies sejam utilizados futuramente, essa decisão deverá ser revisada.

---

# SQL Injection

Obrigatório:

Spring Data JPA

Queries parametrizadas.

Nunca concatenar SQL.

---

# XSS

Toda saída HTML deverá ser sanitizada.

Nunca renderizar conteúdo enviado pelo usuário sem validação.

---

# Upload de Arquivos

Validar:

- extensão
- MIME Type
- tamanho

Nunca confiar apenas na extensão.

Arquivos executáveis são proibidos.

---

# Dados Sensíveis

Nunca registrar em logs:

- senhas
- tokens
- documentos completos
- dados bancários
- cartões
- refresh tokens

---

# Auditoria

Registrar:

Usuário

Tenant

IP

Data

Operação

Entidade

Resultado

---

# Rate Limiting

Implementar limitação por:

- IP
- Usuário

Objetivo:

Evitar ataques de força bruta.

---

# Bloqueio de Conta

Após sucessivas tentativas inválidas:

Bloqueio temporário.

Registrar tentativa.

---

# Secrets

Nunca armazenar:

- senhas
- tokens
- chaves
- URLs privadas

no código.

Utilizar:

Variáveis de ambiente.

---

# Banco de Dados

Utilizar usuário com privilégios mínimos.

Não utilizar usuário administrador da instância.

---

# Backup

Backups automáticos.

Backups criptografados.

Testes periódicos de restauração.

---

# Logs

Logs estruturados.

Separar:

INFO

WARN

ERROR

AUDIT

---

# Dependências

Atualizar dependências periodicamente.

Não utilizar bibliotecas abandonadas.

Monitorar vulnerabilidades.

---

# LGPD

Coletar apenas dados necessários.

Permitir anonimização.

Permitir exportação de dados.

Permitir exclusão conforme legislação.

---

# Sessões

Logout deverá invalidar Refresh Token.

Access Token possui curta duração.

---

# API

Nunca expor:

Stack Trace

SQL

Estrutura interna

Detalhes da infraestrutura

Mensagens técnicas

---

# Princípios Finais

Segurança possui prioridade sobre conveniência.

Nenhuma funcionalidade poderá reduzir o nível de segurança do sistema.

Toda exceção deverá ser documentada em ADR.