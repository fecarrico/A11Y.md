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