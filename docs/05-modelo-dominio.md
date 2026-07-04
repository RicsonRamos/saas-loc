# Modelo de Domínio

## Objetivo

Definir o domínio de negócio da aplicação.

Este documento representa a linguagem ubíqua do sistema e serve como referência para implementação das regras de negócio.

O domínio não possui qualquer dependência de banco de dados ou framework.

---

# Bounded Contexts

O sistema é dividido nos seguintes contextos:

- Empresa
- Usuários
- Clientes
- Frota
- Contratos
- Financeiro
- Manutenção
- Documentos
- Dashboard
- Auditoria
- Notificações

Cada contexto deve possuir baixo acoplamento e alta coesão.

---

# Agregados

## Empresa

Aggregate Root

Responsabilidades:

- representar uma locadora
- configurar parâmetros do sistema
- controlar usuários
- definir plano contratado

---

## Usuário

Aggregate Root

Responsabilidades:

- autenticação
- autorização
- operações administrativas

---

## Cliente

Aggregate Root

Responsabilidades:

- representar o locatário
- armazenar documentação
- manter histórico contratual

---

## Veículo

Aggregate Root

Responsabilidades:

- representar um ativo da empresa
- controlar disponibilidade
- controlar quilometragem
- controlar documentação
- controlar rentabilidade

---

## Contrato

Aggregate Root

Responsabilidades:

- representar uma locação
- controlar período
- controlar valores
- controlar devolução
- controlar pagamentos

---

## Manutenção

Aggregate Root

Responsabilidades:

- registrar intervenções
- controlar custos
- controlar histórico

---

## Despesa

Aggregate Root

Responsabilidades:

- registrar gastos
- classificar custos
- compor fluxo financeiro

---

## Receita

Aggregate Root

Responsabilidades:

- registrar entradas financeiras
- compor fluxo de caixa

---

## Documento

Aggregate Root

Responsabilidades:

- representar arquivos enviados
- controlar metadados
- associar documentos às entidades

---

# Value Objects

Não possuem identidade.

Exemplos:

Endereço

Nome

Telefone

Email

CPF

CNPJ

CNH

Placa

Chassi

RENAVAM

Dinheiro

Período

Quilometragem

---

# Entidades

Empresa

↓

Usuário

↓

Cliente

↓

Contrato

↓

Veículo

↓

Manutenção

↓

Receita

↓

Despesa

↓

Documento

---

# Regras Gerais

Toda entidade pertence a uma empresa.

Toda operação possui usuário responsável.

Toda alteração relevante gera auditoria.

Toda entidade possui ciclo de vida.

Nenhuma entidade conhece detalhes de persistência.

---

# Estados

## Veículo

Disponível

Reservado

Locado

Manutenção

Inativo

Vendido

---

## Contrato

Rascunho

Ativo

Encerrado

Cancelado

Inadimplente

---

## Pagamento

Pendente

Pago

Vencido

Cancelado

---

# Regras de Negócio

Um veículo não pode possuir dois contratos ativos.

Um contrato deve possuir exatamente um cliente.

Um contrato deve possuir exatamente um veículo.

Uma manutenção sempre pertence a um veículo.

Uma despesa pode ou não estar vinculada a um veículo.

Receitas podem existir independentemente de contratos.

Nenhuma operação pode acessar dados de outra empresa.

---

# Serviços de Domínio

Cálculo de lucro.

Cálculo de rentabilidade.

Cálculo de payback.

Cálculo de ocupação.

Cálculo de quilometragem.

Cálculo financeiro.

---

# Eventos de Domínio (Futuro)

ContratoCriado

ContratoEncerrado

VeiculoLocado

VeiculoDevolvido

ManutencaoRegistrada

PagamentoRecebido

DocumentoVencido

---

# Princípios

O domínio representa apenas regras de negócio.

Nenhuma entidade conhece banco de dados.

Nenhuma entidade conhece Spring.

Nenhuma entidade conhece HTTP.

O domínio deve ser puro.