# Guia de Skeletons & Loading

> **Escopo:** Estados de Carregamento

## Regras Centrais
1. **Aria-busy:** Use `aria-busy="true"` no container sendo atualizado.
2. **Anúncio:** Leitores de tela devem ser informados via aria-live.
3. **Movimento:** Respeite `@media (prefers-reduced-motion)` em animações de pulso.