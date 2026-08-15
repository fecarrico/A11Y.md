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
| **Ação que só existe como gesto** (swipe action, menu de long-press, arraste) | `.accessibilityAction(named: Text("Arquivar")) { … }` (UIKit: `accessibilityCustomActions` = `[UIAccessibilityCustomAction(name:actionHandler:)]`) | `Modifier.semantics { customActions = listOf(CustomAccessibilityAction(label) { true }) }` | `accessibilityActions={[{name: 'archive', label: 'Arquivar'}]}` + `onAccessibilityAction` | `Semantics(customSemanticsActions: {CustomSemanticsAction(label: 'Arquivar'): () { … }})` |
| Gerenciamento de foco após navegação | `@AccessibilityFocusState` | `FocusRequester.requestFocus()` | `AccessibilityInfo.sendAccessibilityEvent(handle, 'focus')` | `FocusNode.requestFocus()` |
| `prefers-reduced-motion` | Ambiente `accessibilityReduceMotion` / `UIAccessibility.isReduceMotionEnabled` | Respeite a escala de animação do sistema; evite auto-animação gratuita | `AccessibilityInfo.isReduceMotionEnabled()` | `MediaQuery.of(context).disableAnimations` |
| Zoom de texto (equivalência do SC 1.4.4) | Dynamic Type — use estilos de texto do sistema, nunca tamanhos fixos | Unidades `sp` para texto, nunca `dp` | `allowFontScaling` (default `true` — MUST NOT desabilitar) | `textScaler` do `MediaQuery` — nunca fixe `textScaleFactor: 1.0` |

## Custom Actions — o problema do gesto

A lacuna nativa mais comum no código gerado: **uma ação que só existe como gesto não existe para a tecnologia assistiva.** Deslizar para arquivar numa linha de lista, long-press para menu de contexto, arrastar para reordenar — quem enxerga e toca faz o gesto; quem usa leitor de tela, controle por acionador ou controle por voz não tem caminho nenhum até ela, porque o gesto é interceptado pela tecnologia assistiva ou é fisicamente indisponível. É o irmão nativo de *Pointer Gestures* (SC 2.5.1) e *Dragging Movements* (SC 2.5.7).

1. **Toda ação alcançável apenas por gesto MUST ser exposta também como custom accessibility action**, com a API da plataforma na tabela acima. O toque da linha pode continuar sendo um toque; o que precisa ser exposto são as *consequências* do swipe (arquivar, apagar, fixar).
2. **O rótulo da ação é parente do rótulo visível:** curto, começando pelo verbo, e igual ao texto que a UI mostra para a mesma ação em outro lugar (a SC 2.5.3 se aplica ao que quem usa controle por voz consegue falar).
3. **Como elas aparecem, para quem valida saber o que testar:** o VoiceOver anuncia *"ações disponíveis"* no elemento — a pessoa desliza verticalmente com um dedo para percorrer as ações e toca duas vezes para executar; o TalkBack as apresenta no menu local de ações; Switch Control e Voice Control leem a mesma lista.
4. **Não duplique.** Se os botões dentro da linha são focáveis individualmente *e* reexpostos como custom actions, toda ação é anunciada duas vezes. No Compose, limpe a semântica dos filhos (`clearAndSetSemantics { }`) ao subi-los para `customActions`; o princípio vale em todas as plataformas.
5. **Custom action é suplemento, nunca esconderijo:** uma ação essencial à tarefa continua precisando de caminho visível e descobrível para todo mundo (um menu, uma tela de detalhes) — a custom action devolve paridade a quem usa tecnologia assistiva, não desculpa uma interface cuja *única* affordance é um gesto invisível.

*APIs conferidas contra a documentação das plataformas: [`UIAccessibilityCustomAction`](https://developer.apple.com/documentation/uikit/uiaccessibilitycustomaction) / [`accessibilityAction(named:)`](https://developer.apple.com/documentation/swiftui/view/accessibilityaction(named:_:)) · [Compose `customActions`](https://developer.android.com/develop/ui/compose/accessibility/semantics) · [React Native `accessibilityActions`](https://reactnative.dev/docs/accessibility) · [Flutter `CustomSemanticsAction`](https://api.flutter.dev/flutter/semantics/CustomSemanticsAction-class.html).*

## Verificação (equivalente nativo da Seção 7)

- [ ] **Passagem de leitor de tela solicitada:** VoiceOver (iOS) / TalkBack (Android) — validação humana; a IA MUST NOT alegar que os executou.
- [ ] **Tecnologias assistivas além do leitor de tela:** o rótulo que a pessoa **fala** precisa bater com o rótulo que ela **vê** (Voice Control no iOS, Voice Access no Android — SC 2.5.3); toda ação alcançável por ativação sequencial, para controle por acionador (Switch Control / Switch Access); todo controle alcançável por teclado externo (Full Keyboard Access no iOS, navegação por teclado no Android). Essas três leem o mesmo nome acessível e a mesma ordem de foco que o leitor de tela — e é por isso que um controle nomeado só para o leitor de tela quebra as quatro de uma vez.
- [ ] **Escala de fonte:** a UI sobrevive ao maior tamanho de fonte do sistema sem truncamento ou sobreposição.
- [ ] **Ordem de foco/swipe:** a navegação sequencial segue a ordem visual/lógica.
- [ ] **Anúncios:** feedback assíncrono audível sem tocar na tela.
- [ ] **Paridade de gesto:** toda consequência de swipe, long-press ou arraste é alcançável pelas custom actions do elemento (VoiceOver: "ações disponíveis" → swipe vertical de um dedo; TalkBack: menu local de ações) — e nada é anunciado duas vezes.
