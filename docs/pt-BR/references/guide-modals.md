# Guia de Acessibilidade: Modals & Dialogs

> Escopo: Focus trapping, elemento dialog nativo, controle por teclado e anti-padrões de modal.

## Bons Exemplos

### 1. Focus Trapping e Labeling
```javascript
// Ao abrir o modal:
// 1. Salve a referência para o elemento que tinha o foco.
// 2. Mova o foco para o título do modal ou primeiro elemento focável.
// 3. Mantenha o foco dentro do modal até ser fechado.
```
```html
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <h2 id="modal-title">Confirm Deletion</h2>
  <button aria-label="Close">X</button>
  ...
</div>
```
- **Por quê:** `role="dialog"` anuncia o padrão e `aria-modal="true"` instrui a **tecnologia assistiva** a ignorar o conteúdo fora do dialog. `aria-labelledby` fornece o contexto.
- ⚠️ **`aria-modal` não é focus trap.** Ele não fala com o navegador e não afeta a tecla `Tab`: sem JavaScript, o foco continua saindo do dialog para a página ao fundo. A contenção é responsabilidade sua — ou use o `<dialog>` nativo do exemplo 2, que a implementa.

### 2. Dialog HTML Nativo
```javascript
// Para abrir um modal, use o método nativo HTMLDialogElement.showModal() sempre que possível. Ele move o foco para dentro do modal automaticamente e o retorna ao elemento acionador quando o modal é fechado.
```
```html
<dialog aria-labelledby="modal-title" closedby="any" id="exampleDialog">
  <h2 id="modal-title">Confirm Deletion</h2>
  <button aria-label="Close" command="close" commandfor="exampleDialog">X</button>
  ...
</dialog>
```
- **Por quê:** O elemento nativo `<dialog>` já vem com todos os recursos de acessibilidade necessários. `closedby="any"` acrescenta o *light dismiss* — fechar clicando fora do dialog; a tecla `Esc` **já funciona nativamente** em qualquer dialog aberto com `showModal()`, sem atributo nenhum. `command="close"` e `commandfor=""` permitem fechar o dialog via botão sem JavaScript, usando a API nativa `invokerCommands`. `aria-labelledby` fornece o contexto.

> ⚠️ **Compatibilidade experimental:** Os atributos `closedby` e `command`/`commandfor` (invokerCommands API) têm suporte apenas no **Chrome 133+**. Verifique o [Can I Use](https://caniuse.com) antes de usar em produção e considere um fallback em JavaScript para outros navegadores.

### 3. Keyboard Control
- **Esc Key:** Deve sempre fechar o modal.
- **Tab:** Deve circular através dos elementos APENAS dentro do modal (Focus Trap).

## Maus Exemplos

### 1. Deixar o Foco para Trás
- Ver *Leaked Focus Traps* — core §6.

### 2. Sem Botão de Fechar
- **Implicação:** Usuários que dependem de screen readers ou possuem deficiências cognitivas podem não saber como sair de um modal se não houver uma ação clara e rotulada de "Close" ou "Fechar".

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma página com um controle que abre um diálogo, QUANDO chego nele com `Tab` e pressiono `Enter`, ENTÃO o diálogo abre e o foco pousa dentro dele — no título ou no primeiro controle.
- QUANDO pressiono `Tab` e `Shift+Tab` repetidamente, ENTÃO o foco circula só pelos controles do diálogo e nunca alcança a página atrás.
- QUANDO pressiono `Esc`, ENTÃO o diálogo fecha e o foco volta ao controle que o abriu.
- QUANDO o diálogo tem dados não salvos e pressiono `Esc` ou Fechar, ENTÃO recebo um pedido de confirmação antes de os dados se perderem.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO o diálogo abre, ENTÃO ouço "diálogo" e o nome acessível dele, depois o título ou o primeiro controle.
- QUANDO leio adiante além do último controle do diálogo, ENTÃO não alcanço o conteúdo da página atrás dele.
- QUANDO aciono Fechar, ENTÃO ouço de novo o controle que abriu o diálogo.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO o diálogo abre, ENTÃO ouço o nome dele, e deslizar move só entre os elementos do diálogo.
- QUANDO toco duas vezes em Fechar, ENTÃO o diálogo some e o foco está de volta no controle de abertura.
