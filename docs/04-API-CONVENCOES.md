# 04 · API — Convenções REST

## Prompt de Alto Nível
Desenhe APIs REST previsíveis e simples. Prefira convenção sobre configuração; não adicione recursos (versionamento elaborado, HATEOAS, GraphQL) que o projeto não pede.

Não crie endpoint sem schema Pydantic de entrada/saída e sem checagem explícita de permissão.

## Convenções Globais
- Prefixo `/api/v1/`.
- Payloads em `application/json`, campos em `snake_case`.
- Datas em ISO 8601 UTC, ex.: `2026-07-06T15:30:00Z`.
- Erros no formato Problem Details (RFC 9457): `type`, `title`, `status`, `detail`, `code`.

## Design de Recursos
| Método | Uso |
|---|---|
| `GET` | leitura |
| `POST` | criação |
| `PUT`/`PATCH` | atualização total/parcial |
| `DELETE` | remoção lógica |

Exemplos:

- `GET /api/v1/veiculos`
- `POST /api/v1/contratos`
- `PATCH /api/v1/contratos/{contrato_id}/devolucao`
- `POST /api/v1/manutencoes`

## Paginação
Listagens que podem crescer (contratos, manutenções, pagamentos) usam paginação por página + limite desde o início. Migre para cursor apenas se o volume real de dados exigir — não otimize prematuramente.

## Idempotência
Endpoints que criam contrato ou lançam pagamento devem aceitar um `Idempotency-Key` opcional para evitar duplo clique/duplo submit. Implementação simples (tabela com chave única e TTL de algumas horas) é suficiente — não é necessário Redis se o volume for baixo.

## Erros Padronizados
```json
{
  "type": "https://app.locadora.com/problems/veiculo-indisponivel",
  "title": "Veículo indisponível",
  "status": 409,
  "detail": "O veículo selecionado já está reservado para o período informado.",
  "code": "VEICULO_INDISPONIVEL"
}
```

Erros de validação incluem ponteiro para o campo:

```json
{
  "type": "https://app.locadora.com/problems/validation-error",
  "title": "Payload inválido",
  "status": 422,
  "errors": [
    { "pointer": "/data_inicio", "detail": "A data inicial deve ser anterior à data final." }
  ]
}
```

## Critérios de Aceite
Uma API está pronta quando:

- possui schemas Pydantic de entrada e saída;
- valida permissão antes de executar a ação;
- usa paginação em listagens que podem crescer;
- protege criação de contrato/pagamento contra duplo submit;
- retorna erros no formato Problem Details;
- tem teste de contrato (caminho feliz + erro principal) para o endpoint.
