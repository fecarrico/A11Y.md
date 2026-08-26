# Accessibility: Língua de Sinais & Tradução Automática de Libras

> **Escopo:** Servir quem usa língua de sinais — Libras no Brasil — incluindo os widgets de tradução automática (Hand Talk, VLibras), a janela de Libras em vídeo, e a linha onde o avatar deixa de bastar. Carregue quando o público inclui o Brasil ou qualquer população usuária de língua de sinais.

## 0. A regra que rege as demais

Para a maioria das pessoas usuárias de língua de sinais, a língua de sinais é a primeira língua e o texto escrito é a **segunda**. Os tradutores automáticos (Hand Talk, VLibras) são camadas de melhor esforço que leem o **DOM renderizado, sob clique ou seleção do usuário** — traduzem o que a marcação expõe, na qualidade de língua que o conteúdo oferece. As duas metades são trabalho do desenvolvedor: marcação que o widget alcança, e texto que sobrevive à tradução.

## 1. O que os tradutores alcançam — e o que não

Hand Talk e VLibras capturam **nós de texto reais** (a Hand Talk também traduz o `alt` de imagem). Cada regra abaixo é, ao mesmo tempo, beco sem saída para o tradutor e falha WCAG:

- Texto **MUST** ser texto real no DOM — nunca dentro de imagem, canvas ou pseudo-elemento de CSS (a lista de anti-patterns do core já proíbe os três; os tradutores acrescentam mais um motivo).
- Imagens informativas **MUST** ter `alt` (SC 1.1.1) — para a Hand Talk, o `alt` *é* o conteúdo traduzível.
- `lang` **MUST** estar correto na raiz e nos trechos em outro idioma (SC 3.1.1/3.1.2): os tradutores assumem o idioma da página na entrada.
- **MUST NOT** aplicar `user-select: none` ou `pointer-events: none` a conteúdo textual — seleção e clique são o mecanismo de captura.
- **SHOULD NOT** colocar conteúdo essencial em iframes: a Hand Talk exige configuração explícita (`addListenersToIframe`) e o widget do VLibras só lê o documento em que foi instanciado.

## 2. Texto que sobrevive à tradução

- Mantenha cada bloco de texto **abaixo de ~500–1000 caracteres por elemento** — a Hand Talk trunca além do `maxTextSize`; um parágrafo por elemento, nunca um paredão de texto num nó só.
- **MUST NOT** fragmentar uma frase em vários elementos por estilo (correntes de `<span>`, versos de `<br>`): a captura é por elemento, e fragmentos traduzem sem contexto.
- **Expanda siglas na primeira ocorrência** e marque-as com `<abbr title="…">` (SC 3.1.4): palavra ausente do dicionário de sinais é **soletrada letra a letra** (datilologia) — a frustração mais relatada por quem usa Libras com avatares.
- O microcopy segue linguagem simples — frases curtas, ordem direta, uma ideia por frase ([Cognitiva §6](guide-cognitive.md)): serve quem lê na segunda língua *e* melhora de forma mensurável a qualidade da tradução automática.

## 3. A janela de Libras (quando há mídia)

- Vídeo pré-gravado com trilha de áudio **SHOULD** oferecer **janela de interpretação em Libras** — SC 1.2.6 (AAA), recomendação 5.14.6 da ABNT NBR 17225, e exigência dura recorrente em compras públicas brasileiras. Legenda não a substitui: legenda é português, a segunda língua do usuário.
- A janela segue as convenções de radiodifusão (NBR 15290): intérprete visível da cintura para cima, contraste com o fundo, sem sobreposição a conteúdo visual essencial.

## 4. Onde o avatar para

Um avatar automático não reproduz a gramática facial da Libras — negação, interrogação e intensidade são faciais na língua — e a comunidade de intérpretes (ACATILS, 2025) rejeita formalmente avatares como substitutos de intérpretes.

- Para **conteúdo crítico** — saúde, jurídico, financeiro, avaliações — forneça vídeo com **intérprete humano**; o widget é complemento, nunca a resposta.
- **MUST NOT** apresentar o widget de tradução como o que torna o site "acessível em Libras" — declare a natureza de melhor esforço na página de acessibilidade. (O anti-pattern de overlay, core §6, é a mesma falha com outra roupa.)

## 5. Base legal (Brasil)

A Libras é língua nacional reconhecida (Lei 10.436/2002 + Decreto 5.626/2005); a acessibilidade de sites é exigida pelo **art. 63 da LBI** (Lei 13.146/2015), com a ABNT NBR 17225:2025 como lastro técnico — ver [Governança §6.1](guide-governance.md).

*Critérios de sucesso cobertos: 1.2.6 Língua de Sinais — Pré-gravada (AAA) · 1.1.1 Conteúdo Não Textual (A) · 3.1.1 Idioma da Página (A) · 3.1.2 Idioma das Partes (AA) · 3.1.4 Abreviações (AAA) · 3.1.5 Nível de Leitura (AAA)*
