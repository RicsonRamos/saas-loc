# 09 · Roadmap por Fases

## Prompt de Alto Nível
Execute o projeto por fases curtas e entregáveis. Os módulos de Frota, Contratos/Locações, Manutenções e Financeiro evoluem juntos desde o início — o cliente precisa ver o conjunto funcionando cedo, não um único módulo isolado e perfeito.

Quando receber uma tarefa, identifique a fase correspondente. Se pertencer a uma fase futura, proponha apenas o que for compatível com a fase atual.

## Fase 0 — Fundação
- Setup do backend (FastAPI + SQLAlchemy + Alembic) e do frontend (Vite + React).
- Autenticação simples (login, JWT, RBAC básico).
- CI com lint + testes.

**Gate:** login funciona, CI verde, deploy manual em produção funcionando (ainda que vazio).

## Fase 1 — Cadastros Base + Esqueleto dos 4 Módulos
- CRUD de veículos, clientes e motoristas.
- Telas e endpoints básicos — ainda sem regra de negócio complexa — para Frota, Contratos, Manutenções e Financeiro, cada um com listagem, criação e edição simples.

**Gate:** os 4 módulos existem com CRUD funcionando; time e cliente já conseguem navegar pelo sistema de ponta a ponta.

## Fase 2 — Fluxo de Locação Completo
- Reserva → contrato → devolução, com atualização de status do veículo.
- Prevenção de dupla alocação (constraint no banco + teste de concorrência).
- Registro de manutenção vinculado ao veículo, bloqueando locação se o veículo estiver em manutenção.

**Gate:** teste de concorrência de veículo passa; fluxo completo de locação testado ponta a ponta.

## Fase 3 — Financeiro e Receitas
- Lançamento de pagamentos vinculados a contratos.
- Despesas (incluindo custo de manutenção) por veículo.
- Relatório simples de receita x despesa por veículo/período.

**Gate:** valores batem, testados com `Decimal`; relatório básico de rentabilidade funciona.

## Fase 4 — Alertas e Relatórios
- Alerta de manutenção preventiva por km ou data.
- Dashboard com indicadores: veículos disponíveis, contratos ativos, receita do mês, manutenções pendentes.

**Gate:** alertas de manutenção disparam corretamente; dashboard reflete dados reais.

## Fase 5 — Operação em Produção
- Backup automático testado com restore.
- Ajustes de performance conforme uso real (não antecipado).
- Runbook simples: "o que fazer quando algo quebra".

**Gate:** restore de backup testado; sistema em uso real pelo cliente.

## Política de Mudança de Fase
Se surgir uma demanda de fase futura antes da hora, registre como backlog e entregue apenas o que for compatível com a fase atual. Mas não trave por burocracia: o objetivo aqui é velocidade com segurança nos pontos críticos (dinheiro e disponibilidade de veículo), não processo pesado.

## Fase 6 — Frota Avançada (entregue fora da sequência original)
Demanda direta do cliente para o módulo de Frota, entregue em paralelo às fases acima:

- QR code por veículo (`codigo_publico` regenerável) + página pública de consulta sem autenticação.
- Impressão de ficha e exportação de relatórios (histórico, abastecimentos, manutenções) em PDF.
- Auditoria: tabela `audit_logs` + timeline de alterações por entidade, instrumentada nos services de veículo, pneu, abastecimento e contrato.
- Checklist de entrega/devolução com assinatura digital (canvas), armazenada como anexo.
- Anexos (fotos, documentos) via storage S3-compatível (MinIO local ou Supabase Storage), com referência polimórfica no banco.
- `vehicle_tracking`: apenas schema preparado para integração futura com GPS — sem tela nem endpoint.
- Motorista removido: Cliente já cobria CNH completa, então a entidade separada e a tela de condutores adicionais foram descontinuadas.

**Gate:** suíte de testes cobrindo os fluxos acima (upload/download real de anexo, checklist com regra de contrato ativo, rota pública sem token) passando; validado contra Postgres/Storage do Supabase, não só ambiente local.
