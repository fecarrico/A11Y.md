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

## Brasil — ABNT NBR 17060 (aplicativos móveis)

Quando o produto chega ao público brasileiro como aplicativo móvel, a referência normativa ao lado da WCAG é a **ABNT NBR 17060:2022** — *Acessibilidade em aplicativos de dispositivos móveis: requisitos* (26 de outubro de 2022) —, irmã mobile da NBR 17225 e, como ela, lastro do art. 63 da LBI (Lei 13.146/2015). A norma web cobre conteúdo e aplicações web; esta cobre **aplicativos nativos (Android, iOS), híbridos e web apps em smartphones e tablets, incluindo sites abertos no celular** — por isso um site responsivo com destino Brasil responde às duas. Desktop, TV e vestíveis ficam fora do escopo.

- **Forma:** 54 requisitos e recomendações em quatro grupos — *percepção e compreensão* (5.1.1), *controle e interação* (5.1.2), *mídia* (5.1.3) e *codificação* (5.1.4) —, a maioria rastreada a um critério de sucesso da WCAG. A base é a **WCAG 2.1**, não a 2.2: os seis critérios A/AA que a 2.2 acrescentou (SC 2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) não têm correspondente na norma, e este padrão já os exige. **Uma construção conforme a este padrão no perfil declarado já satisfaz quase todos os itens**; o que segue é o resto.
- **Onde a norma diz mais que a WCAG** — checkpoints nomeados para destino mobile brasileiro:
  - **Rótulo visível antes do campo (5.1.1.11):** o rótulo do formulário fica *antes* da entrada — acima ou à esquerda — e placeholder nunca é rótulo (o check `placeholder-label` do gate é a metade mecânica deste item). Uma inspeção de 2025 em cinco redes sociais encontrou as cinco reprovando nele.
  - **Etapas em sequência (5.1.1.16):** um fluxo em etapas informa o total de etapas e a posição atual; uma lista paginada informa o intervalo exibido e o total de itens. A WCAG não tem critério para isso; a regra de *Carga Cognitiva* (SC 3.3.7/3.3.8) é a obrigação mais próxima neste padrão.
  - **Configurações de acessibilidade (5.1.2.1):** o item da norma para o que a Regra Central 4 já exige — escala de fonte, contraste e movimento reduzido definidos no sistema são respeitados, nunca sobrescritos.
  - **Limites de tempo (5.1.2.6):** a mecânica do SC 2.2.1 — desligar, ajustar ou estender até dez vezes — vale para todo cronômetro não essencial, janelas de chat incluídas.
  - **Sem travamento na navegação sequencial com tecnologia assistiva (5.1.2.14):** a forma nativa de *Sem Armadilha de Teclado* (SC 2.1.2): a ordem de deslize do TalkBack e do VoiceOver alcança todo controle e nunca congela num deles — o caso de campo por trás do item foi um aplicativo de transporte travando ao preencher o local de partida com o leitor de tela ligado.
  - **Conteúdo piscante (5.1.1.25):** o item da norma para o SC 2.3.1 — nada pisca mais de três vezes por segundo, e conteúdo que pode piscar vem com aviso antes de tocar.
  - **Alvo de toque (5.1.2.13, recomendação):** a norma recomenda o alvo de 44×44 do SC 2.5.5; as normas de plataforma da Regra Central 3 já o superam.
- **Mapeamento de conformidade (deste padrão — a norma não define níveis):** ⚖️ Standard (AA) = todo *requisito*; 🛡️ Shield (AAA) = requisitos mais toda *recomendação*, com cada recomendação não atendida justificada no `EXCEPTIONS.md`. Com destino mobile brasileiro, o `REPORT.md` nomeia a NBR 17060 ao lado do perfil de conformidade, como o destino web nomeia seu nível da NBR 17225 ([Governança §6.1](guide-governance.md)).
- **Verificação:** a passada humana deste guia (leitor de tela, controle por voz, acionador, teclado externo, escala de fonte) é o próprio método da norma — as inspeções publicadas foram feitas com TalkBack. A IA **MUST NOT** alegar conformidade com a NBR 17060; quem alega é o validador humano, a partir do relatório.

*Fontes: a ABNT NBR 17060:2022 é distribuída pelo [catálogo da ABNT](https://www.abntcatalogo.com.br/), gratuitamente. Estrutura, escopo e publicação: [NIC.br](https://nic.br/noticia/releases/norma-da-abnt-sobre-acessibilidade-para-dispositivos-moveis-torna-a-navegacao-mais-inclusiva/) · [Web para Todos](https://mwpt.com.br/abnt-lanca-norma-de-acessibilidade-em-aplicativos-moveis/). A numeração dos itens segue a estrutura publicada, reproduzida pelo [checklist da Academia de Acessibilidade](https://www.academiadeacessibilidade.com.br/ferramentas/checklist-abnt-17060/index.html); a redação de 5.1.1.11, 5.1.1.16, 5.1.1.25, 5.1.2.6 e 5.1.2.14, conforme citada por [Gomes, Melo & Mota, IHC 2025](https://sol.sbc.org.br/index.php/ihc/article/view/37713) e por [Vidal, WPT, 2025](https://mwpt.com.br/como-a-abnt-17060-para-dispositivos-moveis-pode-auxiliar-na-correcao-de-problemas-de-acessibilidade/). Quem declara conformidade lê a norma.*

## Verificação (equivalente nativo da Seção 7)

- [ ] **Passagem de leitor de tela solicitada:** VoiceOver (iOS) / TalkBack (Android) — validação humana; a IA MUST NOT alegar que os executou.
- [ ] **Tecnologias assistivas além do leitor de tela:** o rótulo que a pessoa **fala** precisa bater com o rótulo que ela **vê** (Voice Control no iOS, Voice Access no Android — SC 2.5.3); toda ação alcançável por ativação sequencial, para controle por acionador (Switch Control / Switch Access); todo controle alcançável por teclado externo (Full Keyboard Access no iOS, navegação por teclado no Android). Essas três leem o mesmo nome acessível e a mesma ordem de foco que o leitor de tela — e é por isso que um controle nomeado só para o leitor de tela quebra as quatro de uma vez.
- [ ] **Escala de fonte:** a UI sobrevive ao maior tamanho de fonte do sistema sem truncamento ou sobreposição.
- [ ] **Ordem de foco/swipe:** a navegação sequencial segue a ordem visual/lógica.
- [ ] **Anúncios:** feedback assíncrono audível sem tocar na tela.
- [ ] **Destino brasileiro:** o `REPORT.md` nomeia a ABNT NBR 17060 ao lado do perfil de conformidade, e os checkpoints da seção *Brasil* acima foram percorridos por um humano.
- [ ] **Paridade de gesto:** toda consequência de swipe, long-press ou arraste é alcançável pelas custom actions do elemento (VoiceOver: "ações disponíveis" → swipe vertical de um dedo; TalkBack: menu local de ações) — e nada é anunciado duas vezes.
