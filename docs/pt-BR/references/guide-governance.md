# A11y Governance & Compliance Strategy

> Escopo: Verificação estática, estratégia VPAT, conformidade ADA/EAA, EN 301 549 e prontidão para auditoria externa.

## 1. Verificação Estática (O Mínimo de Engenharia)
A verificação primária não consiste em ditar regras rígidas em uma *pipeline específica*, mas responsabilizar o ambiente de desenvolvimento (Seja o Dev ou a IA rodando em tempo real) por testes estáticos de validação rápida.
- **Padrão de Código:** O código *deve* passar obrigatoriamente pelas checagens de linters ou avaliadores focados em acessibilidade (como `eslint-plugin-jsx-a11y` ou motor `axe`) sem exibir violações do nível crítico/sério antes da consolidação de código. 
- **Ferramentas deste padrão:** o repositório publica dois scripts opcionais em [`tools/`](https://github.com/fecarrico/A11Y.md/tree/main/tools), sem dependências: o `verify-a11y.py` roda no **seu projeto** — confere que os artefatos existem, que o `REPORT.md` é mais novo que a última mudança de interface e que o código não traz os anti-padrões da Seção 6; o `lint-standard.py` roda em **cópias ou forks deste padrão**, verificando paridade entre idiomas, gatilhos de carregamento e links. Executá-los nunca é requisito do padrão — o `A11Y.md` é markdown portátil —, mas um gate que reprova o build é mais forte que uma regra que alguém precisa lembrar.
- **Desacoplamento:** Não tente "escrever lógicas robustas para componentes acessíveis e tentar consertá-los": adote bibliotecas agnósticas (Headless UI) sempre que a semântica nativa HTML não cobrir os requisitos da funcionalidade.

### 1.1. Configuração padrão não é cobertura

Uma rodada limpa do axe significa "nenhuma violação entre as regras que estavam ligadas". Dois padrões merecem correção, ambos descobertos ao construir a landing deste próprio projeto sob este padrão:

- **Ligue as regras experimentais que carregam um Critério de Sucesso.** A `label-content-name-mismatch` detecta nome acessível que não contém o texto visível — uma **falha de SC 2.5.3, Nível AA**, que quebra controle por voz — e vem **desligada por padrão**, tanto no axe-core quanto na extensão de navegador. Ligue: `axe.run(context, { rules: { 'label-content-name-mismatch': { enabled: true } } })`, ou marque *Experimental rules* nas configurações da extensão.
- **Resolva o conflito linter × motor em vez de silenciá-lo.** A `scrollable-region-focusable` (axe) exige parada de foco num container que o usuário consegue rolar mas não alcançar por Tab; a `no-noninteractive-tabindex` (`eslint-plugin-jsx-a11y`) acusa exatamente esse `tabIndex`. Seguir as duas ao pé da letra é impossível, e o caminho de menor resistência — desligar a regra do ESLint — remove uma proteção real. Configure:
  ```jsonc
  // .eslintrc — permite a parada de foco que o axe exige, mantém a regra no resto
  "jsx-a11y/no-noninteractive-tabindex": ["error", { "roles": ["region"], "tags": [], "allowExpressionValues": true }]
  ```
  E lembre que a regra do axe é **condicional**: a parada de foco cabe só em regiões cujo conteúdo de fato transborda. Aplicá-la a todo container rolável cria paradas de tabulação que não levam a nada (ver *Armadilhas de Foco que Ninguém Pediu*, `A11Y.md` §6).

> **Um gate de CI é uma forma de verificação independente.** A *Independent Verification* (`A11Y.md` §2) pede que a evidência não seja de autoria exclusiva do agente que escreveu o código. Uma checagem de pipeline satisfaz isso na camada mecânica por construção — roda fora da sessão, contra o artefato, sem memória das decisões que o produziram. Ela não satisfaz, porém, os checkpoints humanos, e não eleva o nível de independência declarado no relatório para nada que uma máquina não consiga testar.

### 1.2. Independent Verification — quem assina a evidência

A *Independent Verification* (`A11Y.md` §2) existe porque a auto-revisão reexecuta o raciocínio que produziu o defeito. A evidência: o defeito de Orphaned ARIA deste próprio padrão sobreviveu ao agente gerador, ao axe **e** ao Lighthouse, e só apareceu num teste independente ([a11y-md-ai-test](https://github.com/mjepis7/a11y-md-ai-test), de Maria Eduarda Iwashita); e modelos encontram mais bugs em código de outro modelo do que no próprio (Greptile, [*Models are worse at reviewing their own code*](https://www.greptile.com/blog/model-inversion), 2026 — dois datasets de 500 PRs, o padrão se inverte nos dois sentidos).

- **cross-agent** — um modelo diferente quebra a correlação entre os defeitos gerados e os defeitos procurados. A forma mais forte.
- **fresh-context** — o mesmo modelo *sem a conversa que produziu o código*: remove a memória de ter decidido. O piso em qualquer lugar — custa um chat novo sobre o mesmo projeto, nunca uma ferramenta nova.
- **self-reported** ⚠️ — honesto e visível, nunca suficiente: reexecuta exatamente o modo de falha que a regra existe para quebrar. Teto: ⚠️ CONDICIONAL.

A declaração é baseada em confiança e ainda assim auditável: o `REPORT.md` nomeia *quem* verificou, e o `verify-a11y.py` aplica o teto mecanicamente (um ✅ PASS self-reported reprova no gate). Nada disso substitui os checkpoints humanos — um segundo agente resolve uma referência entre arquivos; ele não escuta um leitor de tela.

## 2. Evidência Descritiva (The "Why")
Ao criar widgets complexos customizados, o desenvolvedor (ou a IA) MUST incluir um bloco de comentários explicando a estratégia de acessibilidade:
- Qual é a Focus order (ordem de foco)?
- Como os estados são comunicados?
- Qual é o fallback para ambientes sem JS?

## 3. Restrições da Linguagem Visual
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

Para produtos que servem público brasileiro:

- A **ABNT NBR 17225:2025** — *Acessibilidade em conteúdo e aplicações web: requisitos* (março de 2025) — é a norma técnica brasileira e o lastro do **art. 63 da LBI (Lei 13.146/2015)**, que obriga acessibilidade nos sites de órgãos públicos e de empresas com presença no Brasil. Ela organiza **146 itens — 96 requisitos + 50 recomendações — em 16 grupos temáticos**, cada um mapeado a um SC da WCAG 2.2, e define dois níveis de conformidade:
  - **Regular** = todos os 96 requisitos — declarada equivalente à WCAG 2.2 A+AA. Mapeamento de perfil: **Standard (AA) ≈ regular**.
  - **Plena** = requisitos + todas as 50 recomendações, em que recomendação não atendida exige *justificativa razoável* — exatamente a mecânica do `EXCEPTIONS.md` / `A11Y-DECISIONS.md` deste padrão. Mapeamento de perfil: **Shield (AAA) ≈ plena**.
- **Anexo A — a lista de itens críticos**, o checklist de aceitação em compras públicas brasileiras: CAPTCHA com modalidade alternativa · **reconhecimento facial / biometria com rota alternativa acessível** · conteúdo apenas em hover/foco · conteúdo inserido via CSS · conteúdo de terceiros, com o usuário avisado · componentes customizados · **arquivos para download (não-HTML) eles próprios acessíveis** · tabelas de leiaute · marcação conforme a especificação. Três desses vão além da prática WCAG do dia a dia: biometria, arquivos e conteúdo via CSS.
- O **Anexo B** traz dez declarações de desempenho funcional (da EN 301 549) — o `REPORT.md` §7 as oferece como seção opcional que serve NBR, EN 301 549 e VPAT de uma vez.
- **Efeito prático:** com destino brasileiro, o `REPORT.md` declara o nível NBR pretendido (regular/plena) ao lado do perfil de conformidade, e o Anexo A é tratado como checklist nomeado. Para usuários de língua de sinais, ver [Língua de Sinais & Libras](guide-sign-language-br.md).

## 7. Compliance Versioning
Padrão Atual focado: **WCAG 2.2 AA** | **EN 301 549** | **ABNT NBR 17225** (Brasil, quando aplicável).
Desvios do requisito legal devido a limitações severas de UI/UX, plataforma nativa ou arquitetura base, **MUST** ser justificados usando obrigatoriamente o arquivo matriz na página: [**`templates/EXCEPTIONS.md`**](../templates/EXCEPTIONS.md). Todos esses pontos devem possuir ações compensatórias.
