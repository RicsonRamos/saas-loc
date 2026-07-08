# 05 · Frontend

## Prompt de Alto Nível
Construa telas operacionais reais para a equipe da locadora usar no dia a dia: cadastro de frota, fluxo de contrato/locação, registro de manutenção e visão financeira. Cada tela deve cobrir estado de carregamento, vazio, erro e sucesso — não é uma landing page.

## Estrutura (Feature-Driven)
```text
src/
├── core/               # api client, auth, providers
├── components/ui/
├── features/
│   ├── frota/
│   ├── contratos/
│   ├── manutencoes/
│   └── financeiro/
├── routes/
└── main.tsx
```

## Estado de Servidor
TanStack Query é a fonte de verdade para dados remotos. Toda mutation invalida as queries relacionadas — por exemplo, criar um contrato invalida a lista de veículos disponíveis.

## Formulários
React Hook Form + Zod. Schemas Zod espelham a validação do Pydantic no backend (obrigatoriedade, tamanho, formato). Campos monetários são tratados com precisão decimal, nunca como `number` bruto (evita erro de ponto flutuante).

## Tabelas
TanStack Table para listagens de veículos, contratos e manutenções, com filtros básicos (status, período, veículo). Virtualização só é necessária se a lista passar de ~500 linhas visíveis simultaneamente.

## Fluxo-Chave: Nova Locação
A tela deve deixar claro, em tempo real, quais veículos estão disponíveis no período escolhido, e tratar o caso em que o veículo fica indisponível entre a consulta e o envio: o erro `409` do backend precisa de mensagem específica ("este veículo acabou de ser reservado por outra locação"), não um alerta genérico.

## Critérios de Aceite
Uma entrega frontend está pronta quando:

- integra com a API real;
- cobre loading, vazio, erro e sucesso;
- valida formulário com Zod, com valores monetários tratados com precisão;
- trata o conflito de disponibilidade de veículo com mensagem específica;
- é responsiva em desktop (uso interno da equipe) e utilizável em tablet/mobile para consulta rápida.
