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
