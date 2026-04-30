# Guia de Acessibilidade: Forms

Formulários (Forms) são o ponto de falha mais crítico para a acessibilidade. Um formulário que não pode ser preenchido por todos é um produto quebrado.

## Bons Exemplos (Good Examples)

### 1. Labels Explícitas e Helper Text
```html
<div class="form-group">
  <label for="email-field">Email Address</label>
  <input type="email" id="email-field" aria-describedby="email-help" required>
  <p id="email-help">Nós nunca compartilharemos seu e-mail.</p>
</div>
```
- **Por quê:** A `label` está explicitamente vinculada ao `id`. O `aria-describedby` vincula o helper text ao input para os screen readers.

### 2. Tratamento de Erros (Error Handling)
```html
<div class="form-group error">
  <label for="password-field">Password</label>
  <input type="password" id="password-field" aria-invalid="true" aria-errormessage="pass-error">
  <p id="pass-error" role="alert">Password must be at least 8 characters.</p>
</div>
```
- **Por quê:** `aria-invalid` sinaliza o estado de erro. O `role="alert"` garante que o screen reader anuncie o erro imediatamente.

## Maus Exemplos (Bad Examples)

### 1. Placeholder como Label
```html
<input type="text" placeholder="Enter your username">
```
- **Implicação:** Placeholders desaparecem ao digitar, perdendo o contexto. Frequentemente falham nos requisitos de contraste e não são lidos de forma confiável pelos screen readers como labels.

### 2. Informação Apenas por Cor
```html
<input type="text" style="border: 1px solid red;">
```
- **Implicação:** Usuários daltônicos ou com baixa visão podem não ver a mudança na borda. Sempre adicione um ícone ou texto indicando o erro.

## Implicações de Acessibilidade
- **Cognitive Load:** Labels explícitas reduzem o esforço necessário para lembrar para que serve um campo.
- **Predictability:** O uso de tipos de input padrão (email, tel, date) permite que os browsers forneçam teclados especializados e preenchimento automático (autofill).
