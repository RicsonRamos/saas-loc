# Observabilidade

## Objetivo

Definir como o sistema será monitorado, rastreado e analisado em produção.

---

# Pilares

- Logs
- Métricas
- Tracing (futuro)

---

# Logs

## Regras

- Logs estruturados
- Formato JSON (preferencial)
- Níveis claros:

INFO
WARN
ERROR
DEBUG

---

## Proibições

- Nunca logar senha
- Nunca logar token
- Nunca logar dados sensíveis
- Nunca logar documentos completos

---

## Conteúdo obrigatório

- timestamp
- tenant_id
- user_id
- endpoint
- status
- tempo de execução

---

# Métricas

Coletar:

- tempo de resposta
- taxa de erro
- uso de CPU
- uso de memória
- número de requisições
- consultas ao banco

---

# Health Checks

Obrigatórios:

- aplicação
- banco de dados
- cache
- storage

Endpoint padrão:

/actuator/health

---

# Alertas

Configurar alertas para:

- alta taxa de erro
- lentidão
- indisponibilidade
- falha de banco
- falha de autenticação

---

# Auditoria vs Logs

Logs:

- técnicos
- diagnóstico
- sistema

Auditoria:

- ações do usuário
- rastreabilidade legal
- mudanças em dados

---

# Rastreabilidade

Toda requisição deve ser rastreável por:

- request_id
- tenant_id
- user_id

---

# Performance Monitoring

Monitorar:

- endpoints mais lentos
- queries mais pesadas
- gargalos de memória

---

# Ferramentas (sugestão)

- Spring Boot Actuator
- Prometheus
- Grafana
- Loki (logs)

---

# Evolução

Fase inicial:

- logs locais
- Actuator básico

Fase avançada:

- stack completa de observabilidade

---

# Princípio Final

Sem observabilidade, não existe confiabilidade em produção.