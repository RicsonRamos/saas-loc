# 08 · Testes e Qualidade

## Prompt de Alto Nível
Teste o que pode realmente causar dor: dupla alocação de veículo, cálculo financeiro errado e fluxo de contrato quebrado. Não persiga cobertura alta por si só — persiga confiança nos fluxos críticos.

## Pirâmide de Testes (orientativa)
```text
E2E (Playwright)         — poucos, só os fluxos mais críticos
                           (criar locação, registrar devolução, lançar pagamento)
Testes de API/integração — regras de negócio e contrato de endpoints
Testes unitários         — cálculos e validações
```

## Testes Obrigatórios

### Concorrência de Alocação de Veículo
Duas requisições simultâneas tentando reservar o mesmo veículo no mesmo período: apenas uma deve vencer, a outra recebe `409`. Este é o teste não-negociável do projeto.

### Financeiro
- Uso de `Decimal` em todos os cálculos de valor.
- Estorno duplicado é bloqueado.
- Valores negativos/zero tratados conforme a regra de negócio.

### Contratos/Locações
- Fluxo completo: reserva → contrato → devolução muda o status do veículo corretamente.
- Cancelamento libera o veículo para nova locação.

### Manutenções
- Registrar manutenção corretiva/preventiva atualiza o status do veículo quando aplicável (ex.: veículo em manutenção não pode ser reservado).

### Autorização
- Usuário sem permissão recebe `403` nas rotas críticas.

## Qualidade Estática
`ruff`/`eslint` no CI. Cobertura é acompanhada, mas não é um gate bloqueante rígido — priorize que os testes acima existam e sejam confiáveis, em vez de perseguir um número de cobertura.

## Critérios de Aceite
Uma entrega está validada quando:

- o teste de concorrência de veículo existe e passa;
- o fluxo de contrato ponta a ponta está testado;
- os cálculos financeiros estão testados com `Decimal`;
- o CI está verde no PR.
