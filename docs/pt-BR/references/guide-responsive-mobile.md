# Guia de A11y para Web Responsiva & Zoom

> **Escopo:** Layout web, zoom de navegador & toque. Para apps móveis **nativos** (iOS, Android, React Native, Flutter), consulte o [Platform-Native Mapping](guide-platform-native.md) — este guia cobre apenas o navegador.

## Regras Centrais
1. **Redimensionamento de Texto (SC 1.4.4):** A UI MUST NOT quebrar, cortar ou perder função até **200% de zoom de texto**.
2. **Reflow (SC 1.4.10):** O conteúdo MUST refazer o fluxo a **320 CSS px de largura** (equivalente a 400% de zoom num viewport de 1280px) sem rolagem bidimensional — exceto conteúdo que exige layout 2D (tabelas de dados, mapas, gráficos).
3. **Orientação (SC 1.3.4):** MUST NOT travar a orientação em paisagem ou retrato, a menos que essencial.
4. **Alvos de Toque (SC 2.5.8 + Regra da Casa†):** 24×24 CSS px é o piso normativo AA; projete para **44×44px** em superfícies de toque (norma Apple HIG / Material).
5. **Gestos (SC 2.5.1):** Gestos complexos (swipes, multiponto) MUST ter equivalentes simples de ponteiro único.

*† = Regra da Casa: política ergonômica deste padrão além do piso WCAG — ver `A11Y.md` §0.1.*
