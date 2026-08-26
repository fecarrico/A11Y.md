# Guia de Mapeamento de Frameworks

> **Padrão Alvo:** Equivalência Semântica | **Escopo:** Geração de Código por IA

O padrão `A11Y.md` usa a sintaxe **React/TSX** em seus exemplos devido à sua popularidade. No entanto, os requisitos subjacentes de acessibilidade (atributos ARIA, HTML semântico, eventos de teclado) são **agnósticos a framework**.

Quando um agente de IA gera ou revisa código, ele **MUST transpor** esses padrões para o framework ativo do projeto, preservando a equivalência semântica.

> [!IMPORTANT]
> **Escopo: apenas frameworks web.** Atributos ARIA e eventos de DOM não existem em plataformas nativas. Para alvos iOS, Android, React Native ou Flutter, use o guia [Platform-Native Mapping](guide-platform-native.md) — transpor ARIA para código nativo é uma violação da regra *Platform Awareness* do contrato.

## Regras Centrais de Tradução

1. **Nativo sobre Customizado:** Sempre prefira a implementação nativa do framework para um elemento semântico em vez de construir um do zero.
2. **Reatividade:** Mapeie estados dinâmicos ARIA (ex: `aria-expanded={isOpen}`) para a sintaxe de binding de estado do framework.
3. **Eventos:** Mapeie ouvintes de eventos de teclado (ex: `onKeyDown`) para a manipulação de eventos idiomática do framework.

---

## 1. Vue.js / Nuxt
- **State Binding:** Use `v-bind` ou `:` (ex: `:aria-expanded="isOpen"`).
- **Event Handling:** Use `@keydown` (ex: `@keydown.enter="submit"`). Os modificadores de eventos do Vue são altamente recomendados para acessibilidade (ex: `@keydown.esc`, `@keydown.prevent.space`).
- **Foco:** Use `ref` para gerenciamento de foco (`element.value.focus()`).

## 2. Angular
- **State Binding:** Use colchetes `[attr.aria-expanded]="isOpen"`. Note que o prefixo `attr.` é obrigatório para atributos ARIA no Angular.
- **Event Handling:** Use parênteses `(keydown.enter)="submit()"`.
- **Foco:** Use `@ViewChild` e `ElementRef` para gerenciamento de foco.

## 3. Svelte
- **State Binding:** Binding direto `aria-expanded={isOpen}`.
- **Event Handling:** Use `onkeydown` (Svelte 5, atributos de evento). A forma `on:keydown` é a sintaxe de diretiva do Svelte 4 — ainda aceita, porém legada.
- **Diretivas:** Use a diretiva `use:` para trapping de foco complexo ou lógicas de acessibilidade reutilizáveis (ex: `use:focusTrap`).

## 4. SolidJS
- **State Binding:** Similar ao React `aria-expanded={isOpen()}`. Note a invocação do signal.
- **Event Handling:** Similar ao React `onKeyDown={(e) => ...}`.

## 5. Vanilla JS / Web Components (Lit)
- **State Binding:** No Lit, use `.ariaExpanded=${this.isOpen}` ou `?aria-hidden=${this.isHidden}` para atributos booleanos.
- **Shadow DOM:** Tenha extremo cuidado com `aria-controls` e `aria-describedby` através das fronteiras do Shadow DOM, pois referências de ID não as cruzam. Use `ElementInternals` quando aplicável.

---

## IDs que cruzam a fronteira de componentes

Todo framework moderno tem um gerador de ID estável para SSR (`useId` no React 18+ e no Vue 3.5+, equivalentes nos demais). Ele resolve colisão de identificadores — e cria uma armadilha no momento em que dois componentes precisam **se referenciar**.

### ❌ Incorreto

```tsx
// Toolbar.tsx
const panelId = useId();                    // gera um valor
return <button aria-controls={panelId} aria-expanded={open}>Filtros</button>;

// Panel.tsx
const panelId = useId();                    // gera OUTRO valor
return <div id={panelId}>…</div>;
```

O `aria-controls` aponta para um `id` que não existe. Cada chamada de `useId()` é independente — nada faz dois componentes chegarem ao mesmo valor. E o defeito **passa** no axe e no Lighthouse: eles validam a sintaxe do atributo, não resolvem o destino da referência entre componentes. Esse modo de falha é o **inverso do ARIA Soup**: lá, ARIA é adicionado onde a semântica nativa bastava; aqui o ARIA é sintaticamente correto e vazio no destino — o leitor de tela segue o ponteiro e não encontra nada.

### ✅ Correto

```tsx
// Toolbar.tsx — um lado gera, o outro recebe
const panelId = useId();
return (
  <>
    <button aria-controls={panelId} aria-expanded={open}>Filtros</button>
    <Panel id={panelId} />
  </>
);

// Panel.tsx
export function Panel({ id }: { id: string }) {
  return <div id={id}>…</div>;
}
```

Vale para `aria-controls`, `aria-labelledby`, `aria-describedby` e `aria-activedescendant`, em qualquer framework: **o identificador tem uma origem única e desce por propriedade.** Se os componentes estão distantes na árvore, o `id` sobe para o estado compartilhado ou para o contexto — o que não muda é ele ser gerado uma vez só.

*Ver o anti-padrão **Referência ARIA Órfã** na Seção 6 do arquivo central.*

---
