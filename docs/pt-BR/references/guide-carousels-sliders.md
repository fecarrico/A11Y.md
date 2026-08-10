# Guia de Carrosséis & Sliders

> **Escopo:** Conteúdo Deslizante

## Regras Centrais
1. **Pausa:** Carrosséis automáticos MUST ter botão de pausar — SC 2.2.2, Nível A, para qualquer movimento automático acima de 5 segundos. *(Ver [Mídia Temporal & Movimento](guide-media.md) para o critério e o comportamento sob reduced-motion.)*
2. **Botões:** Botões Próximo/Anterior MUST ser `button` com aria-labels.
3. **Slides Ocultos:** Slides fora da tela MUST ser removidos da ordem de tabulação com o atributo `inert`. O `tabindex="-1"` afeta **apenas o elemento em que está** e deixa focáveis os botões e links *dentro* do slide — que é exatamente o foco invisível que esta regra existe para evitar. O `inert` remove a subárvore inteira do foco e da árvore de acessibilidade, tornando o `aria-hidden` desnecessário (e um controle dentro de subárvore `aria-hidden` seria inalcançável de qualquer forma).