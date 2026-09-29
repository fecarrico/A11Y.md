# Guia de Acessibilidade em Tabelas

> **Escopo:** Tabelas de Dados

## Regras Centrais
1. Use `<caption>` para descrever a tabela.
2. Use `<th>` com `scope="col"` ou `scope="row"`.
3. Evite usar `<div>` para dados tabulares. Se for inevitável, a estrutura ARIA MUST ser completa: `role="table"` no contêiner, `role="row"` em **cada linha** e `role="columnheader"` / `role="rowheader"` / `role="cell"` nas células. Sem o `role="row"` a tabela não expõe estrutura nenhuma — vira uma coleção de células soltas, e a navegação por linha e coluna do leitor de tela deixa de existir.

## Exemplo
```html
<table>
  <caption>Dados de Funcionários</caption>
  <thead>
    <tr>
      <th scope="col">Nome</th>
      <th scope="col">Cargo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>João Silva</td>
      <td>Engenheiro</td>
    </tr>
  </tbody>
</table>
```

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO uma página com uma tabela de dados, QUANDO pressiono `Tab` através dela, ENTÃO nenhuma célula recebe foco — só os controles de verdade dentro da tabela (links, botões), na ordem de leitura.
- QUANDO a tabela é feita de `<div>`s com papéis ARIA, ENTÃO o `Tab` se comporta exatamente como numa tabela nativa: nenhuma parada a mais, nenhuma a menos.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego na tabela, ENTÃO ouço "tabela", a legenda dela e o tamanho, em linhas e colunas.
- QUANDO me movo entre células com os comandos de tabela (`Ctrl+Alt` + `←`/`→`/`↑`/`↓`), ENTÃO em cada célula ouço o cabeçalho da coluna — e o da linha, quando existe — antes do valor.
- QUANDO a tabela é feita de `<div>`s, ENTÃO ainda ouço "tabela" e ainda me movo por linha e coluna — comandos de tabela que não fazem nada são reprovação.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo até a tabela, ENTÃO ouço "tabela", a legenda e quantas linhas e colunas ela tem.
- QUANDO deslizo pelas células, ENTÃO cada valor vem depois do cabeçalho da coluna — e do da linha, quando existe.
