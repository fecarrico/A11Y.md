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

*Critérios de sucesso cobertos: 2.4.3 Ordem de Foco (A) · 4.1.3 Mensagens de Status (AA) · 2.1.1 Teclado (A) · 2.4.1 Pular Blocos (A)*
