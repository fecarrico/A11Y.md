# Guia de Acessibilidade: Navigation

A navegação (Navigation) deve ser consistente, previsível (predictable) e fácil de descobrir (discoverable).

## Bons Exemplos (Good Examples)

### 1. Navegação Semântica (Semantic Navigation)
```html
<nav aria-label="Main Navigation">
  <ul>
    <li><a href="/" aria-current="page">Home</a></li>
    <li><a href="/about">About</a></li>
  </ul>
</nav>
```
- **Por quê:** `<nav>` é uma landmark. `aria-current="page"` diz aos usuários qual link representa a localização atual.

### 2. Skip to Content (Pular para o Conteúdo)
```html
<a href="#main-content" class="skip-link">Skip to main content</a>
...
<main id="main-content">...</main>
```
- **Por quê:** Permite que usuários de teclado ignorem links de navegação repetitivos e vão direto para o conteúdo principal.

## Maus Exemplos (Bad Examples)

### 1. Menus Aninhados (Apenas no Hover)
- **Implicação:** Menus que aparecem apenas ao passar o mouse (hover) são inacessíveis para usuários de teclado e dispositivos touch. Eles exigem JS para alternar o estado via click ou focus.

### 2. Links Não-Padrão
```html
<span onclick="window.location='/new-page'">Go to Page</span>
```
- **Implicação:** Isto não é uma tag âncora (`<a>`). Não possui foco, não possui role de "link" e não pode ser aberto em uma nova aba.

## Implicações de Acessibilidade
- **Searchability:** Landmarks de navegação adequadas permitem que usuários de screen reader pulem diretamente para a seção de navegação usando teclas de atalho.
- **Predictability:** Manter a navegação no mesmo lugar e na mesma ordem entre as páginas reduz o cognitive load.
