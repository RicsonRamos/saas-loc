# Visão do Produto

## Nome do Projeto

(Nome a ser definido)

---

# Objetivo

Desenvolver um sistema SaaS (Software as a Service) para gestão de locadoras de veículos, permitindo que múltiplas empresas utilizem uma única plataforma de forma segura, isolada e escalável.

O sistema será comercializado por assinatura mensal, dispensando instalação local e permitindo acesso via navegador.

---

# Problema

Grande parte das pequenas e médias locadoras utiliza:

- Planilhas Excel
- Sistemas antigos
- Sistemas desktop
- Controle manual
- Processos descentralizados

Isso gera:

- Falta de controle financeiro
- Perda de informações
- Dificuldade para acompanhar manutenção
- Baixa visibilidade da lucratividade
- Pouca escalabilidade

---

# Solução

Uma plataforma web centralizada que permita controlar toda a operação da locadora.

Entre os módulos estão:

- Gestão da frota
- Cadastro de clientes
- Contratos
- Financeiro
- Manutenções
- Relatórios
- Dashboard
- Indicadores de desempenho

---

# Público-alvo

Pequenas e médias locadoras de veículos.

Inicialmente o foco será:

- até 500 veículos
- até 50 usuários por empresa

---

# Modelo de Negócio

Software como Serviço (SaaS).

Características:

- assinatura mensal
- múltiplos planos
- atualização contínua
- hospedagem em nuvem
- backup automático
- suporte remoto

---

# Plataforma

Aplicação Web.

Compatível com:

- Desktop
- Notebook
- Tablet
- Smartphone

O sistema deverá possuir interface responsiva.

---

# Arquitetura Geral

Será utilizado um monólito modular.

Cada empresa utilizará a mesma aplicação.

Os dados serão isolados através de arquitetura Multi-Tenant utilizando tenant_id.

---

# Objetivos Técnicos

O sistema deve ser:

- Escalável
- Seguro
- Modular
- Testável
- Fácil manutenção
- Alta disponibilidade
- Cloud Native
- API First

---

# Funcionalidades Principais

- Cadastro de Empresas

- Cadastro de Usuários

- Controle de Permissões

- Cadastro de Clientes

- Cadastro da Frota

- Contratos

- Controle Financeiro

- Controle de Manutenções

- Controle de Documentação

- Indicadores Financeiros

- Dashboard

- Relatórios

- Auditoria

---

# Diferenciais

O sistema deverá fornecer indicadores que normalmente não existem em sistemas simples de locação.

Exemplos:

- lucro por veículo

- custo por quilômetro

- payback do investimento

- comparação FIPE x valor pago

- rentabilidade da frota

- tempo parado

- taxa de ocupação

- despesas por veículo

---

# Escopo Inicial (MVP)

O MVP deverá conter apenas os módulos essenciais:

- Empresas

- Usuários

- Clientes

- Veículos

- Contratos

- Financeiro

- Manutenções

- Dashboard

---

# Fora do Escopo Inicial

Não fazem parte da primeira versão:

- aplicativo mobile nativo

- integração bancária

- emissão fiscal

- telemetria

- rastreamento GPS

- inteligência artificial

Esses recursos poderão ser adicionados futuramente.

---

# Princípios do Projeto

- Simplicidade antes da complexidade.

- Arquitetura preparada para crescimento.

- Segurança desde a primeira versão.

- Código limpo.

- Baixo acoplamento.

- Alta coesão.

- Todas as funcionalidades devem possuir justificativa de negócio.

- Nenhuma funcionalidade será implementada sem documentação prévia.

---

# Visão de Longo Prazo

Transformar a plataforma em um ERP completo para locadoras, oferecendo um ecossistema integrado de gestão operacional, financeira e administrativa, mantendo arquitetura capaz de atender desde pequenas empresas até operações com milhares de veículos.