# Accessibility: Visual Perception, Color & Contrast

Este documento detalha como garantir que interfaces sejam compreensíveis independentemente da capacidade de percepção de cores do usuário, utilizando modelos matemáticos modernos e técnicas de redundância.

## 1. Modelos de Cor e Distância Perceptual
Para garantir que duas cores sejam "distinguíveis", não basta olhar para o código Hex. Usamos o espaço de cor **OKLCH** (Luminance, Chroma, Hue), que é perceptualmente uniforme.

- **Diferença de Luminância (L):** É o fator mais importante para legibilidade. O contraste deve vir primeiro da diferença entre "claro" e "escuro", e só depois do Matiz (Hue).
- **Delta E (ΔE):** Medida de distância entre duas cores.
    - **ΔE > 20:** Diferença perceptível para a maioria dos usuários.
    - **ΔE > 40:** Diferença de alta segurança para usuários daltônicos.

## 2. Redundância Visual e Padrões (Graphs Case)
Gráficos e dashboards **MUST NOT** depender exclusivamente de cores para diferenciar séries de dados.

### Estratégias para Gráficos:
- **Linhas:** Use `dashed`, `dotted` e espessuras diferentes.
- **Pontos (Markers):** Use formas distintas (círculos, triângulos, quadrados, X).
- **Áreas (Charts):** Use texturas/hatch patterns em vez de cores sólidas adjacentes.
- **Diretriz:** Se o gráfico for impresso em preto e branco, ele ainda deve ser interpretável.

## 3. Contraste Moderno (Introdução ao APCA)
Enquanto a WCAG 2.1/2.2 usa o ratio estático (ex: 4.5:1), o **APCA** (Advanced Perceptual Contrast Algorithm) é o modelo sugerido para o futuro (WCAG 3).

- **Por que importa:** O APCA considera que o texto branco no fundo preto e o preto no fundo branco não têm o mesmo impacto visual (efeitos de irradiação).
- **Aplicação Prática:** Use o APCA para validar a legibilidade de fontes muito finas ou tamanhos pequenos, onde o ratio de 4.5:1 pode ser enganoso.
- **Dica:** Procure um score **Lc (Lightness Contrast)** de pelo menos 60 para corpo de texto.

## 4. Estratégias de Redundância Semântica
- **Cor + Ícone:** Toda mensagem de erro ou sucesso deve vir acompanhada de um ícone universal (Checkmark, Warning, Info).
- **Labels Diretas:** Em gráficos de pizza ou barras, coloque a label diretamente sobre ou ao lado do elemento, evitando legendas distantes que exigem correspondência de cores.

## 5. Protocolo de Verificação (QA)
Para considerar a tarefa "Done" em termos de percepção visual:
1. **Grayscale Test:** Desative as cores da tela. Você ainda consegue entender a hierarquia?
2. **Simulator Check:** Use ferramentas como **Color Oracle** ou simuladores de browser para checar:
    - **Protanopia/Deuteranopia:** (Deficiência no vermelho/verde - mais comum).
    - **Tritanopia:** (Deficiência no azul/amarelo - raridade).
3. **Luminance Check:** Garanta que a diferença de Luminance (L no OKLCH) entre fundo e texto seja significativa.
