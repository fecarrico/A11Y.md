# Guia de Autocomplete & Combobox

> **Escopo:** Buscas e Selects

## Regras Centrais
1. **Roles:** Input MUST ter `role="combobox"`, lista `role="listbox"`, opções `role="option"`.
2. **Aria-expanded:** Alterne `aria-expanded` ao abrir/fechar.
3. **Aria-activedescendant:** Use para focar opções sem tirar foco do input.
4. **Status:** Anuncie quantidade de resultados via `aria-live`.