# 10 · Seed de Dados para Desenvolvimento

## Prompt de Alto Nível
Popule o banco de desenvolvimento com um único comando, sem depender de cadastro manual, mantendo toda a integridade referencial e reaproveitando os `services/` já existentes em vez de reimplementar regra de negócio.

## Como rodar

O script recusa rodar contra qualquer banco cujo host não seja `localhost`, `127.0.0.1` ou `db` (serviço do `docker-compose`) — **nunca roda contra produção**, mesmo que `DATABASE_URL` esteja configurada para isso no seu `.env`.

Rodando via `docker-compose` (recomendado — evita a ambiguidade de `localhost:5432` poder resolver tanto para o Postgres do compose quanto para um Postgres nativo eventualmente instalado na máquina):

```bash
docker compose run --rm \
  -e DATABASE_URL=postgresql+psycopg://locadora:locadora@db:5432/locadora \
  backend python scripts/seed_dev_data.py --reset --yes
```

> O `.env` na raiz do repo normalmente já sobrescreve `DATABASE_URL` do `docker-compose.yml` (para apontar o backend local a um Postgres externo, ex.: Supabase) — por isso é preciso passar `-e DATABASE_URL=...` explicitamente apontando para `db:5432` na chamada acima, mesmo rodando dentro do compose.

Rodando localmente (fora do Docker), contra um Postgres que você tenha certeza ser de desenvolvimento:

```bash
cd backend
python scripts/seed_dev_data.py --reset --yes
```

### Flags

| Flag | Efeito |
|---|---|
| `--reset` | apaga (`TRUNCATE ... CASCADE`) todas as tabelas da aplicação antes de semear. Sem essa flag, o script recusa rodar se detectar dados de um seed anterior (usuários com e-mail `@devseed.local`) — rode com `--reset` para recriar do zero. |
| `--yes` | pula a confirmação interativa do guard de ambiente (útil em scripts não interativos). |
| `--com-uploads` | habilita upload real de fotos/assinaturas fictícias via `attachment_service` (Supabase Storage) para um subconjunto de itens de checklist. **Desabilitado por padrão** — só habilite depois de confirmar que o bucket do seu `.env` é de desenvolvimento, não o de produção. |

## O que é gerado

Usuários (30, papéis variados, senha `DevSeed@123`, e-mails `@devseed.local`), clientes (~300), veículos (~250, nas 9 situações possíveis), contratos (ativos/encerrados/cancelados/reservados/futuros), leituras de quilometragem (milhares, série temporal coerente por veículo), manutenções e planos de manutenção preventiva (com exemplos deliberados em `normal`/`atenção`/`crítico`), pneus, abastecimentos, multas, sinistros, danos, despesas, pagamentos e checklists de entrega/devolução (alguns contratos ficam de propósito sem checklist de devolução, e alguns veículos acima da franquia de km contratada).

## Arquitetura

`backend/app/seed/` — um módulo por domínio (`clientes.py`, `veiculos.py`, `contratos.py`, `checklists.py` etc.), cada um consumindo o `service` real correspondente (`contrato_service`, `checklist_service`, `manutencao_service`...) para garantir que o seed respeita as mesmas regras de negócio da aplicação (constraint de sobreposição de contrato, sequência entrega→devolução do checklist, atualização de `veiculo.status`/`km_atual`). As exceções são `leituras_km` e `vehicle_tracking`, que usam `INSERT` em lote direto via ORM — são tabelas de alto volume onde a regra é trivial de replicar e o custo de milhares de round-trips individuais não compensa.

`backend/app/seed/guard.py` é o guard de segurança: allowlist de host (não confia em `settings.environment`, que nada no deploy define como `"production"`) + confirmação interativa antes de qualquer escrita.

`backend/scripts/seed_dev_data.py` é o CLI fino que orquestra guard → (reset opcional) → `app.seed.runner.rodar_seed`.

## Idempotência

Sem `--reset`, o script verifica se já existe algum usuário com e-mail `@devseed.local` e aborta se sim — evita duplicar dados ao rodar duas vezes por engano. `--reset` sempre recria do zero.
