# 03 · Autenticação e Autorização

## Prompt de Alto Nível
Implemente autenticação simples e autorização baseada em papéis (RBAC). Não implemente SSO corporativo, ABAC multi-atributo ou isolamento multi-tenant — não há necessidade disso em um sistema de uma única empresa.

## Autenticação
- JWT emitido pelo próprio backend (ou Supabase Auth, se o banco já for Supabase) com expiração curta + refresh token.
- Senhas com hash forte (bcrypt ou argon2).
- Bloqueio de usuário inativo ou desligado.

## Papéis (RBAC)
Papéis sugeridos: Administrador, Operador (frota/contratos), Financeiro, Mecânico/Manutenção (se houver tela própria para oficina interna).

Permissão no padrão `modulo:acao`, por exemplo:

- `frota:editar`;
- `contratos:emitir`;
- `contratos:cancelar`;
- `manutencoes:registrar`;
- `financeiro:aprovar_estorno`.

Autorização é checada no backend via dependency do FastAPI (`Depends(require_permission("frota:editar"))`), nunca apenas escondendo o botão no frontend.

## Auditoria Mínima
Registre em log: login falho, criação/cancelamento de contrato, lançamento financeiro, alteração de permissão de usuário. Não registre senha, token ou dado de pagamento completo.

## Critérios de Aceite
- Nenhum endpoint de escrita crítico (contratos, financeiro) roda sem checar permissão.
- Existe teste de "usuário sem permissão recebe 403".
- Logs de auditoria não expõem segredo nem dado sensível completo.
