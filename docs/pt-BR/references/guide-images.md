# Accessibility: Images & Alternative Text

> Escopo: Estratégia de alt text, imagens decorativas, imagens complexas (gráficos/diagramas) e acessibilidade em SVG.

## 1. Imagens Informativas
Imagens que transmitem um conceito ou informação.
### ✅ Correto
```html
<img src="grafico-vendas.png" alt="Gráfico de barras mostrando crescimento de 20% nas vendas no primeiro trimestre.">
```
- **Por quê:** O `alt` resume a conclusão do gráfico, não apenas descreve que é um gráfico.

### ❌ Incorreto
```html
<img src="grafico-vendas.png" alt="Gráfico de vendas">
```
- **Problema:** A descrição é vaga e não transmite a informação contida na imagem.

## 2. Imagens Funcionais
Imagens usadas como links ou botões (ícones).
### ✅ Correto
```html
<a href="/imprimir">
  <img src="printer-icon.png" alt="Imprimir documento">
</a>
```
- **Por quê:** O `alt` descreve a **ação** do link, não a aparência do ícone (ex: não use "ícone de impressora").

## 3. Imagens Decorativas
Imagens que não adicionam conteúdo (bordas, ilustrações de fundo).
### ✅ Correto
```html
<!-- Classificada como decorativa e confirmada por um humano — ver Seção 5. -->
<img src="divisor-bonito.png" alt="">
```
- **Por quê:** O `alt=""` (vazio) diz ao leitor de tela para ignorar a imagem. **Nunca** omita o atributo `alt`, senão o leitor lerá o nome do arquivo (ex: "imagem-123-final.png").
- ⚠️ **O valor vazio é uma decisão confirmada, não um padrão.** A IA **MUST NOT** chegar a esta classificação sozinha: o fluxo obrigatório está na **Seção 5**. Um `alt=""` aplicado por conta própria esconde do usuário de leitor de tela uma imagem possivelmente informativa — e nenhum verificador automático detecta, porque o atributo está lá.

## 4. O Problema do "Excesso de Descrição"
Evite começar com "Imagem de..." ou "Foto de...". O leitor de tela já anuncia que é uma imagem. Vá direto ao ponto.

## 5. Imagens Fornecidas pelo Usuário (Image Evidence)
Quando a imagem vem do usuário — um screenshot colado, um asset enviado, um arquivo referenciado —, a decisão do `alt` acontece **antes de a imagem entrar no código**, não depois. *(Esta é a regra "Image Evidence" do AI Behavior Contract, Seção 2 do arquivo principal.)*

**Passo 1 — Verifique o que você consegue perceber.**
- Você **consegue** ver a imagem (input multimodal ou ferramenta de leitura de imagem disponível no ambiente): descreva o que ela mostra e siga para o Passo 2. A visão te dá o *conteúdo*; só o contexto ao redor dá o *propósito* — a mesma foto pode ser decorativa numa página e informativa em outra.
- Você **não consegue** ver a imagem: solicite a descrição ao desenvolvedor no mesmo turno. Nunca prossiga com um `alt` chutado.

**Passo 2 — Classifique pelo teste de remoção.** *"Se eu remover essa imagem, o que o usuário perde?"*
- Perde informação → **informativa**: o `alt` carrega a conclusão do conteúdo (Seção 1).
- Perde uma função (link/botão) → **funcional**: o `alt` nomeia a ação (Seção 2).
- Não perde nada → **candidata a decorativa**: `alt=""` vazio — pendente do Passo 3.

**Passo 3 — Proponha; o humano decide.** Apresente a classificação e o rascunho do `alt` ao desenvolvedor e obtenha uma confirmação explícita. A leitura que a IA faz de uma imagem é hipótese, não evidência — o mesmo princípio da validação humana com leitor de tela no Complex Component Protocol. A confirmação faz parte do fluxo, não é formalidade.

**O que este fluxo proíbe:**
- `alt` fabricado a partir do nome do arquivo (`alt="hero-final-v2"`) — violação de *No Inference*.
- `alt=""` vazio como fallback silencioso: esconde do usuário de leitor de tela uma imagem possivelmente informativa, e nenhum verificador automático consegue pegar — o axe não tem como saber que a imagem importava.
- Entregar com o `alt` "a preencher depois": imagem não resolvida bloqueia o Definition of Done (funcional = 🔴 CRITICAL, informativa = 🟠 HIGH).

Classificações-limite (ex.: uma hero image discutivelmente decorativa) são decisões de padrão: registre no `A11Y-DECISIONS.md` e reutilize.

## Dica para a IA:
Sempre que gerar um componente com imagem, a IA deve se perguntar: *"Se eu remover essa imagem, qual informação o usuário perde?"*. Essa resposta deve ser o seu `alt`.
