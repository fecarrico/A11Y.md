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
- **Ferramentas deste padrão:** o repositório publica dois scripts opcionais em [`tools/`](https://github.com/fecarrico/A11Y.md/tree/main/tools), sem dependências: o `verify-a11y.py` roda no **seu projeto** — confere que os artefatos existem, que o `REPORT.md` é mais novo que a última mudança de interface e que o código não traz os anti-padrões da Seção 6; o `lint-standard.py` roda em **cópias ou forks deste padrão**, verificando paridade entre idiomas, gatilhos de carregamento e links. Executá-los nunca é requisito do padrão — o `A11Y.md` é markdown portátil —, mas um gate que reprova o build é mais forte que uma regra que alguém precisa lembrar.
- **Desacoplamento:** Não tente "escrever lógicas robustas para componentes acessíveis e tentar consertá-los": adote bibliotecas agnósticas (Headless UI) sempre que a semântica nativa HTML não cobrir os requisitos da funcionalidade.

### 1.1. Configuração padrão não é cobertura

Uma rodada limpa do axe significa "nenhuma violação entre as regras que estavam ligadas". Dois padrões merecem correção, ambos descobertos ao construir a landing deste próprio projeto sob este padrão:

- **Ligue as regras experimentais que carregam um Critério de Sucesso.** A `label-content-name-mismatch` detecta nome acessível que não contém o texto visível — uma **falha de SC 2.5.3, Nível AA**, que quebra controle por voz — e vem **desligada por padrão**, tanto no axe-core quanto na extensão de navegador. Ligue: `axe.run(context, { rules: { 'label-content-name-mismatch': { enabled: true } } })`, ou marque *Experimental rules* nas configurações da extensão. Em campo, foi essa regra que pegou um `aria-label` substituindo o texto visível de um seletor de idioma; a rodada padrão passou limpa.
- **Resolva o conflito linter × motor em vez de silenciá-lo.** A `scrollable-region-focusable` (axe) exige parada de foco num container que o usuário consegue rolar mas não alcançar por Tab; a `no-noninteractive-tabindex` (`eslint-plugin-jsx-a11y`) acusa exatamente esse `tabIndex`. Seguir as duas ao pé da letra é impossível, e o caminho de menor resistência — desligar a regra do ESLint — remove uma proteção real. Configure:
  ```jsonc
  // .eslintrc — permite a parada de foco que o axe exige, mantém a regra no resto
  "jsx-a11y/no-noninteractive-tabindex": ["error", { "roles": ["region"], "tags": [], "allowExpressionValues": true }]
  ```
  E lembre que a regra do axe é **condicional**: a parada de foco cabe só em regiões cujo conteúdo de fato transborda. Aplicá-la a todo container rolável cria paradas de tabulação que não levam a nada (ver *Armadilhas de Foco que Ninguém Pediu*, `A11Y.md` §6).

> **Um gate de CI é uma forma de verificação independente.** A *Independent Verification* (`A11Y.md` §2) pede que a evidência não seja de autoria exclusiva do agente que escreveu o código. Uma checagem de pipeline satisfaz isso na camada mecânica por construção — roda fora da sessão, contra o artefato, sem memória das decisões que o produziram. Ela não satisfaz, porém, os checkpoints humanos, e não eleva o nível de independência declarado no relatório para nada que uma máquina não consiga testar.

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

## 4.1. Avaliação formal (WCAG-EM) — quando o projeto for auditado

Nem todo produto passa por auditoria externa, e este padrão não presume que passe. Mas **quando passa**, o `REPORT.md` sozinho não é o instrumento certo: ele acompanha uma *feature*, e a auditoria avalia um *site ou aplicação inteira*. Os dois são complementares e a lacuna entre eles aparece tarde — normalmente na hora de emitir a Declaração de Acessibilidade exigida pela Seção 6.

Quando houver auditoria formal, avaliação de terceiro ou declaração pública no horizonte, ancore o trabalho na metodologia oficial do W3C, a [WCAG-EM](https://www.w3.org/TR/WCAG-EM/):

1. **Definir o escopo:** quais URLs/telas, qual nível-alvo, quais tecnologias de suporte.
2. **Explorar:** identificar tipos de página, funcionalidades essenciais, tecnologias usadas.
3. **Selecionar a amostra:** páginas estruturadas (uma de cada tipo, mais os fluxos completos) somadas a uma amostra aleatória — auditar "as páginas principais" sem amostragem declarada não é avaliação, é opinião.
4. **Auditar a amostra** contra cada critério do nível-alvo.
5. **Relatar:** use o [Template de Relatório de Avaliação](https://www.w3.org/WAI/test-evaluate/report-template/) ou o [WCAG-EM Report Tool](https://www.w3.org/WAI/eval/report-tool) do W3C-WAI, que produzem o formato que auditores e reguladores esperam ler.

Os `REPORT.md` acumulados do projeto são a **evidência de origem** dessa auditoria: eles mostram o que foi verificado, quando, por quem e o que ficou em aberto. Um repositório com histórico de relatórios chega à avaliação formal com lastro; um sem histórico começa do zero.

## 5. Relatórios e Responsabilidades (VPAT Strategy)
Projetos que visam o mercado dos EUA devem ser compatíveis com a Seção 508:
- **VPAT Creation:** Manter um documento técnico que registre quais critérios da WCAG são suportados total ou parcialmente.
- **Traceability:** Cada grande funcionalidade deve ter um comentário no código citando qual critério da WCAG está sendo respeitado.

## 6. European Compliance (EN 301 549)
Para conformidade com o EAA:
- **Interoperability:** Garantir que o software não impeça o uso de tecnologias assistivas de terceiros.
- **Accessibility Declaration:** Manter uma página de acessibilidade pública descrevendo as funcionalidades e o nível de conformidade alcançado.

## 6.1. Conformidade Brasileira (ABNT NBR 17225 / LBI)

Para produtos com público no Brasil:

- A **ABNT NBR 17225:2025** — *Acessibilidade em conteúdo e aplicações web: requisitos* — é a norma técnica brasileira, publicada em março de 2025. Reúne 146 diretrizes entre requisitos e recomendações, alinhadas à WCAG, e inclui uma lista de itens críticos (captchas, reconhecimento facial, navegação assistiva, contraste, espaçamento, arquivos, conteúdo de terceiros, componentes customizados).
- Ela dá lastro técnico ao **artigo 63 da Lei Brasileira de Inclusão (Lei 13.146/2015)**, que obriga a acessibilidade em sites de órgãos públicos e de empresas com sede ou representação comercial no país.
- **Efeito prático neste padrão:** conformidade WCAG 2.2 AA cobre a maior parte dos requisitos, mas a lista de itens críticos da norma brasileira é o checklist de recebimento em contratos públicos no Brasil. Se o projeto tem esse destino, declare-o no `REPORT.md` junto ao perfil de conformidade.

## 7. Compliance Versioning
Padrão Atual focado: **WCAG 2.2 AA** | **EN 301 549** | **ABNT NBR 17225** (Brasil, quando aplicável).
Desvios do requisito legal devido a limitações severas de UI/UX, plataforma nativa ou arquitetura base, **MUST** ser justificados usando obrigatoriamente o arquivo matriz na página: [**`templates/EXCEPTIONS.md`**](../templates/EXCEPTIONS.md). Todos esses pontos devem possuir ações compensatórias.

## 8. Padrões Externos e Motores (External Standards & Engines)
Para o contexto em tempo real da IA e referência do desenvolvedor, siga estes padrões canônicos da indústria:
- **WAI-ARIA APG:** [https://www.w3.org/WAI/ARIA/apg/](https://www.w3.org/WAI/ARIA/apg/)
- **eBay MIND Patterns:** [https://ebay.github.io/mindpatterns/](https://ebay.github.io/mindpatterns/)
- **Deque Axe Core:** [https://github.com/dequelabs/axe-core](https://github.com/dequelabs/axe-core)
