# Guia de Mapeamento de Frameworks

> **Padrão Alvo:** Equivalência Semântica | **Escopo:** Geração de Código por IA

O padrão `A11Y.md` usa a sintaxe **React/TSX** em seus exemplos devido à sua popularidade. No entanto, os requisitos subjacentes de acessibilidade (atributos ARIA, HTML semântico, eventos de teclado) são **agnósticos a framework**.

Quando um agente de IA gera ou revisa código, ele **MUST transpor** esses padrões para o framework ativo do projeto, preservando a equivalência semântica.

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
- **Event Handling:** Use `on:keydown`.
- **Diretivas:** Use a diretiva `use:` para trapping de foco complexo ou lógicas de acessibilidade reutilizáveis (ex: `use:focusTrap`).

## 4. SolidJS
- **State Binding:** Similar ao React `aria-expanded={isOpen()}`. Note a invocação do signal.
- **Event Handling:** Similar ao React `onKeyDown={(e) => ...}`.

## 5. Vanilla JS / Web Components (Lit)
- **State Binding:** No Lit, use `.ariaExpanded=${this.isOpen}` ou `?aria-hidden=${this.isHidden}` para atributos booleanos.
- **Shadow DOM:** Tenha extremo cuidado com `aria-controls` e `aria-describedby` através das fronteiras do Shadow DOM, pois referências de ID não as cruzam. Use `ElementInternals` quando aplicável.

---

## Exemplo de Tradução: Toggle Button

### 🔵 Origem (React/TSX)
```tsx
<button
  aria-pressed={isActive}
  onClick={() => setIsActive(!isActive)}
>
  Alternar
</button>
```

### 🟢 Vue.js
```html
<button
  :aria-pressed="isActive"
  @click="isActive = !isActive"
>
  Alternar
</button>
```

### 🔴 Angular
```html
<button
  [attr.aria-pressed]="isActive"
  (click)="isActive = !isActive"
>
  Alternar
</button>
```

### 🟠 Svelte
```html
<button
  aria-pressed={isActive}
  on:click={() => isActive = !isActive}
>
  Alternar
</button>
```
