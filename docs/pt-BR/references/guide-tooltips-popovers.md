# Guia de Tooltips & Popovers

> **Escopo:** Informação Contextual

## Regras Centrais
1. **Gatilho:** MUST receber foco (botão, link).
2. **Hover/Foco:** MUST aparecer via mouse e via foco de teclado.
3. **Dispensável (SC 1.4.13):** MUST fechar com a tecla `Escape` **sem mover o foco** — quem usa ampliação de tela precisa remover a sobreposição sem perder o lugar.
4. **Hoverable (SC 1.4.13):** MUST não sumir quando o ponteiro se move para cima do próprio tooltip — o caminho até ele passa por fora do gatilho.
5. **Persistente (SC 1.4.13):** MUST permanecer visível até que o usuário o dispense, o gatilho perca hover/foco, ou a informação deixe de ser válida. MUST NOT desaparecer sozinho por tempo.

> **SC 1.4.13 Conteúdo em Hover ou Foco (AA)** é composto exatamente pelas três condições acima. Conteúdo que aparece no hover e some antes de o usuário alcançá-lo falha o critério mesmo tendo `role="tooltip"` correto.