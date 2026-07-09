# Locadora SaaS

Sistema de gestão para uma locadora de veículos gerenciar **frota**, **contratos/locações**, **manutenções** e **financeiro/receitas**. Aplicação single-tenant (uma empresa, com filiais opcionais) pensada para um time pequeno operar com segurança nos pontos que realmente importam: nunca alocar o mesmo veículo duas vezes, nunca perder precisão em dinheiro, e nunca deixar dado sensível vazar para quem não tem permissão.

Os documentos em [`docs/`](docs/) são a fonte de verdade do projeto — arquitetura, modelo de dados, segurança, testes e roadmap por fases. Este README cobre apenas "como rodar e usar".

## Módulos

| Módulo | O que cobre |
|---|---|
| **Frota** | Cadastro completo de veículos (aquisição, documentação, seguro), status, quilometragem, pneus, abastecimentos, indicadores por veículo, QR code + ficha/relatórios em PDF |
| **Clientes** | Dossiê completo (dados pessoais, CNH, financeiro, contato de emergência) — cobre também quem dirige, não só quem contrata |
| **Contratos / Locações** | Fluxo único reserva → ativo → devolução (ou cancelamento), com **prevenção real de dupla alocação**; checklist de entrega/devolução com assinatura digital |
| **Manutenções** | Histórico preventivo/corretivo por veículo, custo, oficina, e bloqueio automático do veículo enquanto em manutenção |
| **Financeiro** | Pagamentos (com estorno controlado), despesas, e relatório de rentabilidade por veículo |
| **Anexos** | Fotos, documentos e comprovantes vinculados a veículo/contrato/checklist, armazenados em storage de objetos (S3-compatível) |
| **Auditoria** | Timeline de alterações (`audit_logs`) por entidade — quem mudou o quê e quando |

## Stack

**Backend** — Python 3.12 · FastAPI · SQLAlchemy 2.0 · Alembic · Pydantic v2 · Pytest · PostgreSQL 16 · ReportLab (PDF) · qrcode · boto3 (storage S3-compatível)
**Frontend** — React 19 · TypeScript · Vite 8 · TanStack Query · React Hook Form + Zod · TanStack Table · Tailwind CSS v4 · Recharts

O Postgres e o storage de objetos podem ser locais (Docker Compose, default) ou apontar para um provedor gerenciado — ex.: **Supabase** para Postgres e **Supabase Storage** (S3-compatível) para arquivos, via as mesmas variáveis de ambiente (`DATABASE_URL`, `STORAGE_*`), sem nenhum código específico de provedor.

Arquitetura em 3 camadas no backend (`api` → `services` → `models`), sem Hexagonal/DDD tático — ver [`docs/01-ARQUITETURA.md`](docs/01-ARQUITETURA.md) para a justificativa. Frontend feature-driven — ver [`docs/05-FRONTEND.md`](docs/05-FRONTEND.md).

## Pré-requisitos

- **Opção A — Docker:** Docker Desktop com Docker Compose v2.
- **Opção B — Local (sem Docker):** Python 3.12+, Node.js 22+, PostgreSQL 16+.

## Rodando com Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

- Backend (Swagger): http://localhost:8000/docs
- Frontend: http://localhost:5173
- PostgreSQL fica disponível em `localhost:5432` (usuário/senha/database: `locadora`)

O `docker compose up` já sobe o Postgres, mas **as migrações e o usuário admin não rodam automaticamente** — depois do primeiro `up`, rode:

```bash
docker compose exec backend alembic upgrade head
docker compose exec backend python create_admin.py admin@locadora.com "senha-forte" "Administrador"
```

## Rodando sem Docker

### 1. Banco de dados

Suba um PostgreSQL 16 local (pode ser via instalador oficial, `winget install PostgreSQL.PostgreSQL.16` no Windows, ou um container avulso) e crie o usuário/bancos:

```sql
CREATE USER locadora WITH PASSWORD 'locadora' CREATEDB;
CREATE DATABASE locadora OWNER locadora;
CREATE DATABASE locadora_test OWNER locadora;  -- usado pelos testes automatizados
```

> A extensão `btree_gist` (necessária para a trava anti-dupla-reserva) é habilitada automaticamente pela migração — não precisa criar manualmente.

### 2. Backend

```bash
cd backend
python -m venv .venv
.venv/Scripts/activate        # Windows — use `source .venv/bin/activate` no Linux/Mac
pip install -r requirements.txt

cp ../.env.example .env       # ajuste DATABASE_URL se necessário
alembic upgrade head
python create_admin.py admin@locadora.com "senha-forte" "Administrador"

uvicorn app.main:app --reload --port 8000
```

Swagger em http://127.0.0.1:8000/docs.

> **Windows:** use `127.0.0.1` em vez de `localhost` ao testar a API — em algumas máquinas `localhost` resolve para `::1` e pode cair em outro serviço já ocupando a porta.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env          # já aponta para http://localhost:8000/api/v1
npm run dev
```

Aplicação em http://localhost:5173. Faça login com o usuário admin criado no passo 2.

## Populando dados de teste

Além do `create_admin.py`, há um seed completo para desenvolvimento — centenas de clientes/veículos/contratos, milhares de leituras de quilometragem, manutenções, alertas e checklists, cobrindo os principais cenários (contratos vencendo, veículos acima da franquia de km, manutenções atrasadas etc.):

```bash
cd backend
python scripts/seed_dev_data.py --reset --yes
```

Recusa rodar fora de um Postgres local (nunca contra produção) e é reexecutável — ver [`docs/10-SEED-DESENVOLVIMENTO.md`](docs/10-SEED-DESENVOLVIMENTO.md) para as flags e o racional.

## Variáveis de ambiente

| Variável | Onde é usada | Descrição |
|---|---|---|
| `DATABASE_URL` | backend | String de conexão SQLAlchemy/psycopg com o Postgres |
| `JWT_SECRET_KEY` | backend | Chave de assinatura dos tokens — **troque em produção** |
| `JWT_ALGORITHM` | backend | Algoritmo JWT (default `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | backend | Validade do access token |
| `REFRESH_TOKEN_EXPIRE_DAYS` | backend | Validade do refresh token |
| `ENVIRONMENT` | backend | `development` / `production` |
| `CORS_ORIGINS` | backend | Origens permitidas, separadas por vírgula |
| `FRONTEND_BASE_URL` | backend | URL pública do frontend — usada para montar o link do QR code do veículo |
| `STORAGE_ENDPOINT` | backend | Endpoint S3-compatível — nenhum provedor vem pronto no `docker-compose.yml`; aponte para Supabase Storage ou um MinIO próprio |
| `STORAGE_ACCESS_KEY` | backend | Access key do storage |
| `STORAGE_SECRET_KEY` | backend | Secret key do storage |
| `STORAGE_REGION` | backend | Região exigida pelo provedor (Supabase exige a região real do projeto; MinIO aceita qualquer valor) |
| `VITE_API_BASE_URL` | frontend | URL base da API consumida pelo frontend |

### Usando um Postgres/Storage externos (ex.: Supabase) em vez do local

`docker-compose.yml` lê `DATABASE_URL` e `STORAGE_*` como variáveis (`${DATABASE_URL:-...}`), com o Postgres local do Compose como default. Para apontar para um provedor externo sem tocar no arquivo versionado, crie um `.env` na raiz do repo (já coberto pelo `.gitignore`) com os valores reais:

```bash
DATABASE_URL=postgresql+psycopg://usuario:senha@host:porta/banco
STORAGE_ENDPOINT=https://<projeto>.storage.supabase.co/storage/v1/s3
STORAGE_ACCESS_KEY=...
STORAGE_SECRET_KEY=...
STORAGE_REGION=...
```

`docker compose up -d` passa a usar esses valores automaticamente. Sem esse arquivo, tudo roda 100% local (Postgres do Compose, storage indisponível — os endpoints de anexo ficam sem efeito, mas o resto da API funciona normalmente).

## Papéis e permissões (RBAC)

| Papel | Pode fazer |
|---|---|
| `administrador` | Tudo |
| `operador` | Frota (editar, regenerar QR), clientes, contratos (emitir/cancelar), checklists, anexos, auditoria, visualizar manutenções |
| `financeiro` | Visualizar frota/contratos/anexos, lançar pagamentos/despesas, aprovar estornos |
| `mecanico` | Visualizar frota, registrar manutenções, enviar anexos, visualizar checklists |

Autorização é sempre checada no backend (`Depends(require_permission("modulo:acao"))`); o frontend só esconde ações que o usuário não pode executar — ver [`docs/03-AUTENTICACAO-AUTORIZACAO.md`](docs/03-AUTENTICACAO-AUTORIZACAO.md).

## A regra mais importante do sistema

Nenhum veículo pode ser alocado a dois contratos com período sobreposto — isso é garantido por uma **constraint de exclusão no PostgreSQL** (`contratos_sem_overlap`, `EXCLUDE USING gist`), não apenas por validação em código. Duas requisições simultâneas tentando reservar o mesmo veículo: o banco aceita uma e rejeita a outra com `409 VEICULO_INDISPONIVEL`, mesmo sob concorrência real.

Isso é coberto por um teste automatizado com threads reais e conexões independentes: `backend/tests/test_contratos_concorrencia.py`.

## Testes

**Backend** (precisa do Postgres rodando e do banco `locadora_test` criado):
```bash
cd backend
pytest -v
```

**Frontend**:
```bash
cd frontend
npm run typecheck
npm run lint
npm run build
```

## Estrutura do repositório

```
.
├── docs/                          # Arquitetura, modelo de dados, segurança, roadmap (fonte de verdade)
├── backend/
│   ├── app/
│   │   ├── api/                   # Routers FastAPI (1 arquivo por módulo de negócio)
│   │   ├── services/              # Regras de negócio e transações (inclui pdf_service, qrcode_service)
│   │   ├── models/                # SQLAlchemy (entidades + metadados de auditoria)
│   │   ├── schemas/                # Pydantic (entrada/saída de cada endpoint)
│   │   ├── static/                 # Logo usado no cabeçalho dos PDFs
│   │   └── core/                  # config, database, security, permissions, deps, storage (S3), audit
│   ├── migrations/                # Alembic (schema inicial incluindo a trava anti-overlap)
│   ├── scripts/                   # sync_requirements.py — gera requirements.txt a partir de pyproject.toml
│   ├── tests/                     # pytest — concorrência, fluxo de contrato, financeiro, auth, anexos, checklists
│   └── create_admin.py            # Script para criar o primeiro usuário administrador
├── frontend/
│   └── src/
│       ├── core/                  # api client, auth (contexto + RBAC no cliente), providers
│       ├── components/ui/         # Button, DataTable, PaginationControls, States...
│       ├── components/shared/     # FileUpload, SignaturePad, Layout
│       ├── features/              # frota, cadastros (clientes), contratos, checklists, manutencoes, financeiro
│       └── routes/                # Proteção de rota autenticada
└── docker-compose.yml             # Postgres + backend + frontend para ambiente local
```

> **Dependências do backend:** existem dois arquivos (`pyproject.toml`, usado por deploys via `uv`, e `requirements.txt`, usado por `pip` local) que precisam ficar sincronizados manualmente. Depois de editar `pyproject.toml`, rode `python backend/scripts/sync_requirements.py` para regenerar o `requirements.txt` (ou `--check` para só validar).

## Roadmap

O projeto é executado por fases curtas e entregáveis — ver [`docs/09-ROADMAP-FASES.md`](docs/09-ROADMAP-FASES.md). Estado atual: **Fases 0 a 3 concluídas** (fundação, CRUD, fluxo completo de locação/manutenção/financeiro), mais uma fase avançada de Frota entregue fora da sequência original: QR code + impressão/exportação em PDF, auditoria (timeline de alterações), checklist de entrega/devolução com assinatura digital, e anexos via storage S3-compatível. A entidade Motorista foi removida — Cliente cobre também quem dirige o veículo.

## Solução de problemas

- **`ModuleNotFoundError: email_validator`** ao importar o backend → `pip install email-validator` (já está no `requirements.txt`; reinstale as dependências).
- **Alias `@/...` não resolve no `npm run dev`** → confirme que `frontend/vite.config.ts` tem `resolve.alias` apontando `@` para `./src`; rode `rm -rf node_modules/.vite` e reinicie o dev server.
- **`localhost` cai em outro serviço na porta 8000/5173** → use `127.0.0.1` explicitamente, ou libere a porta (`netstat -ano | findstr :8000` no Windows).
- **Erro de constraint `contratos_sem_overlap` não existe** → rode `alembic upgrade head`; a extensão `btree_gist` e a constraint são criadas na migração `0001`.
- **Testes do backend falhando por dado duplicado** → confirme que o banco `locadora_test` existe e está limpo; os testes recriam o schema a cada sessão de execução.
