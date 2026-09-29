# Guia de Controles de Formulário

> **Escopo:** Checkboxes, grupos de radio, switches, sliders e o `<select>` nativo — os controles mais gerados e menos especificados — e o estado desabilitado que todos compartilham. Labels, erros e agrupamento vivem em [Forms](guide-forms.md); selects com busca em [Autocomplete & Combobox](guide-autocomplete.md).

## 0. A regra que todas as outras seguem

**O controle nativo é o padrão. Um controle customizado deve tudo o que o nativo dava de graça — nome, papel, estado, as mesmas teclas — e precisa provar que entrega.** `<input type="checkbox">`, `<input type="radio">`, `<input type="range">` e `<select>` são operáveis por teclado, anunciados com papel e estado, estilizáveis com `appearance: none` e `accent-color`, e gratuitos em toda plataforma. Uma `<div>` com cara de checkbox não tem nada disso, e o axe não distingue as duas depois que `role` e `aria-checked` foram salpicados — é a *Half-Climbed ARIA Ladder* do `A11Y.md` §6 na menor escala.

```html
<!-- ❌ Parece checkbox, é uma div: sem nome, sem papel, sem estado, sem Space -->
<div class="checkbox" onclick="toggle(this)"><span class="box"></span> Lembrar de mim</div>

<!-- ✅ O controle nativo, estilizado -->
<label><input type="checkbox" name="remember"> Lembrar de mim</label>
```

Escolha o controle pelo que ele faz, não pela forma (SC 1.3.1): uma escolha entre várias → grupo de radio; opções sim/não independentes → checkboxes; configuração com efeito imediato → switch; valor numa faixa → slider com campo numérico ao lado; uma opção de uma lista → `<select>`.

## 1. Checkbox

1. **O rótulo é o alvo.** Vincule com `for`/`id` ou envolva o controle: clicar ou tocar no texto alterna a caixa, e o alvo de toque passa a ser o rótulo inteiro (SC 2.5.8).
2. **Três estados, cada um visível sem cor** (SC 1.4.1): marcado, desmarcado e — quando um pai resume os filhos — indeterminado: `el.indeterminate = true` no controle nativo, anunciado como "misto". Um checkbox customizado transmite o mesmo por `aria-checked="true|false|mixed"`.
3. **`Espaço` alterna; `Enter` envia o formulário.** Checkbox customizado que alterna com `Enter`, ou não faz nada com `Espaço`, falha o SC 2.1.1.
4. **Só opções independentes.** Se escolher uma precisa desmarcar as outras, é grupo de radio, não checkboxes com script.

## 2. Grupo de radio

1. **O grupo tem nome.** `<fieldset>` + `<legend>` (ver [Forms §3](guide-forms.md)), ou `role="radiogroup"` + `aria-labelledby` num grupo customizado. A legend é o que o leitor de tela diz antes da primeira opção — sem ela, "Sim" e "Não" são respostas a uma pergunta que ninguém ouviu.
2. **Mesmo `name`, uma parada de Tab.** Radios nativos com o mesmo `name` formam o grupo: `Tab` chega à opção marcada (ou à primeira), `↑`/`↓`/`←`/`→` movem **e selecionam**, `Espaço` seleciona a focada. Um grupo customizado reproduz exatamente esse foco itinerante.
3. **Nenhuma opção pré-marcada quando a resposta importa** — um consentimento, uma forma de pagamento: a pessoa escolhe, e o formulário avisa quando ela não escolheu (SC 3.3.1). Opção pré-selecionada em silêncio é decisão que o usuário nunca tomou.
4. **O estado selecionado não é só cor:** ponto preenchido, check, rótulo mais forte — algo que sobreviva ao modo de cores forçadas e a uma impressão monocromática (SC 1.4.1).

## 3. Switch

Switch é um checkbox cuja mudança vale **agora** — sem botão Salvar, sem confirmação.

1. **Marcação:** `<button type="button" role="switch" aria-checked="true|false">`, ou `<input type="checkbox" role="switch">`. O leitor de tela anuncia "switch, ligado/desligado"; `Espaço` (e `Enter` num botão) alterna.
2. **O rótulo nomeia a configuração — nunca o estado atual, nunca a ação.** "Notificações" continua "Notificações" ligado ou desligado; o estado vem do `aria-checked`. Rótulo que vira "Desligar" produz o anúncio *"Desligar, switch, ligado"* — duas verdades que se contradizem (SC 4.1.2).
3. **Ligado e desligado visíveis sem cor:** a posição do botão deslizante mais um texto ou ícone, e a trilha com 3:1 contra o entorno nos dois estados (SC 1.4.11).
4. **Se a mudança precisa de confirmação ou de Salvar, não é switch** — use checkbox e deixe o formulário enviar.

## 4. Slider (range)

1. **Prefira `<input type="range">`** com `<label>`, `min`, `max`, `step` — e o **valor atual visível em texto** ao lado: um botão numa trilha também não diz nada exato para quem enxerga.
2. **Quando o número não é o significado, diga o significado:** `aria-valuetext="Médio"` num slider de qualidade 1–3, `"14:30"` num horário. Slider customizado deve `role="slider"`, `aria-valuemin`/`aria-valuemax`/`aria-valuenow`, e `aria-valuetext` onde o número sozinho não diz nada.
3. **Teclas:** `←`/`↓` diminuem e `→`/`↑` aumentam um `step`; `PageUp`/`PageDown` um passo maior; `Home`/`End` vão aos extremos. Toda mudança por tecla atualiza o valor visível e o anunciado.
4. **Arrastar é atalho** (SC 2.5.7): o valor precisa poder ser definido sem arrasto — clique ou toque na trilha, ou botões de passo. **Precisão pede uma segunda porta** (Regra da Casa†): quando o valor exato importa — preço, dose, intervalo de datas — acompanhe o slider de um `<input>` numérico ligado ao mesmo valor. Arrastar até exatamente 37 é teste de destreza, e o campo numérico é também o caminho do controle por voz.
5. **O botão deslizante é um alvo:** 24×24 CSS px no mínimo (SC 2.5.8), 44×44 pela Regra da Casa† — e a trilha não é o único jeito de chegar ao valor.

## 5. Select nativo

1. **`<select>` primeiro.** Abre a lista da própria plataforma, opera com setas e digitação antecipada, e é o que o leitor de tela da pessoa já conhece. Restilize o estado fechado; deixe a lista aberta com a plataforma.
2. **`<option>` de placeholder não é rótulo.** "Escolha um país" como primeira opção some no instante em que um valor é escolhido; a `<label>` fica (`A11Y.md` §6, *Placeholder Labels*). Se uma escolha em branco precisa existir, dê a ela um nome de verdade ("Sem preferência") e `value=""`.
3. **Agrupe com `<optgroup label="…">`** quando a lista tem seções; o rótulo do grupo é anunciado quando o leitor entra nele.
4. **Mudar a seleção MUST NOT navegar nem enviar por conta própria** (SC 3.2.2): quem percorre as opções com setas e leitor de tela dispara `change` a cada passo. Acrescente um botão.
5. **Busca, multisseleção com chips, opções com ícone — isso é combobox:** ver [Autocomplete & Combobox](guide-autocomplete.md), e registre no `A11Y-DECISIONS.md` a decisão de deixar o elemento nativo.

## 6. Controles desabilitados

1. **`disabled` nativo** tira o controle da ordem de Tab e o anuncia como indisponível — certo quando o controle de fato não pode ser usado agora.
2. **`aria-disabled="true"`** o mantém focável e anunciado como indisponível — certo quando a pessoa precisa *encontrá-lo* para saber por que está desligado (um botão de enviar esperando campos obrigatórios). Acompanhe do motivo, ligado por `aria-describedby`, e nunca dependa só do cinza (SC 1.4.1).
3. **O texto do motivo não é isento de contraste.** O controle desabilitado em si é (SC 1.4.3, componentes inativos); a explicação ao lado é texto corrido e segue o piso do perfil.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO um formulário com checkbox, QUANDO chego nele com `Tab` e pressiono `Espaço`, ENTÃO ele alterna — e `Enter` não o alterna.
- DADO um grupo de radio, QUANDO pressiono `Tab`, ENTÃO uma única parada pousa na opção marcada (ou na primeira), e `↑`/`↓` movem a seleção sem sair do grupo.
- DADO um switch, QUANDO pressiono `Espaço`, ENTÃO ele liga ou desliga na hora, sem etapa de Salvar.
- DADO um slider, QUANDO pressiono `→`, `PageUp` e `End`, ENTÃO o valor visível muda um passo, um passo maior, e vai ao máximo.
- DADO um `<select>`, QUANDO percorro as opções com as setas, ENTÃO nada navega nem envia até eu acionar um botão.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego a um checkbox, ENTÃO ouço o rótulo, "caixa de seleção", e "marcado", "não marcado" ou "misto".
- QUANDO entro num grupo de radio, ENTÃO ouço a legend antes da primeira opção, e cada opção como "botão de opção, n de m".
- QUANDO alterno um switch, ENTÃO ouço o mesmo nome da configuração com "switch, ligado" ou "switch, desligado" — o nome em si nunca muda.
- QUANDO movo um slider, ENTÃO ouço o novo valor — ou o significado dele, quando o número sozinho não diz nada.
- QUANDO chego a um controle desabilitado, ENTÃO ouço "indisponível" e, se ele ainda recebe foco, o motivo de estar desligado.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo até um checkbox ou um switch e toco duas vezes, ENTÃO o estado que ouço em seguida é o oposto do que ouvi antes.
- QUANDO deslizo por um grupo de radio, ENTÃO ouço o nome do grupo uma vez, depois cada opção com a posição dela, e o toque duplo a seleciona.
- QUANDO foco um slider e deslizo para cima ou para baixo, ENTÃO o valor muda um passo e é anunciado.

*Critérios de sucesso cobertos: 1.3.1 Informações e Relações (A) · 3.3.2 Rótulos ou Instruções (A) · 4.1.2 Nome, Função, Valor (A) · 2.1.1 Teclado (A) · 1.4.1 Uso de Cor (A) · 1.4.11 Contraste Não Textual (AA) · 2.5.8 Tamanho do Alvo (Mínimo) (AA) · 2.5.7 Movimentos de Arrastar (AA) · 3.2.2 Em Entrada (A) · 3.3.1 Identificação de Erro (A)*
