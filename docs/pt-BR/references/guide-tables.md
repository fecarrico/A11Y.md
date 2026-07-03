# Guia de Acessibilidade em Tabelas

> **Escopo:** Tabelas de Dados

## Regras Centrais
1. Use `<caption>` para descrever a tabela.
2. Use `<th>` com `scope="col"` ou `scope="row"`.
3. Evite usar `<div>` para dados tabulares, a menos que use `role="table"` e `role="cell"`.

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