# Guia de Acessibilidade em Infinite Scroll

> **Escopo:** Paginação e Feeds

## Regras Centrais
1. **Botão Carregar Mais:** Prefira um botão manual a fetch automático via scroll, pois scroll infinito prende usuários de teclado.
2. **Gerenciamento de Foco:** Ao carregar novos itens, avise o usuário via `aria-live`.
3. **Acesso ao Rodapé:** Garanta que usuários consigam passar o feed para chegar no rodapé.