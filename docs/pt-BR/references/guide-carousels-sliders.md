# Guia de Carrosséis & Sliders

> **Escopo:** Carrosséis, banners rotativos, sliders de conteúdo.

## 0. A regra da qual todas as outras decorrem

**O avanço automático é o problema de acessibilidade; todo o resto é um grupo rotulado de slides.** Um carrossel que nunca se move sozinho é um padrão administrável. Um que gira automaticamente briga com a pessoa em três frentes ao mesmo tempo: move conteúdo no meio da leitura (baixa visão, cognitivo), move conteúdo no meio da escuta (leitor de tela) e move a coisa em que o foco estava parado (teclado).

1. **O controle de pausa é requisito, não enfeite** — SC 2.2.2, Nível A, para qualquer movimento automático acima de 5 segundos: um pausar/parar visível e focável, **primeiro na ordem de tabulação do carrossel**, alcançável antes que a rotação tenha mudado qualquer coisa. Sob `prefers-reduced-motion`, o avanço automático simplesmente não começa (ver [Mídia Temporal & Movimento](guide-media.md)).
2. **A rotação para na interação:** hover, foco entrando no carrossel ou um tooltip aberto suspendem o avanço — e **o slide sob o foco da pessoa nunca vai embora dela**.
3. **Estrutura:** container `role="region"` + `aria-roledescription="carousel"` + nome acessível; cada slide `role="group"` + `aria-roledescription="slide"` + um nome que o localiza — *"3 de 8"* ou o título. A posição não pode ser transmitida só pela cor dos pontos (SC 1.4.1).
4. **Controles são botões:** Anterior/Próximo como `<button>` de verdade com nome; os pontos seletores como botões nomeados pelo slide (*"Slide 3: Coleção de primavera"*), o atual marcado com `aria-current`, nunca só pelo preenchimento.
5. **Slides fora da tela ficam `inert`.** `tabindex="-1"` afeta só o elemento em que está — os links e botões *dentro* do slide oculto continuam focáveis, exatamente o foco invisível que esta regra existe para evitar. `inert` remove a subárvore inteira do foco e da árvore de acessibilidade.
6. **Anuncie só as mudanças iniciadas pela pessoa:** uma região polida confirma *"Slide 4 de 8"* depois do Próximo — mas a rotação automática **nunca** é anunciada, ou o carrossel narra a si mesmo por cima de todo o resto da página.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 2.2.2 Pausar, Parar, Ocultar | A | avanço automático acima de 5s tem pausa alcançável |
| 2.1.1 Teclado | A | todos os controles e o conteúdo dos slides operáveis sem mouse |
| 1.4.1 Uso de Cor | A | posição e slide atual nunca só por cor |
| 4.1.2 Nome, Função, Valor | A | carrossel e slides nomeados; estado atual exposto |
| 2.4.3 Ordem de Foco | A | o foco nunca é abandonado num slide que girou embora |

## Dica para a IA:

Entre no carrossel por Tab e espere dez segundos. Se o slide sob o teu foco foi embora sem ti, ou o leitor de tela anunciou uma rotação que ninguém pediu, o componente falha — por mais correto que o ARIA pareça.
