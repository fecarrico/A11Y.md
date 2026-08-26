# Guia de Mapas Interativos

> **Escopo:** Mapas embutidos e interativos — localizadores de loja, rastreio de entrega, seletores de área, mapas de cobertura — vale o Princípio Zero: se a tarefa só pode ser concluída no mapa, a tarefa não pode ser concluída.

## 0. A regra da qual todas as outras decorrem

**A lista é a alternativa do mapa — e não é plano B, é o caminho principal para uma parcela grande das pessoas.**

```tsx
<section aria-labelledby="lojas-h">
  <h2 id="lojas-h">Lojas perto de 01310-100</h2>
  <div id="mapa" aria-label="Mapa das lojas próximas" role="application">{/* … */}</div>
  <ol>
    <li>
      <h3>Unidade Paulista</h3>
      <p>Av. Paulista 1000 — a 1,2 km — aberta até 22h</p>
      <a href="/lojas/paulista">Detalhes</a>
    </li>
  </ol>
</section>
```

Tudo que o mapa comunica — o que tem aqui, a que distância, em que ordem, o que acontece se eu escolher — existe em texto, na mesma página, atualizando com os mesmos filtros. Uma vez que essa lista existe, a maior parte do ônus de acessibilidade do mapa está quitada, e o que resta é fazer o mapa em si não ser ativamente hostil.

**Nunca faça do mapa o único jeito de:** escolher um endereço, definir uma área de entrega, selecionar uma loja, confirmar uma localização ou ver um status. Um fluxo de arrastar-o-pin sem campo de endereço é um formulário inacessível por teclado.

## 1. Decida que tipo de mapa é

| Tipo | Exemplo | O que ele deve |
| :--- | :--- | :--- |
| **Decorativo** | ilustração estilizada de uma cidade atrás de um título | `aria-hidden="true"` — e o endereço escrito em texto, como sempre |
| **Estático informativo** | imagem renderizada de um único local | é imagem: `alt` com a informação, não "mapa" — ver [Imagens](guide-images.md) |
| **Interativo** | pan, zoom, marcadores clicáveis, filtros | tudo o que vem abaixo |

Uma imagem estática cujo `alt` diz *"Mapa mostrando nossa localização"* não informou nada a quem lê. A alternativa é o endereço.

## 2. Teclado

1. **O container do mapa é uma única parada de tabulação** em que se pode entrar e — crucialmente — **de que se pode sair**. Um mapa que captura as setas é armadilha de teclado (SC 2.1.2); `Esc` precisa sempre devolver à página.
2. **Pan e zoom têm equivalentes por teclado** (setas para mover, `+`/`-` para o zoom), e os controles de zoom são `<button>` de verdade com nome, não `<div>` com ícone.
3. **Marcadores são controles focáveis com nome acessível** — *"Unidade Paulista, 1,2 km"* — ou, melhor, a lista ao lado do mapa é a forma de alcançá-los e o mapa segue a seleção da lista. O segundo desenho é mais fácil de acertar e melhor para todo mundo.
4. **Nada depende de hover.** Informação revelada ao passar o mouse sobre um marcador precisa ser alcançável por foco (ver [Tooltips & Popovers](guide-tooltips-popovers.md)) e estar presente na lista.
5. **Gestos têm alternativa de ponteiro único (SC 2.5.1):** pinça para zoom e pan com dois dedos precisam de botões também; arrastar para posicionar um pin precisa de campo de endereço (ver [Drag & Drop](guide-drag-drop.md)).

> **`role="application"` é arma carregada.** Ele entrega as teclas cruas ao widget e desativa os comandos de leitura do leitor de tela. Use só num mapa que de fato implemente interação completa por teclado, nunca na página inteira nem num container que a pessoa apenas lê.

## 3. Anuncie o que mudou

Pan, zoom e filtro trocam o conteúdo visível em silêncio. Anuncie o **resultado** por região de status polida, nunca o movimento:

```tsx
<div role="status" aria-live="polite" className="sr-only">
  {`${resultados.length} lojas na área visível`}
</div>
```

A mesma regra de qualquer dashboard: anuncie o desfecho ("4 lojas na área visível"), não o evento ("mapa movido"). Rastreio ao vivo que atualiza continuamente precisa de pausa (SC 2.2.2) e não pode reanunciar a cada tique.

## 4. Cor, contraste e rótulos sobre os tiles

- Linhas de rota, sombreamento de área e marcadores são gráficos significativos: **3:1 contra o entorno** (SC 1.4.11) — e entre si, quando duas rotas ou zonas ficam lado a lado.
- **Nunca codifique categoria só por cor** (SC 1.4.1): forma do marcador, numeração ou rótulo carrega junto. Um mapa "verde = disponível / vermelho = lotado" é ilegível para uma parcela grande das pessoas, incluindo o próprio mantenedor deste projeto.
- Texto embutido no tile do mapa não redimensiona com a página e costuma falhar contraste. O que importa é repetido no DOM.
- Texto de mapa não é isento de nada: os rótulos que *você* coloca sobre o mapa seguem o piso tipográfico do perfil ativo.

## 5. Provedores de terceiros

A maioria dos mapas vem de Google Maps, Mapbox, Leaflet ou equivalente. **A obrigação não se transfere junto com o embed** — mesma regra das plataformas de consentimento (ver [Banners de Consentimento](guide-consent-banners.md)).

- Teste o widget padrão do provedor com teclado e leitor de tela **antes** de adotá-lo. Vários entregam suporte a teclado atrás de uma flag de configuração.
- Dê ao `<iframe>` um `title` que diga o que ele contém — um iframe de mapa sem título é anunciado como "frame".
- Onde o controle do provedor não puder ser corrigido neste ciclo, isso é entrada em `EXCEPTIONS.md` com dono, issue e expiração — e a alternativa textual é o que mantém a funcionalidade utilizável enquanto isso, e é por isso que ela nunca é opcional.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 1.1.1 Conteúdo Não Textual | A | a informação do mapa existe como texto |
| 2.1.1 Teclado | A | pan, zoom, marcadores e seleção operáveis sem mouse |
| 2.1.2 Sem Armadilha de Teclado | A | sempre é possível sair do mapa |
| 2.5.1 Gestos de Ponteiro | A | pinça e arraste têm alternativa de ponteiro único |
| 1.4.1 Uso de Cor | A | categoria nunca carregada só por cor |
| 1.4.11 Contraste Não Textual | AA | rotas, zonas e marcadores a 3:1 |
| 4.1.3 Mensagens de Status | AA | mudança de área visível ou de resultados anunciada |
