# Accessibility: Images & Alternative Text

Descrições de imagens são a ponte entre o visual e o compreensível. Para usuários de leitores de tela, uma imagem sem `alt` é um "buraco negro" de informação.

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
<img src="divisor-bonito.png" alt="">
```
- **Por quê:** O `alt=""` (vazio) diz ao leitor de tela para ignorar a imagem. **Nunca** omita o atributo `alt`, senão o leitor lerá o nome do arquivo (ex: "imagem-123-final.png").

## 4. O Problema do "Excesso de Descrição"
Evite começar com "Imagem de..." ou "Foto de...". O leitor de tela já anuncia que é uma imagem. Vá direto ao ponto.

## Dica para a IA:
Sempre que gerar um componente com imagem, a IA deve se perguntar: *"Se eu remover essa imagem, qual informação o usuário perde?"*. Essa resposta deve ser o seu `alt`.
