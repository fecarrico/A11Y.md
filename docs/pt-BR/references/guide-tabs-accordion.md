# Guia de Tabs & Accordions

> **Escopo:** Divulgação de Conteúdo

## Regras Centrais
1. **Teclado:** Use setas direcionais para abas; tecla Tab para entrar nos painéis (onde ela cai: regra 2).
2. **Foco no painel:** o `Tab` a partir da aba selecionada cai no primeiro conteúdo do painel. Quando o painel não tem nenhum elemento focável, ou abre com conteúdo que não é focável (um parágrafo de abertura, um título), o painel leva `tabindex="0"`; quando abre com um controle, o foco vai para esse controle e o painel não leva `tabindex` *([Padrão de abas do APG](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/), Keyboard Interaction, nota 4)*. Sem a parada, o `Tab` pula o texto de abertura e quem usa leitor de tela cai num controle no meio do painel, sem o que vinha antes; com uma parada desnecessária, ela é uma caixa contornada sem nada para operar. Decida painel por painel, pelo primeiro conteúdo: *todos os painéis* e *nenhum painel* erram em algum lugar.
3. **Roles (Tabs):** `tablist`, `tab`, `tabpanel`.
4. **Roles (Accordion):** Use `<details>` e `<summary>`, ou botões com `aria-expanded` e `aria-controls`.
5. **Aria-selected:** Usado em abas para marcar a ativa.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma lista de abas, QUANDO entro nela com `Tab`, ENTÃO o foco pousa na aba selecionada — uma parada para a lista toda.
- QUANDO pressiono `←`/`→`, ENTÃO o foco anda entre as abas, e só o painel da aba selecionada fica visível.
- QUANDO pressiono `Tab` numa aba, ENTÃO o foco entra no painel dela, não na próxima aba: no primeiro controle quando o painel abre com um, no próprio painel quando abre com texto — nunca passando por cima do texto de abertura até um controle mais abaixo.
- DADO um acordeão, QUANDO pressiono `Enter` ou `Espaço` num cabeçalho, ENTÃO o painel dele abre ou fecha e o foco fica no cabeçalho.
- QUANDO um painel está fechado, ENTÃO `Tab` pula o conteúdo dele.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego a uma aba, ENTÃO ouço o nome dela, "aba, 1 de 3" e "selecionada" na ativa.
- QUANDO entro no painel com `Tab`, ENTÃO ouço o conteúdo dele, e é o da aba selecionada.
- QUANDO chego a um cabeçalho de acordeão, ENTÃO ouço o nome, "botão" e "recolhido" ou "expandido"; ao acionar, ouço o novo estado.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo pela lista de abas, ENTÃO cada aba diz "aba, n de 3", e tocar duas vezes numa delas a torna "selecionada", com o painel logo em seguida.
- QUANDO toco duas vezes num cabeçalho de acordeão, ENTÃO ouço "expandido" e deslizar alcança o conteúdo; um novo toque duplo diz "recolhido" e o conteúdo some.
