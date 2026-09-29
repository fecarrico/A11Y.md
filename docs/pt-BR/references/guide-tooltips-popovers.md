# Guia de Tooltips & Popovers

> **Escopo:** Informação Contextual

## Regras Centrais
1. **Gatilho:** MUST receber foco (botão, link).
2. **Hover/Foco:** MUST aparecer via mouse e via foco de teclado.
3. **Dispensável (SC 1.4.13):** MUST fechar com a tecla `Escape` **sem mover o foco** — quem usa ampliação de tela precisa remover a sobreposição sem perder o lugar.
4. **Hoverable (SC 1.4.13):** MUST não sumir quando o ponteiro se move para cima do próprio tooltip — o caminho até ele passa por fora do gatilho.
5. **Persistente (SC 1.4.13):** MUST permanecer visível até que o usuário o dispense, o gatilho perca hover/foco, ou a informação deixe de ser válida. MUST NOT desaparecer sozinho por tempo.

> **SC 1.4.13 Conteúdo em Hover ou Foco (AA)** é composto exatamente pelas três condições acima. Conteúdo que aparece no hover e some antes de o usuário alcançá-lo falha o critério mesmo tendo `role="tooltip"` correto.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO um controle com tooltip, QUANDO chego nele com `Tab`, ENTÃO o tooltip aparece sem nenhum movimento do mouse.
- QUANDO pressiono `Esc`, ENTÃO o tooltip fecha e o foco fica exatamente onde estava.
- QUANDO deixo o tooltip aberto e espero, ENTÃO ele continua visível — nunca some sozinho por tempo.
- DADO um gatilho de popover, QUANDO pressiono `Enter`, ENTÃO o popover abre sem o mouse, e `Esc` o fecha.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego ao gatilho com `Tab`, ENTÃO ouço o nome dele e em seguida o texto do tooltip, sem precisar abrir nada.
- QUANDO pressiono `Esc`, ENTÃO o tooltip some e o gatilho continua sendo o elemento focado que ouço.
- QUANDO abro um popover, ENTÃO consigo ler o conteúdo dele e alcançar qualquer controle lá dentro.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo até o gatilho, ENTÃO ouço o nome dele e o texto do tooltip juntos.
- QUANDO toco duas vezes num gatilho de popover, ENTÃO o popover abre e deslizar adiante alcança o conteúdo dele.
