# Guia de Acessibilidade: Buttons & Actions

> Escopo: Uso semântico de botões, padrões ARIA, interações por teclado e regras de rotulagem.

## Bons Exemplos (Good Examples)

### 1. Elemento Native Button
```html
<button type="button" class="btn-primary">
  Submit Application
</button>
```
- **Por quê:** Elementos `<button>` nativos possuem suporte embutido para teclado (Enter/Space) e são automaticamente identificados como "button" pelos screen readers (leitores de tela).

### 2. Icon Buttons com Texto
```html
<button aria-label="Close modal">
  <svg>...</svg>
</button>
```
- **Por quê:** Para botões sem texto visível, o `aria-label` fornece o contexto necessário para usuários de screen reader.

## Maus Exemplos (Bad Examples)

### 1. A "Clickable Div"
```html
<div onclick="submit()" class="my-button">Submit</div>
```
- **Implicação:** Isso é invisível para usuários de teclado (sem tab focus) e screen readers (sem a role "button"). Exige excesso de JS para consertar o que o HTML faz de graça.

### 2. Vague Labels (Rótulos Vagos)
```html
<button>Click Here</button>
<button>Learn More</button>
```
- **Implicação:** Usuários de screen reader frequentemente listam todos os botões de uma página para navegar. "Click Here" não fornece nenhum contexto sobre o que o botão realmente faz. Use "Download Report" ou "Leia sobre nossa história" em vez disso.

## Implicações de Acessibilidade
- **Affordance:** Botões visualmente distintos ajudam usuários com deficiências cognitivas a identificar pontos de interação.
- **Precisão:** Áreas de clique grandes (Target Size min 44x44px) são essenciais para usuários mobile e pessoas com deficiências motoras.
