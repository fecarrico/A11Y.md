# Accessibility: Visual Perception, Color & Contrast

> Escopo: Modelo de cores OKLCH, Delta E, contraste APCA, redundância em gráficos e protocolo de QA para daltonismo.

## 1. Modelos de Cor e Distância Perceptual
Para garantir que duas cores sejam "distinguíveis", não basta olhar para o código Hex. Usamos o espaço de cor **OKLCH** (Luminance, Chroma, Hue), que é perceptualmente uniforme.

- **Diferença de Luminância (L):** É o fator mais importante para legibilidade. O contraste deve vir primeiro da diferença entre "claro" e "escuro", e só depois do Matiz (Hue).
- **Delta E (ΔE):** Medida de distância entre duas cores.
    - **ΔE > 20:** Diferença perceptível para a maioria dos usuários.
    - **ΔE > 40:** Diferença de alta segurança para usuários daltônicos.

## 2. Contraste Moderno (Introdução ao APCA)
Enquanto a WCAG 2.1/2.2 usa o ratio estático (ex: 4.5:1), o **APCA** (Advanced Perceptual Contrast Algorithm) é o modelo sugerido para o futuro (WCAG 3).

- **Por que importa:** O APCA considera que o texto branco no fundo preto e o preto no fundo branco não têm o mesmo impacto visual (efeitos de irradiação).
- **Aplicação Prática:** Use o APCA para validar a legibilidade de fontes muito finas ou tamanhos pequenos, onde o ratio de 4.5:1 pode ser enganoso.
- **Dica:** Procure um score **Lc (Lightness Contrast)** de pelo menos 60 para corpo de texto.

## 3. Protocolo de Definição de Paleta

O momento em que as cores nascem é o momento em que o contraste se decide — o benchmark deste padrão encontrou falhas de contraste em todas as condições sem instrução, e contraste é a maior dívida de auditoria da web (WebAIM Million: 83,9% das páginas). Ao criar ou alterar design tokens, paletas ou arquivos de tema, a IA **MUST**:

1. **Enumerar os pares intencionais** — toda combinação texto/fundo e UI/fundo que os tokens vão formar, incluindo estados (hover, foco, desabilitado, erro) e os dois temas quando houver dois.
2. **Calcular o ratio WCAG de cada par no momento da definição** — [`tools/contrast-check.py`](https://github.com/fecarrico/A11Y.md/tree/main/tools) com shell, a fórmula de luminância relativa sem. Nunca "parece escuro o bastante".
3. **Ajustar luminância, não só matiz**, até todo par superar o piso do perfil ativo (core §0.1).
4. **Registrar a matriz de pares** (par → ratio medido) no `A11Y-DECISIONS.md`; os valores alimentam o `REPORT.md` §1.

Paleta validada no nascimento não reprova na auditoria; paleta validada só na auditoria reprova primeiro em produção.

## 4. Protocolo de Verificação (QA)
Para considerar a tarefa "Done" em termos de percepção visual:
1. **Grayscale Test:** Desative as cores da tela. Você ainda consegue entender a hierarquia?
2. **Simulator Check:** Use ferramentas como **Color Oracle** ou simuladores de browser para checar:
    - **Protanopia/Deuteranopia:** (Deficiência no vermelho/verde - mais comum).
    - **Tritanopia:** (Deficiência no azul/amarelo - raridade).
3. **Luminance Check:** Garanta que a diferença de Luminance (L no OKLCH) entre fundo e texto seja significativa.
