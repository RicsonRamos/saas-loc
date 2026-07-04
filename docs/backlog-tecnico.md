## Backlog técnico do MVP (ordem de execução)

Aqui o objetivo muda: sair de documentação e ir para implementação incremental sem criar um sistema “grande demais antes de funcionar”.

---

# EPIC 0 — Base do projeto

Objetivo: preparar estrutura mínima do SaaS.

Histórias:

* Criar repositório backend (Spring Boot)
* Criar repositório frontend (React + TypeScript)
* Configurar Docker Compose (backend, frontend, postgres)
* Configurar PostgreSQL com schema inicial
* Configurar Flyway
* Criar estrutura multi-tenant base (tenant_id em tudo)
* Criar autenticação base (JWT)

Entregável:
Sistema sobe local com login funcionando.

---

# EPIC 1 — Autenticação e multi-tenant

Objetivo: garantir isolamento e segurança base.

Histórias:

* Cadastro de empresa (tenant)
* Cadastro de usuário por empresa
* Login JWT
* Refresh token
* RBAC básico (admin, operador)
* Middleware de tenant resolution
* Filtro obrigatório de tenant em todas queries

Entregável:
Usuário loga e já está isolado por empresa.

---

# EPIC 2 — Cadastro de clientes

Objetivo: primeiro módulo de negócio real.

Histórias:

* CRUD de clientes
* Validação CPF/CNPJ
* Histórico de contratos por cliente
* Upload de documentos (CNH, etc)
* Busca e filtros

Entregável:
Sistema já começa a ser utilizável.

---

# EPIC 3 — Frota (veículos)

Objetivo: núcleo do produto.

Histórias:

* CRUD de veículos
* Status do veículo (disponível, alugado, manutenção)
* Registro de compra (FIPE vs preço pago)
* Quilometragem atual
* Histórico do veículo
* Upload de documentos do veículo

Entregável:
Controle de frota funcional.

---

# EPIC 4 — Contratos

Objetivo: core financeiro-operacional.

Histórias:

* Criar contrato
* Vincular cliente + veículo
* Definir período
* Definir valores e caução
* Controle de status do contrato
* Controle de km inicial e final
* Cálculo de km excedente
* Encerramento de contrato

Entregável:
Sistema já opera como locadora real.

---

# EPIC 5 — Financeiro básico

Objetivo: controle de dinheiro.

Histórias:

* Registro de receitas
* Registro de despesas
* Categorias financeiras
* Fluxo de caixa simples
* Lucro básico
* Relatório mensal

Entregável:
Visão financeira inicial.

---

# EPIC 6 — Manutenção

Objetivo: custo operacional.

Histórias:

* Registro de manutenção
* Tipos (preventiva/corretiva)
* Custo por veículo
* Histórico de manutenção
* Alertas básicos (km ou tempo)

Entregável:
Controle de custo da frota.

---

# EPIC 7 — Dashboard

Objetivo: valor percebido.

Histórias:

* Receita total
* Despesa total
* Lucro líquido
* Lucro por veículo
* Veículos mais rentáveis
* Taxa de ocupação
* Payback estimado

Entregável:
Produto deixa de parecer “CRUD”.

---

# EPIC 8 — Relatórios

Objetivo: exportação de dados.

Histórias:

* Exportar PDF
* Exportar Excel
* Relatórios por período
* Relatórios por veículo
* Relatórios por cliente

Entregável:
Uso empresarial real.

---

# EPIC 9 — Segurança e auditoria reforçada

Objetivo: preparar para produção.

Histórias:

* Auditoria completa de ações
* Logs estruturados
* Rate limiting
* Bloqueio de tentativas de login
* Revisão de permissões
* Hardening de API

Entregável:
Sistema pronto para produção.

---

# EPIC 10 — Infraestrutura e deploy

Objetivo: colocar em produção real.

Histórias:

* Deploy em VPS
* NGINX reverse proxy
* HTTPS (certbot)
* CI/CD GitHub Actions
* Backup automático
* Monitoramento básico

Entregável:
Sistema SaaS rodando em produção.

---

# Ordem REAL de execução (crítica)

1. EPIC 0
2. EPIC 1
3. EPIC 3
4. EPIC 2
5. EPIC 4
6. EPIC 5
7. EPIC 6
8. EPIC 7
9. EPIC 8
10. EPIC 9
11. EPIC 10

---

# Observação importante (realidade do projeto)

Se você não seguir essa ordem, o projeto vai falhar por um motivo simples:

* tentar fazer dashboard antes de ter dados reais
* tentar fazer financeiro antes de contratos
* tentar escalar antes de ter produto

Isso é o erro clássico de SaaS iniciante: construir “sistema bonito” sem fluxo operacional real.

---