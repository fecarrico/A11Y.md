# Guia de Acessibilidade: Buttons & Actions

> Escopo: Uso semântico de botões, padrões ARIA, interações por teclado e regras de rotulagem.

## Bons Exemplos

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

## Maus Exemplos

### 1. A "Clickable Div"
```html
<div onclick="submit()" class="my-button">Submit</div>
```
- Ver *Clickable Divs* — core §6.

### 2. Rótulos Vagos
```html
<button>Click Here</button>
<button>Learn More</button>
```
- **Implicação:** Usuários de screen reader frequentemente listam todos os botões de uma página para navegar. "Click Here" não fornece nenhum contexto sobre o que o botão realmente faz. Use "Download Report" ou "Leia sobre nossa história" em vez disso.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma página com botões, QUANDO pressiono `Tab`, ENTÃO cada botão recebe foco na sequência, com o anel de foco bem visível.
- QUANDO pressiono `Enter` ou `Espaço` num botão focado, ENTÃO a ação dele executa — a mesma que um clique dispara.
- QUANDO percorro a página com `Tab`, ENTÃO nada que pareça e aja como botão é pulado.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego a um botão com `Tab`, ENTÃO ouço o nome dele seguido de "botão" — nunca "clicável" nem um "botão" sem nome.
- QUANDO chego a um botão só de ícone, ENTÃO ouço o que ele faz ("Fechar modal"), não o ícone nem um nome de arquivo.
- QUANDO abro a lista de botões do leitor de tela, ENTÃO cada nome diz o que o botão faz fora de contexto — nada de "Clique aqui" ou "Saiba mais".

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo até um botão, ENTÃO ouço o nome dele, depois "botão", e tocar duas vezes executa a ação.
- QUANDO deslizo até um botão só de ícone, ENTÃO ouço o nome da ação, nunca "botão sem rótulo".
