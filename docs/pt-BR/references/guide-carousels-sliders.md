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

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO um carrossel que gira sozinho, QUANDO entro nele com `Tab`, ENTÃO a primeira parada é o controle de pausa e a rotação para enquanto o foco está dentro.
- QUANDO pressiono `Enter` em Pausar, ENTÃO a rotação para.
- QUANDO sigo com `Tab`, ENTÃO o foco alcança só Anterior, Próximo, os pontos e os links do slide visível — nada dentro de um slide fora da tela.
- QUANDO o foco está num link dentro de um slide, ENTÃO esse slide nunca vai embora de mim.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego ao carrossel, ENTÃO ouço "carrossel" e o nome dele, e cada slide como "slide" com a posição — "3 de 8" — ou o título.
- QUANDO aciono Próximo, ENTÃO ouço "Slide 4 de 8" uma vez.
- QUANDO o carrossel gira sozinho, ENTÃO não ouço nada sobre isso.
- QUANDO chego a um ponto seletor, ENTÃO ouço "botão", o slide a que ele leva e "atual" no ativo.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo para dentro do carrossel, ENTÃO o primeiro elemento que ouço é o controle de pausa.
- QUANDO continuo deslizando, ENTÃO passo só pelo conteúdo do slide visível, nunca por slides fora da tela.
- QUANDO toco duas vezes em Próximo, ENTÃO ouço a nova posição do slide; QUANDO ele gira sozinho, ENTÃO não ouço nada.

*Critérios de sucesso cobertos: 2.2.2 Pausar, Parar, Ocultar (A) · 2.1.1 Teclado (A) · 1.4.1 Uso de Cor (A) · 4.1.2 Nome, Função, Valor (A) · 2.4.3 Ordem de Foco (A)*
