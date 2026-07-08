# 01 · Arquitetura do Sistema

## Prompt de Alto Nível
Projete uma arquitetura em camadas simples e pragmática. Não use Arquitetura Hexagonal completa nem DDD tático (agregados, eventos de domínio, ports/adapters explícitos) a menos que uma regra de negócio realmente exija esse isolamento — para um time pequeno construindo um MVP, essa cerimônia custa mais do que entrega. O objetivo é código fácil de entender e modificar, com separação clara entre "como os dados entram" (API), "o que o sistema faz" (regras de negócio) e "onde os dados ficam" (banco).

Ao propor um módulo, descreva: rota, schema de entrada/saída, regra de negócio principal e tabela(s) afetadas. Evite qualquer abstração que não reduza esforço real.

## Visão de Camadas
```text
Frontend (React)
     |
     v
API Layer — FastAPI routers + schemas Pydantic (validação de entrada/saída)
     |
     v
Service Layer — regras de negócio, transações, validações
     |
     v
Repository/ORM Layer — SQLAlchemy models e queries
     |
     v
PostgreSQL
```

## Contratos de Camada
1. **Routers (`api/`):** recebem a request, validam com Pydantic, chamam um service, devolvem um schema de saída. Não contêm regra de negócio.
2. **Services (`services/`):** contêm a lógica de negócio (ex.: `ContratoService.criar_locacao`), abrem transação, chamam repositórios/models e lançam exceções de domínio.
3. **Repositories/Models (`models/`, `repositories/`):** SQLAlchemy. Crie um repositório dedicado só quando a query for reutilizada em mais de um lugar; caso contrário, query direta no service é aceitável.
4. **Schemas (`schemas/`):** Pydantic para entrada e saída de cada endpoint.

## Estrutura de Pastas — Backend
```text
backend/
├── app/
│   ├── api/
│   │   ├── frota.py
│   │   ├── contratos.py
│   │   ├── manutencoes.py
│   │   └── financeiro.py
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── core/          # config, auth, sessão de banco
│   └── main.py
├── migrations/
├── tests/
└── README.md
```

## Estrutura de Pastas — Frontend
```text
frontend/
├── src/
│   ├── core/           # api client, auth, providers
│   ├── components/ui/
│   ├── features/
│   │   ├── frota/
│   │   ├── contratos/
│   │   ├── manutencoes/
│   │   └── financeiro/
│   ├── routes/
│   └── main.tsx
```

## Quando Adicionar uma Camada Extra
Só introduza uma abstração nova (ex.: Unit of Work explícito, fila de eventos, cache dedicado) quando:

- a mesma lógica se repetir em três ou mais lugares; ou
- um teste ficar impossível de escrever sem o isolamento; ou
- houver um requisito de performance ou concorrência comprovado (ex.: proteção contra dupla reserva de veículo).

## Critérios de Aceite
Uma proposta arquitetural é válida quando:

- separa claramente API, regra de negócio e acesso a dados;
- não introduz camada ou padrão sem justificativa concreta;
- inclui teste do fluxo principal;
- descreve o comportamento em erro (o que a API retorna e por quê).
