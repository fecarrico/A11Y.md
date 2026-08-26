# Accessibility Guide: Navegação & Estrutura do Documento

> Escopo: Landmarks, skip links, propósito e consistência de links, links de nova aba e de arquivo, breadcrumbs, hierarquia de cabeçalhos, semântica de listas e gestão de foco em rotas de SPA.

## 1. Landmarks & Skip Link

```html
<a href="#main-content" class="skip-link">Pular para o conteúdo</a>
<nav aria-label="Navegação Principal">
  <ul>
    <li><a href="/" aria-current="page">Início</a></li>
    <li><a href="/sobre">Sobre</a></li>
  </ul>
</nav>
<main id="main-content">…</main>
```

- `<nav>`, `<main>`, `<header>`, `<footer>` e `<aside>` são landmarks — quem usa leitor de tela pula entre eles por atalho. Quando o mesmo landmark aparece mais de uma vez (dois `<nav>`), cada um **MUST** ter um `aria-label` que os distinga.
- O skip link é o **primeiro** elemento focável e **MUST** ficar visível ao receber foco — permite ao usuário de teclado pular a navegação repetida (SC 2.4.1).
- `aria-current="page"` marca a localização atual no menu.

## 2. Propósito do Link (SC 2.4.4)

O propósito de todo link **MUST** ser determinável pelo texto dele sozinho, ou pelo texto mais o contexto programático. Quem usa leitor de tela navega listando os links fora de contexto.

```html
<!-- ❌ o propósito vive fora do link -->
<a href="/relatorio.pdf">Clique aqui</a> para baixar o relatório anual.

<!-- ✅ o texto do link é o propósito -->
<a href="/relatorio.pdf">Baixar o relatório anual (PDF, 2 MB)</a>
```

- **MUST NOT** usar "clique aqui", "saiba mais", "leia mais" nus — textos idênticos repetidos apontando para destinos diferentes reprovam no teste da listagem. Onde um card repete "Leia mais", complemente programaticamente (`aria-labelledby="titulo-do-card id-do-leia-mais"`).
- **Nova aba ou janela:** link que abre fora do contexto atual **MUST** dizer isso no nome acessível ("abre em nova aba") — perder o botão Voltar sem aviso desorienta tanto quem usa lupa quanto quem tem carga cognitiva alta.
- **Destino não-HTML:** link para arquivo **MUST** declarar formato e, idealmente, tamanho no texto ("(PDF, 2 MB)") — a pessoa decide *antes* do download se as ferramentas dela o abrem (NBR 17225 5.7.7; o arquivo em si precisa ser acessível — ver [Governança §6.1](guide-governance.md)).

## 3. Navegação Consistente (SC 3.2.3)

Mecanismos de navegação repetidos entre páginas **MUST** manter a mesma ordem relativa em todas. Componentes com a mesma função **MUST** ser identificados de forma consistente (SC 3.2.4): o campo de busca não é "Buscar" aqui e "Pesquisar" ali.

- Em código: a navegação vive no layout compartilhado, nunca reconstruída página a página — a mesma regra de *Consistent Help* (core §3) vale para mecanismos de ajuda.
- **Breadcrumbs** (SC 2.4.8 AAA — recomendados para qualquer hierarquia com mais de dois níveis): lista ordenada dentro de `<nav aria-label="Breadcrumb">`, página atual marcada com `aria-current="page"`.

## 4. Hierarquia de Cabeçalhos & Listas

Cabeçalhos e listas são o esqueleto do documento — a primeira coisa que um usuário de leitor de tela pede é a lista de cabeçalhos.

- **Um `<h1>` por página**, descrevendo a página (par do `<title>` — core §3, *Título da Página*).
- Níveis **MUST NOT** pular (h2 → h4 é um buraco no sumário); o texto do cabeçalho **MUST** descrever a seção que abre (SC 2.4.6).
- **MUST NOT** escolher a tag de cabeçalho pelo tamanho da fonte — estilize com CSS; o nível é estrutura, não estética. O inverso também falha: um `<p>` em negrito fazendo papel de título de seção é invisível na lista de cabeçalhos (SC 1.3.1).
- Sequências de itens relacionados — menus incluídos — **MUST** ser listas reais (`<ul>`/`<ol>`): o leitor de tela anuncia "lista, 5 itens", o que uma pilha de `<div>`s nunca diz.

## 5. Rotas de SPA

Após uma mudança de rota no cliente, o foco **MUST** ser gerenciado — enviado ao `<h1>` do conteúdo novo ou ao topo da página — e o `<title>` **MUST** ser atualizado (core §3, *SPA Routing* e *Título da Página*). Mudança de rota que o leitor de tela nunca ouve é página que nunca mudou.

## Maus Exemplos

### 1. Menus Aninhados (Apenas no Hover)
- Menus que só aparecem no hover são inalcançáveis por teclado e por toque. Alterne no clique/foco, feche no `Esc`.

### 2. Links Fora do Padrão
```html
<span onclick="window.location='/nova-pagina'">Ir para a Página</span>
```
- Ver *Clickable Divs* — core §6: sem foco, sem role de link, sem nova aba, sem copiar endereço.

*Critérios de sucesso cobertos: 2.4.1 Ignorar Blocos (A) · 2.4.4 Propósito do Link — Em Contexto (A) · 2.4.6 Cabeçalhos e Rótulos (AA) · 2.4.8 Localização (AAA) · 1.3.1 Informações e Relações (A) · 3.2.3 Navegação Consistente (AA) · 3.2.4 Identificação Consistente (AA)*
