# Guia de Tabs & Accordions

> **Escopo:** Divulgação de Conteúdo

## Regras Centrais
1. **Teclado:** Use setas direcionais para abas; tecla Tab para entrar nos painéis.
2. **Roles (Tabs):** `tablist`, `tab`, `tabpanel`.
3. **Roles (Accordion):** Use `<details>` e `<summary>`, ou botões com `aria-expanded` e `aria-controls`.
4. **Aria-selected:** Usado em abas para marcar a ativa.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma lista de abas, QUANDO entro nela com `Tab`, ENTÃO o foco pousa na aba selecionada — uma parada para a lista toda.
- QUANDO pressiono `←`/`→`, ENTÃO o foco anda entre as abas, e só o painel da aba selecionada fica visível.
- QUANDO pressiono `Tab` numa aba, ENTÃO o foco entra no painel dela, não na próxima aba.
- DADO um acordeão, QUANDO pressiono `Enter` ou `Espaço` num cabeçalho, ENTÃO o painel dele abre ou fecha e o foco fica no cabeçalho.
- QUANDO um painel está fechado, ENTÃO `Tab` pula o conteúdo dele.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego a uma aba, ENTÃO ouço o nome dela, "aba, 1 de 3" e "selecionada" na ativa.
- QUANDO entro no painel com `Tab`, ENTÃO ouço o conteúdo dele, e é o da aba selecionada.
- QUANDO chego a um cabeçalho de acordeão, ENTÃO ouço o nome, "botão" e "recolhido" ou "expandido"; ao acionar, ouço o novo estado.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo pela lista de abas, ENTÃO cada aba diz "aba, n de 3", e tocar duas vezes numa delas a torna "selecionada", com o painel logo em seguida.
- QUANDO toco duas vezes num cabeçalho de acordeão, ENTÃO ouço "expandido" e deslizar alcança o conteúdo; um novo toque duplo diz "recolhido" e o conteúdo some.
