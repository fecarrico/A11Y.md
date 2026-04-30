# Guia de Acessibilidade: Modals & Dialogs

Modais são componentes de alto risco. Eles interrompem o fluxo do usuário e podem "prender" (trap) os usuários se não forem implementados corretamente.

## Bons Exemplos (Good Examples)

### 1. Native HTMLDialogElement (Recomendado)
A maneira mais robusta e acessível de criar um modal é usando o elemento nativo `<dialog>` com o método `showModal()`. Ele gerencia automaticamente o focus trapping, a inércia do background e a tecla Esc.

```html
<dialog id="my-modal" aria-labelledby="modal-title">
  <h2 id="modal-title">Confirm Deletion</h2>
  <form method="dialog">
    <button>Close</button>
  </form>
</dialog>

<script>
  document.getElementById('my-modal').showModal();
</script>
```

### 2. Focus Trapping e Labeling (Custom Div)
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
- **Por quê:** `role="dialog"` e `aria-modal="true"` dizem ao browser para ignorar o resto da página. `aria-labelledby` fornece o contexto.

### 3. Keyboard Control
- **Esc Key:** Deve sempre fechar o modal.
- **Tab:** Deve circular através dos elementos APENAS dentro do modal (Focus Trap).

## Maus Exemplos (Bad Examples)

### 1. Deixar o Foco para Trás (Leaving Focus Behind)
- **Implicação:** Se um modal abre e o foco permanece no acionador ao fundo, um usuário de screen reader pode continuar interagindo com a página "por baixo" do modal, levando a confusões e erros.

### 2. Sem Botão de Fechar (No Close Button)
- **Implicação:** Usuários que dependem de screen readers ou possuem deficiências cognitivas podem não saber como sair de um modal se não houver uma ação clara e rotulada de "Close" ou "Fechar".

## Implicações de Acessibilidade
- **Modality:** Garantir que o usuário saiba que ele está em um "sub-estado" da aplicação.
- **Restoration:** Quando o modal é fechado, o foco MUST retornar para o elemento que o acionou, para que o usuário saiba onde ele está no documento.
