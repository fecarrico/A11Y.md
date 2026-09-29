# Guia de Autocomplete & Combobox

> **Escopo:** Buscas e Selects

## Regras Centrais
1. **Roles:** Input MUST ter `role="combobox"`, lista `role="listbox"`, opções `role="option"`.
2. **Aria-expanded:** Alterne `aria-expanded` ao abrir/fechar.
3. **Aria-activedescendant:** Use para focar opções sem tirar foco do input.
4. **Status:** Anuncie quantidade de resultados via `aria-live`.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO um combobox, QUANDO digito, ENTÃO a lista de resultados abre abaixo do campo.
- QUANDO pressiono `↓`/`↑`, ENTÃO o destaque anda pelas opções enquanto o cursor fica no campo — posso continuar digitando.
- QUANDO pressiono `Enter` numa opção destacada, ENTÃO ela preenche o campo e a lista fecha.
- QUANDO saio do campo com `Tab`, ENTÃO a lista fecha e o foco pousa no próximo controle.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego ao campo com `Tab`, ENTÃO ouço o rótulo, "caixa de combinação" e "recolhido".
- QUANDO digito e aparecem resultados, ENTÃO ouço quantos resultados há.
- QUANDO pressiono `↓`, ENTÃO ouço o texto de cada opção ao ser destacada ("Brasil, 1 de 5"), e continuo no campo.
- QUANDO pressiono `Enter`, ENTÃO o campo fica com o valor escolhido e ouço "recolhido".

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO digito no campo, ENTÃO ouço a quantidade de resultados.
- QUANDO deslizo adiante, ENTÃO alcanço as opções uma a uma, cada uma como "opção", e tocar duas vezes numa delas preenche o campo e fecha a lista.
