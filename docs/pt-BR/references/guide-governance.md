# A11y Governance & Compliance Strategy

> Escopo: Verificação estática, estratégia VPAT, conformidade ADA/EAA, EN 301 549 e prontidão para auditoria externa.

## 0. Onde uma regra deve morar (princípio de projeto deste padrão)

> **Evidência de campo (01/08/2026):** num post-mortem documentado de um projeto real, um agente aplicou corretamente as Seções 0 a 6 e não produziu nenhum `REPORT.md` nem `EXCEPTIONS.md`. O artefato que *foi* produzido (`A11Y-DECISIONS.md`) era o único citado pelo nome dentro de uma regra do **AI Behavior Contract**. A variável não foi obrigatoriedade — os outros dois já eram MUST em outros pontos — foi **onde o nome do arquivo aparecia**.

Agentes tratam a Seção 2 como contrato executável e todo o resto como material de consulta. Portanto, ao estender este padrão:

- **Tudo que a IA precisa FAZER** — criar um arquivo, recusar uma ação, checar algo antes de prosseguir — pertence ao **AI Behavior Contract (Seção 2)**, com um evento-gatilho explícito.
- **A Seção 7 e os guias de referência** carregam profundidade, detalhe de verificação e justificativa — eles explicam e ampliam, mas nunca devem ser o *único* lugar onde uma obrigação existe.
- Prefira **gatilhos por evento** ("antes de qualquer entrega ao usuário final") a **gatilhos por fase** ("na entrega final"): projetos de entrega contínua nunca alcançam a fase, e a regra nunca dispara.

## 1. Verificação Estática (O Mínimo de Engenharia)
A verificação primária não consiste em ditar regras rígidas em uma *pipeline específica*, mas responsabilizar o ambiente de desenvolvimento (Seja o Dev ou a IA rodando em tempo real) por testes estáticos de validação rápida.
- **Padrão de Código:** O código *deve* passar obrigatoriamente pelas checagens de linters ou avaliadores focados em acessibilidade (como `eslint-plugin-jsx-a11y` ou motor `axe`) sem exibir violações do nível crítico/sério antes da consolidação de código. 
- **Desacoplamento:** Não tente "escrever lógicas robustas para componentes acessíveis e tentar consertá-los": adote bibliotecas agnósticas (Headless UI) sempre que a semântica nativa HTML não cobrir os requisitos da funcionalidade.

## 2. Evidência Descritiva (The "Why")
Ao criar widgets complexos customizados, o desenvolvedor (ou a IA) MUST incluir um bloco de comentários explicando a estratégia de acessibilidade:
- Qual é a Focus order (ordem de foco)?
- Como os estados são comunicados?
- Qual é o fallback para ambientes sem JS?

## 3. Restrições da Linguagem Visual (Visual Language Constraints)
- **Color:** NUNCA comunique um estado (Válido/Inválido/Aviso) usando apenas cor. Um ícone acompanhando ou uma descrição em texto é obrigatório.
- **Contrast:** Cores da marca que falham no ratio de 4.5:1 MUST ser ajustadas para elementos de UI ou pareadas com uma alternativa de alto contraste.

## 4. Auditorias e Conformidade Legal (ADA/EAA Readiness)
Para preparar sub-sistemas para certificação externa e auditoria:
1. **Inventory:** Consolidar uma lista ou storybook dos componentes visuais chaves do fluxo e seus comportamentos com tecnologias assistivas.
2. **Keyboard Path:** Prevenir Dead-ends através do mapeamento claro e planejado da ordem do layout visual (`Tab`).
3. **Auditoria Padrão:** O checklist em [**`templates/REPORT.md`**](../templates/REPORT.md) **MUST** ser operado como "Definition of Done" **antes de qualquer entrega ao usuário final** — build publicado, deploy, artefato compartilhado, tag — e não apenas numa "entrega final" que projetos de entrega contínua nunca alcançam (ver *Release Evidence*, `A11Y.md` §2).
4. **Um relatório vivo, não um por publicação:** o relatório acompanha a **interface**, não a contagem de releases. Se nada mudou desde o último, ele continua valendo. Quando a interface muda, atualize a data e revisite apenas as entradas afetadas: todo checkpoint cuja evidência a mudança invalida volta para `[ ]` ou `[~]` até ser reverificado. Checkpoints humanos (leitor de tela, simulador de cor) mantêm o `[x]` e a data da sessão que os produziu, e são refeitos quando o fluxo que cobriam muda.

## 5. Relatórios e Responsabilidades (VPAT Strategy)
Projetos que visam o mercado dos EUA devem ser compatíveis com a Seção 508:
- **VPAT Creation:** Manter um documento técnico que registre quais critérios da WCAG são suportados total ou parcialmente.
- **Traceability:** Cada grande funcionalidade deve ter um comentário no código citando qual critério da WCAG está sendo respeitado.

## 6. European Compliance (EN 301 549)
Para conformidade com o EAA:
- **Interoperability:** Garantir que o software não impeça o uso de tecnologias assistivas de terceiros.
- **Accessibility Declaration:** Manter uma página de acessibilidade pública descrevendo as funcionalidades e o nível de conformidade alcançado.

## 7. Compliance Versioning
Padrão Atual focado: **WCAG 2.2 AA** | **EN 301 549**.
Desvios do requisito legal devido a limitações severas de UI/UX, plataforma nativa ou arquitetura base, **MUST** ser justificados usando obrigatoriamente o arquivo matriz na página: [**`templates/EXCEPTIONS.md`**](../templates/EXCEPTIONS.md). Todos esses pontos devem possuir ações compensatórias.

## 8. Padrões Externos e Motores (External Standards & Engines)
Para o contexto em tempo real da IA e referência do desenvolvedor, siga estes padrões canônicos da indústria:
- **WAI-ARIA APG:** [https://www.w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/)
- **eBay MIND Patterns:** [https://ebay.github.io/mindpatterns/](https://ebay.github.io/mindpatterns/)
- **Deque Axe Core:** [https://github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)
