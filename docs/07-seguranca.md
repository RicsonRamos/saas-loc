# 07 · Segurança

## Prompt de Alto Nível
Aplique controles de segurança proporcionais ao risco real: dados de clientes, contratos e pagamentos são sensíveis, mas o sistema é single-tenant e de uso interno — não precisa do aparato de um SaaS enterprise multi-cliente (SSO corporativo, SOC2, auditoria cross-tenant).

Ao criar uma feature que toca dado sensível ou dinheiro, pense: quem pode ver isso, o que fica no log, e o que acontece se a validação falhar.

## Controles Essenciais
| Risco | Controle |
|---|---|
| Acesso indevido | RBAC no backend, nunca só escondido no frontend |
| Configuração insegura | segredos fora do repositório, HTTPS em produção |
| Dependências vulneráveis | `pip audit`/`npm audit` periódico |
| Injeção | SQLAlchemy parametrizado, validação Pydantic/Zod |
| Falha de autenticação | senha com hash forte, rate limit no login |
| Exceções mal tratadas | handler global, sem stack trace na resposta |

## Dados Sensíveis
Documentos de cliente, contratos e dados de pagamento devem: usar storage privado (nunca bucket público), não aparecer em log, e ter acesso restrito por permissão explícita.

## Segredos
Variáveis de ambiente/`.env` ficam fora do Git, carregadas via variáveis do provedor de deploy. Nunca commitar `.env` com valor real.

## Rate Limiting
Limite básico em login e em endpoints de criação de contrato/pagamento, para evitar abuso ou bug de duplo submit em loop.

## Critérios de Aceite
Uma feature está segura o suficiente para avançar quando:

- nenhum endpoint crítico roda sem checagem de permissão;
- segredos estão fora do repositório (checado por `gitleaks` no CI);
- erros não vazam stack trace ao cliente;
- logs não contêm senha, token ou dado de pagamento completo.
