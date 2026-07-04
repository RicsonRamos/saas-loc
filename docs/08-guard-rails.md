# Guard Rails

## Objetivo

Este documento define regras obrigatórias para desenvolvedores e ferramentas de IA.

Estas regras possuem prioridade sobre preferências individuais.

Seu objetivo é manter consistência arquitetural durante toda a vida do projeto.

---

# Arquitetura

Sempre seguir a arquitetura definida em arquitetura.md.

Não alterar a arquitetura sem ADR.

Não criar novos padrões.

---

# Código

Escrever código simples.

Preferir clareza.

Evitar abstrações prematuras.

Evitar otimizações prematuras.

---

# Controllers

Controllers apenas:

- recebem requisições
- validam DTOs
- chamam Services
- retornam Responses

Nunca colocar regra de negócio.

Nunca acessar Repository.

---

# Services

Toda regra de negócio pertence aos Services ou Domain Services.

Services podem utilizar múltiplos Repositories.

---

# Repositories

Repositories possuem apenas responsabilidade de persistência.

Nunca realizar:

- validações
- cálculos
- regras de negócio

---

# DTOs

Nunca expor entidades JPA.

Toda API utiliza DTOs.

Nunca reutilizar Entity como Request ou Response.

---

# Banco

Nunca escrever SQL concatenado.

Nunca utilizar SELECT *.

Sempre utilizar paginação.

Toda migration deverá utilizar Flyway.

Nunca alterar banco manualmente.

---

# Multi-Tenant

Toda entidade possui tenant_id.

Toda consulta filtra tenant_id.

Nunca permitir acesso cruzado.

Nunca confiar no tenant enviado pelo frontend.

---

# Segurança

Nunca desabilitar autenticação para facilitar testes.

Nunca remover validações.

Nunca registrar dados sensíveis.

Nunca criar endpoints públicos sem documentação.

---

# Exceções

Utilizar Exception Handler Global.

Nunca utilizar try/catch desnecessário.

Nunca ocultar erros silenciosamente.

---

# Logs

Registrar apenas informações úteis.

Nunca registrar:

- senha
- token
- documentos
- cartão
- SQL completo

---

# Dependências

Não adicionar bibliotecas sem justificativa.

Preferir bibliotecas já utilizadas.

Evitar duplicidade de responsabilidades.

---

# Testes

Toda regra de negócio deve possuir testes.

Todo bug corrigido deve gerar teste.

Não reduzir cobertura.

---

# Performance

Evitar consultas N+1.

Utilizar Lazy Loading quando apropriado.

Paginação obrigatória.

Evitar processamento desnecessário.

---

# Organização

Cada módulo é independente.

Não criar dependências circulares.

Não acessar classes internas de outros módulos.

Comunicação apenas através de interfaces públicas.

---

# Convenções

Utilizar nomenclatura consistente.

Classes:

PascalCase

Métodos:

camelCase

Constantes:

UPPER_CASE

Pacotes:

lowercase

---

# IA

Ao gerar código:

Seguir arquitetura existente.

Não inventar padrões.

Não alterar estrutura do projeto.

Não substituir bibliotecas oficiais.

Não criar código não solicitado.

Não remover comentários importantes.

Não modificar comportamento existente sem justificativa.

Sempre reutilizar componentes existentes antes de criar novos.

---

# Refatoração

Não realizar grandes refatorações junto com novas funcionalidades.

Uma Pull Request deve possuir apenas um objetivo.

---

# Documentação

Toda decisão arquitetural deve possuir documentação.

Toda alteração estrutural deve atualizar a documentação.

---

# Commits

Cada commit deve possuir apenas um propósito.

Mensagens claras.

Commits pequenos.

---

# Pull Requests

Pequenas.

Objetivas.

Com testes.

Sem código morto.

Sem arquivos desnecessários.

---

# Princípio Final

Sempre escolher a solução mais simples que atenda corretamente ao requisito.

Quando houver dúvida entre duas soluções equivalentes:

Escolher a mais simples.

Quando houver conflito entre velocidade e qualidade:

Priorizar qualidade.

Quando houver conflito entre conveniência e segurança:

Priorizar segurança.

Nenhum código será aceito se violar qualquer regra deste documento.