# Guia de Gráficos & Visualização de Dados

> **Escopo:** Gráficos, dashboards e qualquer desenho cujo conteúdo seja dado (*Padrões Visuais*, §3).

## 0. A regra da qual todas as outras decorrem

**Um gráfico não é uma figura de dados. É dado, desenhado.** Logo, a alternativa acessível dele é **o dado**, não a descrição do desenho.

```tsx
// ❌ A falha que este guia existe para evitar — conforme para todo verificador, inútil
<img src="/receita.svg" alt="Gráfico de barras mostrando o crescimento da receita em 2026" />

// ✅ A alternativa são os números, ao alcance de todo mundo
<figure>
  <img src="/receita.svg" alt="Gráfico de barras: receita mensal, 2026. Sobe de 40 mil em janeiro a 120 mil em junho." />
  <figcaption>Receita mensal, 2026</figcaption>
  <details>
    <summary>Ver dados como tabela</summary>
    <table>{/* a mesma série, em linhas */}</table>
  </details>
</figure>
```

O `alt` diz o que a pessoa *veria*; a tabela entrega o que ela *aprenderia*. Um gráfico que entrega só o primeiro é um gráfico que só quem enxerga consegue ler — e nenhum verificador automático vai dizer isso, porque o atributo `alt` está lá e é descritivo.

**Vale para as três formas:** a tabela equivalente é **MUST** para gráficos informativos, em todos os perfis de conformidade. Onde a tabela é impraticável (milhares de pontos, série ao vivo), um dataset para download ou um endpoint declarado na legenda é equivalente aceitável; "os números estão em outro lugar do produto" não é.

## 1. Primeiro decida qual das três formas você está construindo

A técnica muda por completo, e errar aqui é a raiz da maioria dos gráficos quebrados:

| Forma | Quando é a certa | O que ela deve |
| :--- | :--- | :--- |
| **Imagem estática** (PNG/SVG exportado) | o gráfico nunca muda e nada nele é clicável | `alt` com a **tendência e os extremos**, mais a tabela de dados por perto — ver [Imagens](guide-images.md) |
| **SVG inline** | o gráfico é renderizado a partir de dados, sem interação ponto a ponto | `role="img"` no `<svg>` **mais** `aria-label`/`aria-labelledby`; filhos com `aria-hidden` para o leitor não percorrer uma pilha de `<path>` |
| **Interativo** (canvas, hover/clique em pontos, zoom, brush) | a pessoa age sobre o dado | tudo do §3 — teclado, foco, anúncio — mais a tabela |

```tsx
// SVG inline, sem interação: um nó na árvore de acessibilidade, não duzentos
<svg role="img" aria-labelledby="grafico-t grafico-d" viewBox="0 0 600 300">
  <title id="grafico-t">Receita mensal, 2026</title>
  <desc id="grafico-d">Sobe de 40 mil em janeiro a 120 mil em junho, com queda a 35 mil em março.</desc>
  <g aria-hidden="true">{/* paths, eixos, linhas de grade */}</g>
</svg>
```

> **Canvas não tem árvore de acessibilidade.** Um gráfico desenhado em `<canvas>` é, para a tecnologia assistiva, um retângulo em branco. O que quer que a biblioteca renderize, a tabela de dados e o caminho por teclado precisam existir no DOM ao lado dele — nunca dentro do canvas.

## 2. Cor nunca é a codificação

Tratado a fundo em [Percepção Visual](guide-visual-perception.md); aqui, o que isso significa especificamente num gráfico:

1. **Toda série carrega um segundo canal além do matiz** — padrão de traço, forma do marcador, textura ou rótulo direto na ponta da linha. É a regra *Padrões Visuais* do `A11Y.md` §3, e é a falha mais comum em dashboards gerados.
2. **Rótulo direto vence legenda.** A legenda obriga a pessoa a guardar na memória um mapa cor↔nome e casá-lo ao longo do plano — custo cognitivo para todo mundo, tarefa impossível para muita gente. Rotule a série onde ela está desenhada.
3. **Séries adjacentes precisam de 3:1 entre si** (SC 1.4.11), não só contra o fundo: dois azuis que passam no branco ainda se fundem numa linha só para quem tem sensibilidade reduzida ao contraste.
4. **Estado nunca anda só na cor** — uma barra "crítica" não é apenas vermelha; é vermelha **e** rotulada ou marcada.

## 3. Teclado: alcançar o gráfico não é lê-lo

Um gráfico interativo é um widget, e a tecla Tab não pode ser a única coisa que funciona.

1. **Uma parada de tabulação para o gráfico**, e então setas para andar entre pontos — o padrão de uma grade, não uma lista de duzentas paradas.
2. **O foco é visível no ponto focado** (SC 2.4.7): anel, halo, marcador ampliado — nunca apenas um tooltip aparecendo.
3. **O ponto focado anuncia seus valores.** Ou o ponto é um elemento focável de verdade, com nome acessível (`<g tabindex="0" role="img" aria-label="Março: 35.000">`), ou uma região `role="status"` ao lado do gráfico é atualizada conforme o foco anda.
4. **Tudo que o mouse faz, o teclado faz:** se hover abre tooltip, foco abre o mesmo tooltip (ver [Tooltips & Popovers](guide-tooltips-popovers.md)); se arrastar seleciona um intervalo, uma alternativa por teclado seleciona o mesmo intervalo (ver [Drag & Drop](guide-drag-drop.md)).
5. **`Esc` sai** de qualquer modo de zoom ou brush sem sair da página.

```tsx
// Anunciando o ponto sob o foco, sem reconstruir o gráfico inteiro
<div role="status" aria-live="polite" className="sr-only">
  {focado ? `${focado.rotulo}: ${formatarValor(focado.valor)}` : ""}
</div>
```

## 4. Gráficos que atualizam

Dashboards mudam sob filtros, intervalos de data e dados ao vivo. Toda mudança é mudança de status (SC 4.1.3).

- Anuncie o **resultado**, não o evento: *"Filtrado por 2º trimestre: 3 séries, 12 pontos"* — nunca *"gráfico atualizado"*.
- **Não** ponha `aria-live` no container do gráfico: um redesenho dispara centenas de mutações e o leitor de tela lê o redesenho, não o resultado. Anuncie de uma região pequena e dedicada.
- Gráfico com dado ao vivo **MUST** oferecer pausa (SC 2.2.2) — movimento automático contínuo não é isento por ser dado.
- Mantenha a tabela sincronizada com os filtros. Uma tabela mostrando o conjunto sem filtro é uma segunda resposta, contraditória.

## 5. Dashboards

- Cada gráfico fica numa região rotulada — `<section aria-labelledby>` com título de verdade, para o painel inteiro ser navegável por cabeçalhos.
- **O texto do título nomeia a pergunta que o gráfico responde**, não o tipo do gráfico: "Receita por mês", nunca "Gráfico de barras 3".
- Metadado pequeno é onde a exceção de densidade de 10px mais é abusada — é entrada em `EXCEPTIONS.md` com contraste 7:1, não padrão (`A11Y.md` §4).
- Um "gráfico" que é um número só (um card de KPI) é texto: marque como texto, não como imagem de um número.

*Critérios de sucesso cobertos: 1.1.1 Conteúdo Não Textual (A) · 1.4.1 Uso de Cor (A) · 1.4.11 Contraste Não Textual (AA) · 2.1.1 Teclado (A) · 2.4.7 Foco Visível (AA) · 2.2.2 Pausar, Parar, Ocultar (A) · 4.1.3 Mensagens de Status (AA)*
