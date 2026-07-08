🇺🇸 Read in English: ./README.md

> ⚠️ Esta é a versão original em português.
> A versão oficial e atualizada do projeto (e da Wiki) está em inglês.

<div align="center">
  <img src="./a11ymd.png" alt="Project A11Y.md Banner" style="max-width: 100%; border-radius: 8px;" />
  <br/><br/>
  <h1>♿ Project A11Y.md</h1>
  <p><b>O Sistema de Contexto Persistente para Acessibilidade</b></p>
  
  [![WCAG 2.2 AA](https://img.shields.io/badge/WCAG-2.2_AA-blue.svg)](#)
  [![ADA Compliant](https://img.shields.io/badge/Compliance-ADA%20%7C%20EAA-success.svg)](#)
  [![AI Ready](https://img.shields.io/badge/Context-AI_Ready-purple.svg)](#)
  
  <br/>
  <a href="https://github.com/fecarrico/A11Y.md/wiki" target="_blank">📖 Leia a Wiki Oficial</a> | <a href="https://v0-projecta11y.vercel.app/" target="_blank">🌐 Site Oficial</a> | <a href="https://medium.com/ux-user-experience-design-em-portugues/a11y-md-acessibilidade-antes-de-qualquer-prompt-5c8778ccb310" target="_blank">📝 Leia o Manifesto (Medium)</a>
</div>

<br/>

> **O A11Y.md não é um guia de boas práticas.**
> Ele é um protocolo de validação de acessibilidade e uma **arquitetura de contexto persistente** para o desenvolvimento de softwares guiado por IA. Foi concebido para integrar-se com agentes autônomos (Cursor, Claude, Copilot) garantindo conformidade certificável desde a origem.

Nós tratamos arquivos como `.gitignore`, `eslint` e `CLAUDE.md` como verdades canônicas nos nossos repositórios. Mas por que a acessibilidade não é canônica? O `A11Y.md` traduz as regras de acessibilidade para uma camada de governança universal. Em vez de regras genéricas, ele força qualquer agente a aderir estritamente às normas WCAG 2.2 AA e ADA desde a primeira linha de código gerada.

---

## ⚡ Core Features (Inovações)

- 🧠 **Contrato Comportamental da IA (8 Regras):** Restrições determinísticas que forçam a IA a atuar como uma tradutora semântica entre frameworks e a parar de gerar anti-padrões destrutivos (como `divs` clicáveis).
- 🛡️ **Compliance Profiles Modulares:** Suporte aos perfis Shield (AAA), Standard (AA) e **Launchpad (A)**. O perfil Launchpad permite que startups construam MVPs rápidos relaxando regras visuais cosméticas, sem nunca sacrificar a estrutura semântica crítica.
- 📚 **Lazy Context Loading:** 20 guias profundos de engenharia (WAI-ARIA APG). A IA é programada para carregar apenas os guias necessários sob demanda, economizando tokens e mantendo o foco afiado.

---

## 🚀 Quick Start (Menos de 2 minutos)

Ler sobre acessibilidade é o primeiro passo, injetá-la no código é o objetivo real. Faça isto **agora** no seu projeto:

1. **Baixe o Padrão:** Copie o arquivo `docs/pt-BR/A11Y.md` para o repositório da sua aplicação. (Ele pode ser colocado na raiz, dentro de uma pasta `docs/`, ou em qualquer outro lugar). Opcionalmente, copie também as pastas `references/` e `templates/` junto dele para manter os guias detalhados disponíveis offline; se você não copiá-las, a IA usa como fallback os guias deste repositório via URLs upstream.
2. **Injete o Comando:** Você precisa instruir explicitamente a sua IA a lê-lo. Se você usa um arquivo `.cursorrules` ou `CLAUDE.md`, adicione esta diretiva:
   > *"Ao desenvolver o frontend, siga estritamente as regras de desenvolvimento definidas no arquivo A11Y.md."*
3. **Defina o Perfil:** A IA perguntará proativamente qual Compliance Profile (Shield, Standard ou Launchpad) ela deve usar, caso você não tenha especificado.

👉 **<a href="https://github.com/fecarrico/A11Y.md/wiki/Setup-and-Integration" target="_blank">Leia o guia completo de Setup e Integração na nossa Wiki.</a>**

---

## 📖 Documentação Oficial (A Wiki)

A arquitetura completa, protocolos e exemplos práticos estão profundamente documentados na nossa Wiki no GitHub (em Inglês).

**<a href="https://github.com/fecarrico/A11Y.md/wiki" target="_blank">🔗 Visite a Wiki do A11Y.md</a>**

Lá dentro você encontrará:
- **O Command Center:** Como o arquivo principal A11Y.md funciona.
- **Anti-patterns & Protocol:** Casos reais de alucinações de IA sendo corrigidas nativamente.
- **Reference Library:** A taxonomia dos 20 guias de engenharia.
- **Governança & Compliance:** Preparação técnica para auditorias formais.

---

## 🔍 O Impacto Prático (Antes vs Depois)

A diferença entre um código gerado aleatoriamente e um código guiado pelo `A11Y.md`:

**❌ Sem o Contexto A11y:**
- IA gerando `<div onClick={...}>` (quebrando interações via teclado).
- Modais impossíveis de fechar com `ESC` (Focus Trap invertido e inacessível).
- Mensagens de erro visuais que não são lidas por Leitores de Tela.

**✅ Com o Contexto A11y Ativo:**
- Elementos `<button>` nativos usados como regra rígida.
- Foco gerenciado automaticamente após transições de roteamento em SPAs.
- Injeções precisas de `aria-live` para leitura imediata de dados dinâmicos.

---

## 💡 O Paradigma do Projeto

Nossa filosofia determina que a acessibilidade web nunca deve ser um "polimento tardio", mas sim uma **pré-condição de uso técnica**. A estrutura sustenta-se em três pilares:

- 👤 **Human-Centric:** Desenhado estritamente para garantir autonomia real a usuários com deficiência.
- 🤖 **AI-Ready:** Diretrizes determinísticas criadas especificamente para ancorar o comportamento de Agentes de código, ceifando pela raiz a "invenção" (alucinações técnicas).
- ⚖️ **Certifiable:** Cada diretriz no `A11Y.md` é mapeada explicitamente para critérios WCAG 2.2 rigorosos, permitindo uma rastreabilidade direta que blinda a empresa em auditorias.

---

## 🤝 Open Source & Comunidade

O A11Y.md é fundamentalmente uma iniciativa open-source. Não me coloco como o dono da verdade absoluta em acessibilidade, mas sim como um entusiasta tentando cruzar a ponte entre Inclusão e Inteligência Artificial.

O objetivo deste projeto é ser uma arquitetura viva. Ele depende da comunidade open-source — pessoas muito mais inteligentes e experientes em engenharia de acessibilidade — para contribuir, refinar a biblioteca de referências e tornar esse sistema robusto o suficiente para mudar como soluções digitais são criadas na era do "vibe coding".

**Pull Requests para melhorar os guias de referência ou o Contrato da IA são extremamente bem-vindos!**

---

<br />

<div align="center">
  <p><b>Autor & Curadoria</b></p>
  <h3>Felipe A. Carriço</h3>
  <p><i>UX Designer Especialista | AI Product Builder | Daltônico</i></p>
  
  <p>Construído a partir da premissa de que a eficiência da inteligência artificial deve, invariavelmente, atuar como alavanca e destruidor de barreiras tanto no mundo físico quanto no digital.</p>
  
  <a href="https://linkedin.com/in/fecarrico" target="_blank">LinkedIn</a> | <a href="https://medium.com/@carrico" target="_blank">Medium</a>
</div>
