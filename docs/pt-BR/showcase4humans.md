# 🖼️ Showcase: Acessibilidade na Prática (Para Humanos)

Seja muito bem-vindo(a)! 👋

Este documento é a **vitrine de exemplos práticos** do padrão A11Y.md. Ele foi escrito para nós, humanos, que muitas vezes criamos componentes seguindo a intuição visual, mas acabamos acidentalmente criando barreiras para quem usa leitores de tela ou teclado.

Aqui, vamos contrastar a "forma que estamos acostumados a fazer" com a "forma acessível e semântica".

> 💡 **De onde vieram esses exemplos?**
> Os anti-padrões mostrados aqui foram gerados ao utilizar o projeto A11Y.md como um reviewer do código de um sistema gerado pelo **Gemini 3 Flash** dentro dos ambientes do **Figma Make** e do **Antigravity**. Isso reforça a importância desse projeto: o modelo e os ambientes que mais utilizamos cometem erros básicos de acessibilidade. Ou seja, estamos gerando código rápido, mas também corremos o risco de colocar mais inacessibilidade no mundo em larga escala.

---

## 1. O "Botão" que Não é Botão (Interação e Operabilidade)

**Cenário:** Você está criando um card em um Dashboard que serve como atalho para outra página.

### 🔴 O Jeito Comum (Anti-padrão)
O instinto de muitos desenvolvedores (e até da IA às vezes) é criar uma `div` e colocar um `onClick` nela. Visualmente funciona, mas para quem navega por teclado (usando a tecla `Tab`), essa `div` **simplesmente não existe**. Ela não recebe foco e não pode ser ativada com Enter.

```tsx
// OverviewCard.tsx
<div 
  onClick={() => navigate('/components')} 
  className="glass-panel p-6 cursor-pointer hover:border-blue-500"
>
  <Puzzle className="w-5 h-5" />
  <p className="text-3xl font-bold">120</p>
  <p className="text-xs font-semibold uppercase">Componentes</p>
</div>
```

### ✅ O Jeito Acessível
Se algo pode ser clicado para disparar uma ação ou navegação, deve ser uma tag semântica (`button` ou `a`). Ao fazer isso, o navegador já resolve de graça o foco, o suporte às teclas Enter/Espaço e o anúncio correto no leitor de tela.

```tsx
// OverviewCard.tsx
<button 
  onClick={() => navigate('/components')}
  aria-label="Ver lista de componentes (120 indexados)"
  className="glass-panel p-6 text-left hover:border-blue-500 focus:ring-2 focus:ring-blue-500 outline-none"
>
  <Puzzle className="w-5 h-5" aria-hidden="true" />
  <p className="text-3xl font-bold">120</p>
  <p className="text-xs font-semibold uppercase">Componentes</p>
</button>
```

> 💡 **Lembre-se:** Nunca use `div` ou `span` para interações de clique.

---

## 2. A "Letra Miúda" (Tipografia e Legibilidade)

**Cenário:** Você precisa encaixar muitas informações em um card pequeno, como uma legenda de "Última atualização".

### 🔴 O Jeito Comum (Anti-padrão)
Para fazer o design "respirar", diminuímos a fonte para `10px` e clareamos a cor. Para usuários com baixa visão ou em monitores com brilho ruim, esse texto se torna invisível.

```tsx
// TokenList.tsx
<p className="text-[10px] text-gray-500 mt-1.5">
  Última sincronização há 2 horas
</p>
```

### ✅ O Jeito Acessível
Mantenha o tamanho mínimo de `12px` (no Tailwind, isso equivale a `text-xs`). Se a cor for muito clara, aumente o contraste deixando-a um pouco mais escura.

```tsx
// TokenList.tsx
<p className="text-xs text-gray-700 font-medium mt-1.5">
  Última sincronização há 2 horas
</p>
```

> 💡 **Exceção à regra:** Se o seu Design System exigir `10px` para uma tag/badge, você é obrigado a compensar isso com altíssimo contraste (Nível AAA, 7:1) contra o fundo.

---

## 3. O Campo "Órfão" (Formulários e Relacionamentos)

**Cenário:** Criar uma tela de login simples.

### 🔴 O Jeito Comum (Anti-padrão)
O campo e o rótulo (label) estão próximos visualmente, então quem enxerga entende a relação. Mas tecnicamente, eles estão soltos. Quando um leitor de tela foca no input, ele diz apenas "Caixa de texto", e o usuário não sabe se ali vai o e-mail ou a senha.

```tsx
// AuthForm.tsx
<label className="block text-xs font-semibold uppercase">
  E-mail
</label>
<input
  type="email"
  placeholder="nome@empresa.com"
  className="w-full px-4 py-3 border rounded-xl"
/>
```

### ✅ O Jeito Acessível
Ligue a `label` ao `input` usando `htmlFor` (em React) ou `for` apontando para o `id` do input. Outra vantagem? Se o usuário clicar na palavra "E-mail", o input já ganha o foco automaticamente!

```tsx
// AuthForm.tsx
<label 
  htmlFor="auth-email" 
  className="block text-xs font-semibold uppercase"
>
  E-mail
</label>
<input
  id="auth-email"
  type="email"
  required
  placeholder="nome@empresa.com"
  className="w-full px-4 py-3 border rounded-xl focus:ring-2"
/>
```

---

## 4. O Alerta Silencioso (Feedback Dinâmico)

**Cenário:** O usuário envia um formulário e ocorre um erro. Um balão vermelho aparece na tela.

### 🔴 O Jeito Comum (Anti-padrão)
O React renderiza a mensagem na tela. Mas quem usa leitor de tela não recebe **nenhum aviso acústico** de que um erro acabou de brotar na interface, e fica esperando a tela carregar eternamente.

```tsx
// Notification.tsx
{error && (
  <div className="p-3 bg-red-100 text-red-700 border border-red-500">
    {error}
  </div>
)}
```

### ✅ O Jeito Acessível
Adicione `role="alert"` (ou `aria-live="assertive"`). Assim, no momento exato em que a mensagem aparecer no DOM, o leitor de tela vai interromper o que está falando e avisar o usuário imediatamente sobre o erro.

```tsx
// Notification.tsx
{error && (
  <div 
    role="alert" 
    aria-live="assertive"
    className="p-3 bg-red-100 text-red-700 border border-red-500"
  >
    {error}
  </div>
)}
```

---

## 🚨 O Peso de Cada Erro

Não sabe priorizar? Aqui vai um guia rápido do que focar primeiro:

| O que quebrou? | Gravidade | O que o usuário sente na pele? |
| :--- | :--- | :--- |
| **Clique em `div`** | 🔴 **CRÍTICO** | *"Não consigo clicar nesse botão com o teclado."* |
| **Erro sem `role="alert"`** | 🟠 **ALTO** | *"Apertei salvar e nada aconteceu, estou preso."* |
| **Fonte minúscula (< 12px)** | 🟠 **ALTO** | *"Minha vista dói tentando ler as datas."* |
| **Label solta do input** | 🟠 **ALTO** | *"Foquei no campo mas não sei o que digitar aqui."* |

> Quer se aprofundar em casos mais complexos? Confira nossos guias técnicos completos na pasta `references/`!
