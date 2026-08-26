# Accessibility: Mídia Temporal, Vídeo de Fundo & Movimento

> Escopo: vídeo e áudio, mídia decorativa/de fundo, parallax e movimento disparado por scroll, texto sobre mídia em movimento, e a regra de humano no circuito para legendas e transcrições.

## 1. Classifique antes de embedar

O teste de remoção do [guia de Imagens](guide-images.md) vale sem alteração: *"Se eu remover esta mídia, o que o usuário perde?"*

| Resposta | Classe | O que ela deve |
| :--- | :--- | :--- |
| Perde informação | **Informativa** | legendas (SC 1.2.2), transcrição, audiodescrição quando o visual carrega o que a trilha não diz (SC 1.2.5) |
| Perde uma função (executa uma etapa, confirma uma ação) | **Funcional** | nome acessível para o controle **e** um caminho não-midiático para o mesmo resultado |
| Não perde nada além de atmosfera | **Decorativa** | nenhuma legenda — mas ainda deve mecanismo de pausa (SC 2.2.2), silêncio (SC 1.4.2) e comportamento sob reduced-motion |

**Decorativa não é sinônimo de fundo.** Um vídeo de hero mostrando o produto em uso é informativo *e* está no fundo. A classe vem do que a mídia carrega, não de onde ela está.

## 2. Media Evidence — as três perguntas

A IA não consegue perceber um arquivo de mídia. Input multimodal lê um frame colado, não um `.mp4` do repositório — então o caminho do guia de Imagens ("eu consigo ver, logo classifico") não existe aqui. A IA **pergunta, no mesmo turno**:

1. **Ela carrega informação ou função**, ou é atmosfera? *(a classificação da Seção 1 — resposta do desenvolvedor, não palpite da IA)*
2. **Ela tem faixa de áudio?** Se sim: o áudio precisa ser audível, ou pode ir mudo?
3. **Já existem legendas, transcrição ou audiodescrição?** Se não, quem produz, e até quando?

Legendas e transcrições geradas pela IA ou por serviço automático são **rascunhos para revisão humana**, nunca a alternativa entregue. Uma legenda automática não revisada é o `alt` deduzido do nome do arquivo, em outro meio: presente, plausível e errada exatamente onde o conteúdo é mais difícil — nomes próprios, jargão, números. O mercado chama o resultado de *craptions*, e nenhum verificador automático sinaliza, porque o elemento `<track>` está lá.

## 3. Vídeo de fundo

O caso mais comum, e o que mais falha. Um loop decorativo e mudo ainda deve três coisas:

### ✅ Correto

```html
<section class="hero">
  <!-- Confirmado decorativo pelo desenvolvedor: não carrega informação. -->
  <video id="heroVideo" muted loop playsinline
         poster="hero-still.jpg"
         aria-hidden="true" tabindex="-1">
    <source src="hero.mp4" type="video/mp4">
  </video>
  <div class="hero__scrim"></div>

  <div class="hero__content">
    <h1>Software acessível desde a primeira linha</h1>
    <button type="button" id="heroMotionToggle">Pausar vídeo de fundo</button>
  </div>
</section>
```

```js
// O autoplay é concedido por script, nunca pela marcação — assim a preferência
// pode vetá-lo antes de um único frame se mover.
const video = document.getElementById('heroVideo');
const toggle = document.getElementById('heroMotionToggle');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

const render = () => {
  toggle.textContent = video.paused ? 'Reproduzir vídeo de fundo' : 'Pausar vídeo de fundo';
};
const respeitarPreferencia = () => {
  if (reduceMotion.matches) video.pause();   // o frame do poster permanece na tela
  else video.play();
  render();
};

toggle.addEventListener('click', () => { video.paused ? video.play() : video.pause(); render(); });
reduceMotion.addEventListener('change', respeitarPreferencia);
respeitarPreferencia();
```

- **`aria-hidden="true"` + `tabindex="-1"`** — o vídeo decorativo sai da árvore de acessibilidade e da ordem de tabulação. O botão de pausa fica **fora** dele: um controle dentro de uma subárvore `aria-hidden` é inalcançável.
- **`muted`** — áudio que começa sozinho exige controle próprio (SC 1.4.2); entregar mudo elimina o problema em vez de resolvê-lo.
- **`poster`** — o frame estático é o fallback de quem usa reduced-motion, de conexão lenta e de autoplay bloqueado. Escolha-o deliberadamente: ele vira a imagem de hero de verdade.
- **O controle de pausa não é opcional.** Um loop acima de 5 segundos é conteúdo em movimento sob a SC 2.2.2 — Nível A. "É só um fundo" não é isenção no texto do critério.

### ❌ Incorreto

```html
<video autoplay loop playsinline src="hero.mp4"></video>
```

Toca sozinho independentemente do `prefers-reduced-motion`, não oferece como parar, carrega faixa de áudio não silenciada por padrão e aparece na árvore de acessibilidade como um elemento de mídia sem nome.

## 4. Texto sobre mídia

A falha que ferramenta nenhuma pega. Um título sobre vídeo tem razão de contraste que **muda a cada frame**, e todo verificador automático aprova: o axe mede o texto contra o fundo computado do container — que é transparente —, nunca contra os pixels que o usuário está vendo.

### ✅ Correto

```css
.hero__scrim {
  position: absolute;
  inset: 0;
  background: rgb(12 14 18 / 0.72);   /* a superfície contra a qual o contraste é de fato medido */
}
.hero__content { position: relative; }   /* acima do scrim */
```

Meça o texto contra o **pior caso composto**: o frame mais claro do vídeo visto através do scrim. Se você não consegue enumerar os frames, aumente o scrim até o vídeo não alterar materialmente o resultado — uma faixa opaca atrás do texto é resposta legítima, e a única que sobrevive à troca do vídeo pelo time de marketing.

### ❌ Incorreto

- "O vídeo é escuro o suficiente" — até o frame em que não é.
- Um gradiente ajustado ao corte atual, sem decisão registrada. O próximo vídeo quebra em silêncio.
- `text-shadow` como única mitigação: muda a legibilidade percebida sem mudar a razão mensurável — é correção para o revisor, não para o usuário.

Registre o valor de scrim aceito no `A11Y-DECISIONS.md`: é decisão de nível de padrão, e o próximo hero vai precisar dela.

## 5. Parallax & movimento por scroll

Translação disparada por scroll é gatilho vestibular — náusea, tontura e desorientação em pessoas com distúrbios vestibulares — e **não é coberta** pelo botão de pausa da Seção 3, porque o usuário nunca pediu aquele movimento; o scroll pediu.

- Sob `prefers-reduced-motion: reduce`, o parallax **MUST** degradar para composição estática: as camadas param de transladar, a seção continua legível.
- Construa o caminho reduced-motion como **padrão**, acrescentando movimento no ramo `no-preference`. Escrito ao contrário, o fallback é justamente o que ninguém testa.

```css
.layer { transform: none; }                      /* padrão: sem movimento */

@media (prefers-reduced-motion: no-preference) {
  .layer { animation: parallax linear both; animation-timeline: scroll(); }
}
```

- Movimento que começa sozinho e passa de 5 segundos (marquees auto-rolantes, tickers em loop) cai de novo na SC 2.2.2: precisa de parada, não só de media query.

## 6. Mídia informativa & funcional

- **Legendas (SC 1.2.2, A):** sincronizadas, via `<track kind="captions">`. Carregam a fala **e** o áudio não-verbal significativo — `[porta bate]`, `[alarme]`, troca de interlocutor.
- **Transcrição:** não exigida nominalmente no AA, mas é a única alternativa que serve a pessoas surdocegas em linha braille, e a mais barata de produzir. Linke ao lado do player, não a três cliques de distância.
- **Audiodescrição (SC 1.2.5, AA):** exigida quando a imagem carrega informação que a trilha não dá — um gráfico que aparece na tela, texto em tela que ninguém lê em voz alta. A correção barata é a montante: roteirize a narração dizendo o que a tela mostra, e a descrição se torna desnecessária.
- **Controles:** prefira o atributo nativo `controls`. Um player customizado é Componente Complexo (Seção 5 do arquivo central) — operável por teclado de ponta a ponta, cada controle um `<button>` real com nome, estado anunciado.
- **Embeds de terceiros (YouTube, Vimeo, Loom):** o embed não transfere a obrigação. Verifique se as legendas existem no ativo hospedado e se o `<iframe>` tem `title`. Legenda autogerada é rascunho, exatamente como na Seção 2.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 1.2.1 Apenas Áudio e Apenas Vídeo | A | transcrição para só-áudio; alternativa para vídeo mudo que carrega informação |
| 1.2.2 Legendas (Pré-gravado) | A | legendas sincronizadas para qualquer áudio pré-gravado em vídeo |
| 1.2.3 Audiodescrição **ou** Alternativa | A | uma das duas para a informação visual |
| 1.2.5 Audiodescrição (Pré-gravado) | AA | a audiodescrição em si — a alternativa deixa de bastar |
| 1.4.2 Controle de Áudio | A | pausar/parar/volume independente para áudio acima de 3 segundos |
| 2.2.2 Pausar, Parar, Ocultar | A | mecanismo para movimento automático acima de 5 segundos |
| 2.3.1 Três Flashes | A | no máximo três flashes por segundo |
| 2.3.3 Animação por Interação | AAA (Regra da Casa† aqui) | `prefers-reduced-motion` respeitado por autoplay e parallax |
| 1.4.3 Contraste (Mínimo) | AA | texto sobre mídia medido contra camada estável, não contra um frame |
