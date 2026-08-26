# Acessibilidade & a Web Agêntica

> **Escopo:** Como agentes de IA que operam interfaces — agentes de navegador, modelos de computer use — consomem páginas; onde isso coincide com a acessibilidade humana, onde diverge, e as duas armadilhas. Contexto não-normativo, exceto onde aponta para regras do core.

## 0. A afirmação, na ordem certa

Este padrão é construído para pessoas. Acontece que a mesma camada é o que os agentes operam: as arquiteturas dominantes leem a **árvore de acessibilidade** — os mesmos roles, nomes e estados que servem um leitor de tela — porque ela custa uma ordem de grandeza menos que pixels. A ordem do argumento não é negociável: *precisamos disso para pessoas, e agentes também se beneficiam.* Uma interface "legível para agentes" que pessoas com deficiência não conseguem usar falhou com os dois públicos e com este padrão.

## 1. O que os agentes realmente leem

- Agentes de navegador e modelos de computer use convergem para **híbridos de AXTree + DOM**; os frameworks descrevem a página ao modelo por snapshots da árvore de acessibilidade, e os fabricantes documentam que labels e roles ARIA são o que seus agentes consomem.
- A evidência controlada: páginas com HTML semântico, nomes acessíveis e dados estruturados quase **dobraram a taxa de sucesso de agentes (≈89% vs ≈49%)** com menos passos — a mesma marcação que este padrão já obriga.
- A sobreposição é o núcleo deste arquivo: semântica nativa, nomes acessíveis, estados programáticos, landmarks, operabilidade por teclado. **Toda regra do core que alimenta a árvore de acessibilidade alimenta o agente.** Não há nada extra a gerar.

## 2. Onde as necessidades divergem

- **Agentes não precisam** da camada perceptual: contraste, tamanho de alvo, redução de movimento, legendas, pisos de fonte. Essas regras existem para pessoas e não se flexibilizam porque um agente é indiferente a elas — pessoas vêm primeiro, sempre.
- **Agentes precisam do que a acessibilidade não define:** contratos de ação (o que um controle *faz*, pré-condições e efeitos — a camada emergente WebMCP), identificadores estáveis, dados legíveis por máquina. Isso é uma camada **adicional** sobre a interface acessível, nunca um substituto dela.

## 3. As duas armadilhas (estas são regras)

- **ARIA como isca para robôs** — adicionar ARIA para parecer "amigável a agentes" é o [*ARIA Soup*](../A11Y.md) (core §6) em escala: agentes leem a mesma árvore que a tecnologia assistiva, e os dados de campo mostram páginas com mais ARIA carregando **mais** erros detectados, não menos. Nada sobre agentes muda a Primeira Regra do ARIA.
- **Portas de conteúdo só-máquina** — uma "visão para agentes" paralela ou cópia achatada do conteúdo para máquinas é o anti-pattern novo do core §6 (*Machine-Only Content Doors*): versões paralelas divergem, e a cópia achatada remove a estrutura de que a tecnologia assistiva precisa. Uma única interface canônica e acessível.

## 4. O dano colateral a vigiar

Muralhas anti-bot e CAPTCHAs classificam cada vez mais usuários de tecnologia assistiva como automação. Se o produto bloqueia agentes — escolha legítima —, verifique que o caminho acessível continua funcionando para pessoas: o mecanismo de bloqueio não distingue o padrão de uso de um leitor de tela do de um bot.

*A evidência por trás deste guia (arquiteturas de agentes, o estudo controlado, as posições da comunidade) está compilada nas notas de pesquisa do projeto; o benchmark do próprio padrão mede o lado humano.*
