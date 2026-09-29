# Guia de Acessibilidade: Forms

> Escopo: Vinculação de labels, mensagens de erro, agrupamento de campos e padrões acessíveis de formulário.

## Bons Exemplos

### 1. Labels Explícitas e Helper Text
```html
<div class="form-group">
  <label for="email-field">Email Address</label>
  <input type="email" id="email-field" aria-describedby="email-help" required>
  <p id="email-help">Nós nunca compartilharemos seu e-mail.</p>
</div>
```
- **Por quê:** A `label` está explicitamente vinculada ao `id`. O `aria-describedby` vincula o helper text ao input para os screen readers.

### 2. Tratamento de Erros
```html
<div class="form-group error">
  <label for="password-field">Password</label>
  <input type="password" id="password-field" aria-invalid="true" aria-errormessage="pass-error">
  <p id="pass-error" role="alert">Password must be at least 8 characters.</p>
</div>
```
- **Por quê:** `aria-invalid` sinaliza o estado de erro. O `role="alert"` garante que o screen reader anuncie o erro imediatamente.

### 3. Agrupamento com `fieldset` e `legend`
```html
<fieldset>
  <legend>Forma de entrega</legend>
  <label><input type="radio" name="entrega" value="retirada"> Retirar na loja</label>
  <label><input type="radio" name="entrega" value="motoboy"> Entrega por motoboy</label>
</fieldset>
```
- **Por quê:** A `legend` é o nome do grupo — o leitor de tela a diz antes da primeira opção, e "Retirar na loja" é ouvido como resposta a "Forma de entrega" (SC 1.3.1). Grupos de radio, checkboxes relacionados e as partes de uma mesma resposta (dia / mês / ano) são grupos; uma `<div class="form-group">` é classe de CSS, invisível para a tecnologia assistiva. Os controles em si — checkbox, radio, switch, slider, select nativo — estão especificados em [Controles de Formulário](guide-form-controls.md).

## Maus Exemplos

### 1. Placeholder como Label
```html
<input type="text" placeholder="Enter your username">
```
- Ver *Placeholder Labels* — core §6.

### 2. Informação Apenas por Cor
```html
<input type="text" style="border: 1px solid red;">
```
- Ver *Semantic Redundancy* — core §3.

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO um formulário, QUANDO entro num campo com `Tab`, ENTÃO o rótulo continua visível ao lado enquanto digito — não some como um placeholder.
- QUANDO envio com um campo inválido, ENTÃO o erro aparece como texto junto do campo, não só como borda vermelha.
- QUANDO percorro o formulário com `Tab`, ENTÃO alcanço todos os campos e o botão de envio — nada exige o mouse.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO chego a um campo com `Tab`, ENTÃO ouço o rótulo, o tipo do campo, "obrigatório" quando for, e o texto de ajuda.
- QUANDO envio com um campo inválido, ENTÃO ouço a mensagem de erro na hora, sem sair do lugar.
- QUANDO volto a esse campo, ENTÃO ouço "inválido" e o texto do erro junto com o rótulo.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO deslizo até um campo, ENTÃO ouço o rótulo e o texto de ajuda antes de tocar duas vezes para editar.
- QUANDO toco duas vezes em Enviar com um campo inválido, ENTÃO ouço a mensagem de erro.
