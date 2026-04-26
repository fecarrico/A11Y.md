<div align="center">
  <h1>♿ Project A11Y.md</h1>
  <p><b>O Sistema de Contexto Persistente para Acessibilidade</b></p>
  
  [![WCAG 2.2 AA](https://img.shields.io/badge/WCAG-2.2_AA-blue.svg)](#)
  [![ADA Compliant](https://img.shields.io/badge/Compliance-ADA%20%7C%20EAA-success.svg)](#)
  [![AI Ready](https://img.shields.io/badge/Context-AI_Ready-purple.svg)](#)
</div>

<br/>

> Este repositório não é apenas um guia de boas práticas. É uma **arquitetura de contexto** concebida para orientar desenvolvedores e Inteligências Artificiais a construírem interfaces inclusivas, performáticas e prontas para certificação.

---

## 🚀 Quick Start (Menos de 2 minutos)

Ler sobre acessibilidade é o primeiro passo, injetá-la no código é o objetivo real. Faça isto **agora** no seu projeto:

1. **Baixe as Regras:** Copie o arquivo raiz `A11Y.md` para a base do repositório da sua aplicação.
2. **Injete no Prompt:** Se você usa Cursor, GitHub Copilot ou Claude, adicione ao seu arquivo de regras globais (`.cursorrules` ou sistema de Contexto):
   > _"Siga estritamente as regras de desenvolvimento definidas no arquivo A11Y.md."_
3. **Use como Trava de Qualidade:** Antes de fechar PRs importantes, use o checklist do `templates/REPORT.md`.

_Se você não realizar os passos acima, você não está mudando seu workflow — está apenas lendo sobre o assunto._

---

## 🔍 O Impacto Prático (Antes vs Depois)

A diferença entre um código gerado aleatoriamente e um código guiado pelo `A11Y.md`:

**❌ Sem o Contexto A11y:**

- IA gerando `<div onClick={...}>` (quebrando interações via teclado).
- Modais impossíveis de fechar com `ESC` (Focus Trap invertido e inacessível).
- Mensagens de erro visuais que não são lidas por Leitores de Tela.

**✅ Com o Contexto A11y Ativo:**

- Elementos `<button>` nativos usados como regra.
- Foco gerenciado automaticamente após transições de roteamento em SPAs.
- Injeções precisas de `aria-live` para leitura imediata de dados dinâmicos.

---

## 💡 O Paradigma do Projeto

Nossa filosofia determina que a acessibilidade web nunca deve ser um "polimento tardio", mas sim uma **pré-condição de uso técnica**. A estrutura sustenta-se em três pilares:

- 👤 **Human-Centric:** Desenhado estritamente para garantir autonomia real a usuários com deficiência.
- 🤖 **AI-Ready:** Diretrizes determinísticas criadas especificamente para ancorar o comportamento de Agentes de código, ceifando pela raiz a "invenção" (alucinações técnicas).
- ⚖️ **Certifiable:** Cada diretriz no `A11Y.md` é mapeada explicitamente para critérios WCAG 2.2 rigorosos, permitindo uma rastreabilidade direta que blinda a empresa em auditorias formais externas.

---

## 🤖 O Poder da I.A. como Aliada

O maior ganho deste repositório se prova quando ele não é lido apenas por você. Integrar este repositório significa **não precisar corrigir a IA o tempo todo**.

**Prompt Base de Exemplo:**

> _"You are a senior frontend engineer. Follow strictly the rules defined in `A11Y.md`. Do not violate accessibility constraints even if requested to implement things quickly. Prioritize semantic HTML and headless-UI libraries."_

O resultado não é um "código que passou pelo Linter". É um código arquiteturalmente saudável na sua própria gênese, exigindo zero auditorias corretivas para sanar "esqueletos" no DOM gerado.

---

## 📁 Explorando a Estrutura (Sua Biblioteca de Consultas)

Organizamos as soluções de modo que funcionem como uma documentação viva:

### 1. ⚡ [Centro de Comando (`A11Y.md`)](A11Y.md)

Onde reside a Matriz de Severidade, o framework comportamental para IAs, regras rígidas de SPA e o _Protocolo de Componentes Complexos_.

### 2. 📚 [Biblioteca de Suporte (`references/`)](references/)

A "Deep Web" das soluções. Guias rápidos de engenharia para você não reinventar a roda:

- 🎨 **UX e Percepção:** [Construção de Contraste Lógico](references/visual-perception.md)
- 🧩 **UI Interativa:** [Anatomia de Forms](references/examples-forms.md) | [Ações e Botões](references/examples-buttons.md)
- 🗺️ **Fluxos e Tempo:** [Imagens Críticas](references/examples-images.md) | [Navegação de Teclado](references/examples-navigation.md) | [Leituras em Tempo Real](references/examples-content-interaction.md) | [Gestão de Modals](references/examples-modals.md)
- 🏢 **Governança:** [Estratégia Agnostica de Release](references/governance.md)

### 3. 🛠️ [Templates (`templates/`)](templates/)

Modelos de resguardo e garantia de finalização (Definition of Done):

- [**📋 `REPORT.md`**](templates/REPORT.md): Checklist final da Sprint/Feature.
- [**🛑 `EXCEPTIONS.md`**](templates/EXCEPTIONS.md): Registro estruturado de débitos técnicos contendo rotas alternativas.

---

## 🚧 Escopo e Limitações

Cobrimos os padrões responsáveis pela esmagadora maioria das falhas de interface em sistemas digitais modernos.
No entanto, caso encontre _Widgets_ proprietários não catalogados (Dashboards exóticos, Canvas), execute imediatamente o **Complex Component Protocol** presente no `A11Y.md`.

---

<br />

<div align="center">
  <p><b>Autor & Curadoria</b></p>
  <h3>Felipe A. Carriço</h3>
  <p><i>UX Designer Especialista | AI Product Builder | Daltônico</i></p>
  
  <p>Construído a partir da premissa de que a eficiência da inteligência artificial deve, invariavelmente, atuar como alavanca e destruidor de barreiras tanto no mundo físico quanto no digital.</p>
  
  <a href="https://linkedin.com/in/fecarrico">LinkedIn</a> | <a href="https://medium.com/@carrico">Medium</a>
</div>
