# Requisitos Funcionais

## Objetivo

Este documento descreve todas as funcionalidades do sistema. Cada requisito funcional representa um comportamento esperado da aplicação.

---

# Convenção

Todos os requisitos serão identificados pelo padrão:

RF-XXX

Exemplo:

RF-001

RF-002

RF-003

---

# Módulo: Empresas

## RF-001

O sistema deve permitir o cadastro de empresas (locadoras).

---

## RF-002

Cada empresa deve possuir um identificador único (tenant).

---

## RF-003

Os dados de uma empresa nunca poderão ser acessados por outra empresa.

---

## RF-004

Cada empresa poderá possuir múltiplos usuários.

---

## RF-005

A empresa poderá configurar informações como:

- nome fantasia
- razão social
- CNPJ
- endereço
- telefone
- e-mail
- logotipo

---

# Módulo: Usuários

## RF-006

Permitir cadastro de usuários.

---

## RF-007

Permitir login utilizando e-mail e senha.

---

## RF-008

Permitir recuperação de senha.

---

## RF-009

Permitir alteração de senha.

---

## RF-010

Controlar permissões através de papéis (roles).

Exemplos:

- Administrador
- Gerente
- Financeiro
- Operador

---

# Módulo: Clientes

## RF-011

Cadastrar clientes pessoa física.

---

## RF-012

Cadastrar clientes pessoa jurídica.

---

## RF-013

Armazenar documentos.

---

## RF-014

Cadastrar múltiplos telefones.

---

## RF-015

Cadastrar múltiplos endereços.

---

## RF-016

Cadastrar condutores adicionais.

---

## RF-017

Consultar histórico completo de contratos.

---

## RF-018

Consultar histórico financeiro do cliente.

---

# Módulo: Veículos

## RF-019

Cadastrar veículos.

---

## RF-020

Controlar status:

- disponível
- alugado
- manutenção
- reservado
- vendido
- inativo

---

## RF-021

Registrar:

- placa
- RENAVAM
- chassi
- marca
- modelo
- ano
- cor
- combustível
- câmbio
- quilometragem

---

## RF-022

Registrar aquisição.

Campos:

- data
- valor pago
- fornecedor
- FIPE na aquisição

---

## RF-023

Registrar venda do veículo.

---

## RF-024

Consultar histórico completo do veículo.

---

## RF-025

Controlar documentação.

- IPVA
- licenciamento
- seguro

---

# Módulo: Contratos

## RF-026

Criar contratos.

---

## RF-027

Editar contratos enquanto não iniciados.

---

## RF-028

Encerrar contratos.

---

## RF-029

Cancelar contratos.

---

## RF-030

Registrar:

- veículo
- cliente
- usuários responsáveis
- datas
- caução
- valor
- forma de pagamento

---

## RF-031

Registrar quilometragem inicial.

---

## RF-032

Registrar quilometragem final.

---

## RF-033

Calcular automaticamente quilometragem percorrida.

---

## RF-034

Calcular excesso de quilometragem.

---

## RF-035

Registrar danos identificados na devolução.

---

# Módulo: Financeiro

## RF-036

Registrar receitas.

---

## RF-037

Registrar despesas.

---

## RF-038

Classificar despesas.

Exemplos:

- manutenção
- combustível
- seguro
- IPVA
- marketing
- folha

---

## RF-039

Controlar contas a pagar.

---

## RF-040

Controlar contas a receber.

---

## RF-041

Registrar pagamentos.

---

## RF-042

Registrar recebimentos.

---

## RF-043

Calcular lucro líquido.

---

## RF-044

Calcular fluxo de caixa.

---

# Módulo: Manutenção

## RF-045

Registrar manutenção preventiva.

---

## RF-046

Registrar manutenção corretiva.

---

## RF-047

Registrar:

- oficina
- fornecedor
- peças
- serviços
- quilometragem
- valor
- data

---

## RF-048

Consultar histórico completo de manutenção.

---

## RF-049

Emitir alertas de manutenção preventiva.

---

# Módulo: Dashboard

## RF-050

Exibir indicadores gerais.

---

## RF-051

Exibir lucro por veículo.

---

## RF-052

Exibir despesas por veículo.

---

## RF-053

Exibir receita mensal.

---

## RF-054

Exibir despesas mensais.

---

## RF-055

Exibir fluxo de caixa.

---

## RF-056

Exibir veículos mais rentáveis.

---

## RF-057

Exibir veículos com maior custo de manutenção.

---

## RF-058

Exibir taxa de ocupação da frota.

---

## RF-059

Calcular tempo estimado de payback por veículo.

---

# Módulo: Relatórios

## RF-060

Gerar relatórios em PDF.

---

## RF-061

Exportar dados para Excel.

---

## RF-062

Permitir filtros por período.

---

## RF-063

Permitir filtros por veículo.

---

## RF-064

Permitir filtros por cliente.

---

# Auditoria

## RF-065

Registrar todas as alterações relevantes.

---

## RF-066

Registrar:

- usuário
- data
- ação
- entidade alterada

---

# Notificações

## RF-067

Alertar contratos próximos do vencimento.

---

## RF-068

Alertar documentação vencida.

---

## RF-069

Alertar manutenção preventiva.

---

## RF-070

Alertar contas em atraso.

---

# Pesquisa

## RF-071

Permitir pesquisa global.

---

## RF-072

Permitir filtros avançados.

---

# Arquivos

## RF-073

Permitir upload de documentos.

---

## RF-074

Permitir upload de imagens.

---

# Segurança

## RF-075

Toda operação deve respeitar o tenant da empresa.

---

## RF-076

Toda operação deve verificar permissões do usuário.

---

# Requisitos Gerais

## RF-077

Todas as operações críticas deverão ser registradas em auditoria.

---

## RF-078

Nenhum dado poderá ser excluído fisicamente sem autorização explícita.

---

## RF-079

O sistema deverá utilizar exclusão lógica (Soft Delete) sempre que aplicável.

---

## RF-080

Todos os módulos deverão suportar paginação, ordenação e filtros.