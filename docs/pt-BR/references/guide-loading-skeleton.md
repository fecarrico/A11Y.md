# Guia de Loading, Skeletons & Conteúdo Condicionado a JS

> **Escopo:** Estados de carregamento, skeleton screens, spinners — e conteúdo cuja visibilidade um script controla, que é onde um estado de carregamento vira barreira em silêncio.

## 0. A regra da qual todas as outras decorrem

**Estado de carregamento é promessa, não conteúdo: anuncie a espera uma vez, anuncie o desfecho uma vez — e nunca deixe a promessa ser a única coisa que a página consegue mostrar.** Os dois modos de falha são opostos e igualmente comuns: o skeleton *mudo* (quem usa leitor de tela age sobre uma página meio carregada, ou espera sem sinal nenhum de que algo acontece) e o *tagarela* (cada shimmer e re-render anunciado). Um status na entrada, um status na saída.

1. **Marque a região que espera, não o mundo:** `aria-busy="true"` no container sendo atualizado, removido quando o conteúdo chega.
2. **Um status na entrada, um na saída:** uma região `role="status"` (presente no DOM antes da mensagem) anuncia *"Carregando resultados"*, depois o desfecho — *"12 resultados carregados"*. Nunca `role="alert"` para progresso, nunca um anúncio por bloco de skeleton.
3. **Skeleton é cenografia:** `aria-hidden="true"` nos blocos de placeholder. Skeleton na árvore de acessibilidade é conteúdo que não diz nada.
4. **O pulso respeita `prefers-reduced-motion`** — um shimmer de página inteira é exatamente o movimento ambiente que a preferência existe para parar.
5. **Nunca mova o foco porque algo carregou** — anuncie e deixe a pessoa chegar. Se o foco dela estava dentro da região substituída, mova-o ao ancestral estável mais próximo, não ao topo.
6. **Spinner não é progresso:** passado um instante, diga o que está acontecendo; quando a fração é mensurável, use um `<progress>` de verdade com rótulo.

## Conteúdo condicionado a JS — onde mora o anti-pattern do §6

*Conteúdo Refém do JavaScript* (`A11Y.md` §6) é um estado de carregamento que nunca se resolve. A animação de entrada escrita como `opacity: 0` no CSS e revelada por script renderiza a página **vazia** quando o script falha, é bloqueado (proxy corporativo, extensão, CSP) ou ainda não rodou — conteúdo no DOM, invisível para todo mundo, e invisível para todo verificador, porque no navegador do verificador o script rodou.

- **O estado renderizado por padrão é o legível.** Duas formas corretas: condicionar a animação a uma classe que um **script inline pré-paint** remove (`<html class="no-js">` → o script a tira antes do primeiro paint; o CSS só anima quando a classe some), ou partir do visível e animar *a partir* do visível.
- **Revelar no scroll é a mesma armadilha:** conteúdo abaixo da dobra existe para leitores, impressão e busca *antes* de qualquer `IntersectionObserver` disparar — o observer adiciona a animação, nunca adiciona o conteúdo.
- **`<noscript>` não é a correção.** O caso que falha costuma ser JavaScript *ligado* porém quebrado, bloqueado ou atrasado — um bloco `<noscript>` não ajuda nenhum desses.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 4.1.3 Mensagens de Status | AA | espera anunciada uma vez, desfecho anunciado uma vez |
| 2.4.3 Ordem de Foco | A | carregar nunca rouba nem encalha o foco |
| 1.1.1 / Princípio Zero | A | conteúdo nunca condicionado a um script que pode não rodar |
| Motion (Regra da Casa†) | — | o pulso do skeleton honra `prefers-reduced-motion` |

## Dica para a IA:

Carregue a página duas vezes: uma com JavaScript desligado, outra com ele ligado e estrangulado. Em nenhum momento a página pode estar em branco enquanto o conteúdo dela está no DOM. Depois passe um leitor de tela por um ciclo de carregamento — você deve ouvir exatamente duas coisas: que a espera começou, e o que chegou.
