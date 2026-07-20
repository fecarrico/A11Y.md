# Mapeamento de Acessibilidade para Plataformas Nativas

> **Padrão Alvo:** Equivalência Semântica | **Escopo:** iOS (SwiftUI/UIKit), Android (Compose/Views), React Native, Flutter

A camada normativa do `A11Y.md` (Principle Zero, POUR, Perfis de Conformidade, Severidade, Governança) é agnóstica de plataforma — a WCAG 2.2 é escrita para ser neutra em tecnologia, e o [WCAG2ICT](https://www.w3.org/TR/wcag2ict-22/) a mapeia para software não-web. As **referências técnicas**, porém, são web-first. Este guia é a camada de tradução.

## Regras Centrais

1. **Nunca emita idiomas web em plataformas nativas.** Atributos ARIA, roles e pixels CSS não existem em SwiftUI, Compose, React Native ou Flutter. Traduza a *intenção*, não a sintaxe. Inventar híbridos (ex.: `aria-live` no SwiftUI) é violação 🔴 CRITICAL.
2. **Prefira componentes nativos.** Controles padrão da plataforma (Button, Switch, Alert) já vêm com semântica, comportamento de foco e alvos de toque conformes — o equivalente nativo de "prefira HTML semântico".
3. **Alvos de toque:** **44×44pt (Apple HIG)** / **48×48dp (Material)** são as normas das plataformas e satisfazem a Regra da Casa deste padrão por default. O piso WCAG (SC 2.5.8, 24×24) segue valendo para controles desenhados do zero.
4. **Respeite as configurações de acessibilidade do sistema:** escala de fonte (Dynamic Type / unidades `sp` / `textScaler`), Reduzir Movimento e modos de contraste elevado são os equivalentes nativos de zoom, `prefers-reduced-motion` e requisitos de contraste.
5. **Anuncie mudanças dinâmicas.** Toasts, resultados assíncronos e erros de validação MUST ser anunciados pela API de notificação de acessibilidade da plataforma — o equivalente nativo de `aria-live`.

## Tabela de Tradução (intenção semântica → plataforma)

| Intenção web | iOS (SwiftUI) | Android (Compose) | React Native | Flutter |
| :--- | :--- | :--- | :--- | :--- |
| `<button>` / `role="button"` | `Button` ou `.accessibilityAddTraits(.isButton)` | `Button` ou `Modifier.semantics { role = Role.Button }` | `accessibilityRole="button"` | `ElevatedButton` ou `Semantics(button: true)` |
| Nome acessível (`aria-label`, `alt`) | `.accessibilityLabel("…")` | `contentDescription` / `semantics { contentDescription = "…" }` | `accessibilityLabel` | `Semantics(label: "…")` |
| `aria-live` / `role="status"` | `AccessibilityNotification.Announcement("…").post()` (iOS 17+; antes: `UIAccessibility.post(notification: .announcement, …)`) | `Modifier.semantics { liveRegion = LiveRegionMode.Polite }` (`announceForAccessibility` está deprecado na API 36) | `accessibilityLiveRegion` (Android) / `AccessibilityInfo.announceForAccessibility(…)` | `SemanticsService.sendAnnouncement(…)` — prefira semântica de live region no Android |
| Modal + contenção de foco | `.accessibilityAddTraits(.isModal)` (UIKit: `accessibilityViewIsModal`) | `Dialog()` (escopa o foco por default) | `accessibilityViewIsModal` (iOS); esconda o fundo com `importantForAccessibility="no-hide-descendants"` (Android) | `showDialog` (escopo de rota); `Semantics(scopesRoute: true)` para overlays customizados |
| Heading (`<h1>`–`<h6>`) | `.accessibilityAddTraits(.isHeader)` | `Modifier.semantics { heading() }` | `accessibilityRole="header"` | `Semantics(header: true)` |
| Estado desabilitado (`disabled`, `aria-disabled`) | `.disabled(true)` (exposto automaticamente) | `enabled = false` | `accessibilityState={{disabled: true}}` | `Semantics(enabled: false)` ou widget desabilitado |
| Agrupamento de conteúdo relacionado (label + valor) | `.accessibilityElement(children: .combine)` | `Modifier.semantics(mergeDescendants = true) {}` | `accessible={true}` no contêiner | `MergeSemantics` |
| Gerenciamento de foco após navegação | `@AccessibilityFocusState` | `FocusRequester.requestFocus()` | `AccessibilityInfo.sendAccessibilityEvent(handle, 'focus')` | `FocusNode.requestFocus()` |
| `prefers-reduced-motion` | Ambiente `accessibilityReduceMotion` / `UIAccessibility.isReduceMotionEnabled` | Respeite a escala de animação do sistema; evite auto-animação gratuita | `AccessibilityInfo.isReduceMotionEnabled()` | `MediaQuery.of(context).disableAnimations` |
| Zoom de texto (equivalência do SC 1.4.4) | Dynamic Type — use estilos de texto do sistema, nunca tamanhos fixos | Unidades `sp` para texto, nunca `dp` | `allowFontScaling` (default `true` — MUST NOT desabilitar) | `textScaler` do `MediaQuery` — nunca fixe `textScaleFactor: 1.0` |

## Verificação (equivalente nativo da Seção 7)

- [ ] **Passagem de leitor de tela solicitada:** VoiceOver (iOS) / TalkBack (Android) — validação humana; a IA MUST NOT alegar que os executou.
- [ ] **Escala de fonte:** a UI sobrevive ao maior tamanho de fonte do sistema sem truncamento ou sobreposição.
- [ ] **Ordem de foco/swipe:** a navegação sequencial segue a ordem visual/lógica.
- [ ] **Anúncios:** feedback assíncrono audível sem tocar na tela.
