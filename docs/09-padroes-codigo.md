# Padrões de Código

## Objetivo

Definir o padrão oficial de desenvolvimento.

Todo código desenvolvido deverá seguir obrigatoriamente este documento.

---

# Princípios

Priorizar:

- Simplicidade
- Clareza
- Legibilidade
- Manutenção
- Testabilidade

Evitar:

- Código inteligente demais
- Abstrações desnecessárias
- Duplicação
- Acoplamento

---

# Clean Code

Todo código deverá seguir:

- SOLID
- DRY
- KISS
- YAGNI

---

# Estrutura de Pacotes

Cada módulo deverá possuir:

controller/

service/

repository/

entity/

dto/

mapper/

validator/

exception/

specification/

---

# Classes

Uma classe deve possuir apenas uma responsabilidade.

Classes muito grandes devem ser divididas.

Evitar classes acima de 500 linhas.

---

# Métodos

Métodos devem:

- realizar apenas uma tarefa
- possuir nomes claros
- evitar efeitos colaterais

Preferencialmente:

até 30 linhas.

---

# Variáveis

Utilizar nomes descritivos.

Evitar:

x

tmp

obj

data1

teste

---

# Constantes

Toda constante deverá possuir nome significativo.

Nunca utilizar números mágicos.

---

# Comentários

Comentar apenas:

- decisões
- regras complexas
- justificativas

Nunca comentar código óbvio.

---

# Controllers

Responsabilidades:

- receber requisição
- validar DTO
- chamar Service
- retornar resposta

Nunca:

- acessar Repository
- calcular regras
- acessar banco

---

# Services

Responsáveis por:

- regras de negócio
- orquestração
- transações

---

# Repositories

Responsáveis apenas por persistência.

Nunca conter:

if de negócio

validações

cálculos

---

# DTOs

Separar:

Request

Response

Nunca reutilizar DTO para ambos.

---

# Entities

Entities representam domínio.

Não expor pela API.

Não utilizar como DTO.

---

# Mapper

Utilizar exclusivamente MapStruct.

Evitar conversões manuais repetitivas.

---

# Exceptions

Criar exceções específicas.

Nunca lançar Exception genérica.

Utilizar Exception Handler Global.

---

# Validação

Toda entrada deve utilizar Bean Validation.

Nunca validar manualmente o que a framework resolve.

---

# Optional

Utilizar Optional apenas em retornos.

Nunca utilizar como atributo.

Nunca utilizar como parâmetro.

---

# Streams

Utilizar apenas quando melhorarem a legibilidade.

Evitar streams excessivamente complexas.

---

# Injeção de Dependência

Utilizar injeção por construtor.

Nunca utilizar field injection.

---

# Lombok

Permitido:

@Getter

@Setter

@Builder

@RequiredArgsConstructor

@NoArgsConstructor

@AllArgsConstructor

Evitar uso excessivo de anotações.

---

# Logging

Utilizar SLF4J.

Nunca utilizar System.out.println().

---

# Transações

Utilizar @Transactional apenas onde necessário.

Nunca abrir transações desnecessárias.

---

# Paginação

Obrigatória para listagens.

Nunca retornar listas gigantes.

---

# Ordenação

Toda listagem deverá permitir ordenação.

---

# Testes

Nome dos testes:

deveFazerXQuandoY()

Cada teste valida apenas um comportamento.

---

# Nomenclatura

Classes:

PascalCase

Métodos:

camelCase

Variáveis:

camelCase

Constantes:

UPPER_SNAKE_CASE

Pacotes:

lowercase

Endpoints:

kebab-case

Banco:

snake_case

---

# Código Morto

Proibido.

---

# TODO

Não deixar TODOs no código de produção.

Criar Issue.

---

# Imports

Remover imports não utilizados.

Evitar wildcard imports.

---

# Formatação

Indentação:

4 espaços.

UTF-8.

Final newline obrigatório.

---

# Princípio Final

Código é escrito para pessoas.

O compilador é apenas consequência.