# 02 · Modelo de Dados e Persistência

## Prompt de Alto Nível
Modele os dados para um sistema single-tenant (uma única empresa), com múltiplas filiais opcionais. Priorize integridade referencial, migrações seguras e uma regra inegociável: nenhum veículo pode estar em duas locações com período sobreposto.

Antes de criar ou alterar uma tabela, identifique: o ciclo de vida do registro, quem lê e quem escreve, e se a mudança afeta dinheiro ou disponibilidade de veículo.

## Metadados Padrão
Toda tabela de negócio deve ter:

| Campo | Tipo | Regra |
|---|---|---|
| `id` | UUID ou `SERIAL` | chave primária |
| `created_at` | `TIMESTAMPTZ` | default `now()` |
| `updated_at` | `TIMESTAMPTZ` | atualizado em toda escrita |
| `deleted_at` | `TIMESTAMPTZ` | soft delete, nullable |

`empresa_id`/RLS não é necessário — o sistema é single-tenant. Se houver múltiplas filiais, use `filial_id` como campo de negócio simples, sem políticas de isolamento tipo RLS.

## Módulos e Tabelas Sugeridas
- **Frota:** `veiculos` (placa, modelo, ano, status, km_atual, filial_id).
- **Clientes/Motoristas:** `clientes`, `motoristas`.
- **Contratos/Locações:** `contratos` (cliente_id, veiculo_id, motorista_id, data_inicio, data_fim_prevista, data_fim_real, status, valor_diaria, `version`), `contrato_eventos` (histórico de mudança de status).
- **Manutenções:** `manutencoes` (veiculo_id, tipo [preventiva/corretiva], data, km, custo, oficina, descricao, proxima_manutencao_km, proxima_manutencao_data).
- **Financeiro:** `pagamentos` (contrato_id, valor, data, status, metodo), `despesas` (veiculo_id opcional, categoria, valor, data).

## Prevenção de Dupla Alocação (regra crítica)
Use, em ordem de preferência:

1. **Constraint de exclusão no PostgreSQL** com `EXCLUDE USING gist` sobre `veiculo_id` e o intervalo `[data_inicio, data_fim_prevista)` — o banco recusa o overlap automaticamente:

```sql
ALTER TABLE contratos ADD CONSTRAINT contratos_sem_overlap
EXCLUDE USING gist (
  veiculo_id WITH =,
  tsrange(data_inicio, data_fim_prevista) WITH &&
) WHERE (status IN ('reservado', 'ativo'));
```

2. Se a constraint de exclusão não for viável no estágio atual, use concorrência otimista (coluna `version`) combinada com validação explícita de overlap na service layer, dentro da mesma transação.

Não dependa apenas de validação na aplicação sem nenhuma garantia no banco — é exatamente o cenário onde duas requisições simultâneas conseguem reservar o mesmo veículo.

## Migrações (Alembic)
- Toda mudança de schema é uma migration versionada.
- Migrações já aplicadas em produção não devem ser editadas — crie uma nova para corrigir.
- Para mudanças que quebram compatibilidade, use expand-and-contract: adicionar coluna nova, migrar dados, só então remover a antiga.

## Critérios de Aceite
Uma alteração de dados está pronta quando:

- tem migration (e downgrade quando fizer sentido);
- preserva soft delete e timestamps de auditoria;
- a prevenção de dupla alocação foi testada com concorrência real (duas requisições simultâneas contra o mesmo veículo/período);
- não usa `OFFSET` em listagens que podem crescer muito — prefira paginação por página+cursor simples desde já se o volume esperado for alto.
