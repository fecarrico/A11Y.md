# Guia de Tree View & Hierarquia

> **Escopo:** Tree views, exploradores de arquivo, seletores de categoria aninhados e qualquer hierarquia expansível — adote em vez de reinventar (`A11Y.md` §6).

## 0. Primeiro pergunte se aquilo deveria ser uma árvore

A maioria das "árvores" geradas é menu de navegação vestindo `role="tree"` — e a função deixa tudo *pior*: ela avisa à tecnologia assistiva que aquilo é um widget de seleção com navegação por setas, então os comandos normais de leitura da pessoa param de se comportar normalmente e os links deixam de ser anunciados como links.

| O que aquilo realmente é | Marcação correta |
| :--- | :--- |
| navegação do site ou da documentação, com links | `<nav>` + `<ul>` aninhada + `<a>` — seções expansíveis usam `aria-expanded` num `<button>` |
| seções de conteúdo que abrem e fecham | disclosure / acordeão — ver [Tabs & Acordeões](guide-tabs-accordion.md) |
| um filtro com checkboxes aninhados | `<fieldset>` aninhado + checkboxes, não árvore |
| **selecionar ou explorar itens numa hierarquia** (explorador de arquivos, seletor de organograma, painel de camadas) | **`role="tree"`** — este guia |

Se a pessoa está *indo a algum lugar*, é navegação. Se está *escolhendo algo* dentro de uma hierarquia, é árvore.

## 1. O padrão

Siga o [padrão Tree View da APG](https://www.w3.org/WAI/ARIA/apg/patterns/treeview/). O contrato estrutural:

```tsx
<ul role="tree" aria-label="Arquivos do projeto">
  <li role="treeitem" aria-expanded={aberto} aria-selected={selecionado} tabIndex={focado ? 0 : -1}>
    <span>src</span>
    <ul role="group">
      <li role="treeitem" aria-selected={false} tabIndex={-1}>index.tsx</li>
    </ul>
  </li>
</ul>
```

1. **`aria-expanded` só em nós que têm filhos.** Numa folha, é mentira: o leitor anuncia "recolhido" para algo que nunca vai abrir.
2. **Filhos vivem num `role="group"`**, aninhado dentro do `treeitem` pai — não como irmão.
3. **Quando o DOM não é a árvore inteira** (listas virtualizadas, ramos carregados sob demanda), todo nó visível **MUST** carregar `aria-level`, `aria-setsize` e `aria-posinset`. Sem isso o leitor anuncia "1 de 3" para um nó que é o nono de quarenta, e a profundidade desaparece por completo.
4. **Uma parada de tabulação para a árvore inteira.** O nó focado tem `tabindex="0"`, todos os outros `-1` — foco itinerante. Uma árvore com quarenta paradas de tabulação é exatamente a falha que este padrão existe para evitar.

## 2. Teclado

| Tecla | Comportamento |
| :--- | :--- |
| ↑ / ↓ | nó **visível** anterior / seguinte (pulando subárvores recolhidas) |
| → | expande um nó fechado; vai ao primeiro filho se já estiver aberto |
| ← | recolhe um nó aberto; vai ao pai se já estiver fechado |
| `Home` / `End` | primeiro / último nó visível |
| `Enter` | ativa (abre o arquivo, aplica a escolha) |
| `Espaço` | seleciona, onde seleção é separada de ativação |
| a–z | busca incremental pelo próximo nó com aquela inicial |
| `*` | expande todos os irmãos do nível atual |

**Expandir não é selecionar.** Um nó pode estar aberto e não selecionado, ou selecionado e fechado; `aria-expanded` e `aria-selected` são independentes, e uma árvore que confunde os dois não consegue expressar "abri esta pasta para olhar dentro sem escolhê-la".

## 3. Seleção múltipla e carregamento assíncrono

- Árvores de seleção múltipla declaram `aria-multiselectable="true"` no `tree`, e **todo** nó selecionável carrega `aria-selected` — `true` *ou* `false`. Colocar só no nó selecionado torna o resto inselecionável para a API.
- Um ramo carregando filhos anuncia a espera (`aria-busy="true"` no nó, e uma região de status polida para o resultado: *"src expandido, 12 itens"*). Expansão assíncrona silenciosa é o motivo mais comum de quem usa leitor de tela achar que a árvore quebrou.
- Indentação é só visual. Profundidade chega à tecnologia assistiva por aninhamento ou por `aria-level` — nunca por padding.

*Critérios de sucesso cobertos: 1.3.1 Informação e Relações (A) · 2.1.1 Teclado (A) · 2.4.3 Ordem de Foco (A) · 4.1.2 Nome, Função, Valor (A) · 4.1.3 Mensagens de Status (AA)*
