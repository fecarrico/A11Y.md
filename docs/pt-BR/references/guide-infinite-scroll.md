# Guia de Infinite Scroll & Paginação

> **Escopo:** Feeds, listas sem fim, paginação automática.

## 0. A regra da qual todas as outras decorrem

**"Carregar mais" é o padrão acessível; infinite scroll é a exceção que precisa merecer.** Buscar conteúdo automaticamente no scroll destrói três coisas em silêncio: o **rodapé** (alcançável só no instante antes de fugir), a **barra de rolagem** como senso de posição e tamanho, e o **botão Voltar** (retorne, e você está no topo de uma lista mais curta). Um botão devolve a quem usa teclado um ponto de parada, a quem usa leitor de tela um ponto de anúncio, e a todo mundo o rodapé.

1. **Prefira o botão "Carregar mais" explícito.** Depois da ativação, o foco vai para o **primeiro item novo** — nunca volta ao topo, nunca fica preso num botão que pulou de lugar.
2. **Se for carregar automaticamente:** anuncie cada lote por região de status polida, desfecho e não evento — *"mais 20 resultados, 60 de 200"* — e nunca item a item. O sentinela que dispara o carregamento não é focável nem entra na árvore de acessibilidade.
3. **Acrescentar nunca move a pessoa.** Itens novos entram *depois* da posição de leitura atual; reordenar ou rerenderizar a lista existente no meio da leitura é mudança de contexto que ninguém pediu.
4. **A posição é recuperável:** Voltar retorna à mesma posição com os mesmos itens (history state); nomes de item ou `aria-setsize`/`aria-posinset` carregam o *"n de m"* onde o total é conhecido — "em algum lugar de uma lista sem fim" vira um lugar endereçável.
5. **O rodapé continua alcançável.** Se o conteúdo cresce sozinho, ou pare o carregamento automático depois de alguns lotes (trocando para o botão), ou ofereça um atalho para pular o feed — rodapé que foge quando você se aproxima é conteúdo que existe e não pode ser usado (Princípio Zero).
6. **`role="feed"`** é o container certo para um feed de verdade (fluxo de artigos): deixa o leitor de tela navegar entre artigos enquanto o carregamento continua; cada artigo carrega `aria-posinset`/`aria-setsize`.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma lista com botão Carregar mais, QUANDO pressiono `Enter` nele, ENTÃO o foco pousa no primeiro item novo — não no topo, não no botão.
- QUANDO o conteúdo carrega sozinho enquanto desço, ENTÃO o foco fica onde estava e nenhum gatilho invisível recebe `Tab`.
- QUANDO passo da lista com `Tab`, ENTÃO alcanço o rodapé — um botão Carregar mais ou um atalho de pular o feed me leva lá antes de a lista crescer.
- QUANDO abro um item e volto, ENTÃO estou na mesma posição, com os mesmos itens carregados.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO aciono Carregar mais, ENTÃO ouço o primeiro item novo, com a posição quando o total é conhecido — "21 de 200".
- QUANDO um lote carrega sozinho, ENTÃO ouço um anúncio só — "mais 20 resultados, 60 de 200" — nunca um por item.
- QUANDO itens novos entram enquanto leio, ENTÃO o que estou lendo não se move nem muda; eles vêm depois.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO toco duas vezes em Carregar mais, ENTÃO o próximo elemento que ouço é o primeiro item novo.
- QUANDO um lote carrega sozinho, ENTÃO ouço um resumo só — "mais 20 resultados, 60 de 200" — e minha posição não muda.
- QUANDO continuo deslizando além da lista, ENTÃO alcanço o rodapé.

*Critérios de sucesso cobertos: 2.4.3 Ordem de Foco (A) · 4.1.3 Mensagens de Status (AA) · 2.1.1 Teclado (A) · 2.4.1 Pular Blocos (A)*
