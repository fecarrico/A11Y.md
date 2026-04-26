# Exemplos Práticos: Acessibilidade na Prática (A11Y)

Este documento complementa o [**A11Y.md**](A11Y.md) com exemplos reais extraídos do cotidiano de desenvolvimento, contrastando implementações que violam as normas com suas versões corrigidas e acessíveis.

---

## 1. Interação Semântica e Operabilidade
**Cenário:** Cards de dashboard que servem como atalhos de navegação.

### 🔴 RUIM (Anti-padrão)
O uso de `div` com `onClick` impossibilita que usuários de teclado ou tecnologias assistivas percebam o elemento como interativo.

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

### ✅ ACESSÍVEL
O uso de uma tag semântica (`button` ou `a`) garante foco nativo, suporte a tecla Enter/Espaço e anúncio correto pelo leitor de tela.

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

> **Por que? (A11Y.md - Seção 6):** "MUST NOT usar div ou span para ações de clique. Prefira botões nativos... para garantir o comportamento de foco e eventos de teclado."

---

## 2. Tipografia e Legibilidade
**Cenário:** Metadados secundários ou legendas em cards.

### 🔴 RUIM (Anti-padrão)
Fontes abaixo de 12px reduzem drasticamente a legibilidade para usuários com baixa visão ou em dispositivos com brilho reduzido.

```tsx
// TokenList.tsx
<p className="text-[10px] text-gray-500 mt-1.5">
  Última sincronização há 2 horas
</p>
```

### ✅ ACESSÍVEL
Manter o mínimo de 12px (`text-xs` no Tailwind padrão) garante conformidade. Se a densidade for crítica, aumentar o contraste para compensar.

```tsx
// TokenList.tsx
<p className="text-xs text-gray-700 font-medium mt-1.5">
  Última sincronização há 2 horas
</p>
```

> **Por que? (A11Y.md - Seção 4):** "Texto MUST NOT ser menor que 12px. O sucesso da percepção é garantido pela escala legível."

---

## 3. Formulários e Relacionamentos
**Cenário:** Campos de input em telas de autenticação ou configuração.

### 🔴 RUIM (Anti-padrão)
Labels sem conexão técnica com o input impedem que o leitor de tela anuncie o nome do campo ao focar nele.

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

### ✅ ACESSÍVEL
Uso obrigatório de `id` no input e `htmlFor` na label para criar o vínculo semântico.

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

> **Por que? (A11Y.md - Seção 3):** "Formulários MUST ter labels explícitas conectadas via id e for. Evite re-invenções que quebrem os eventos nativos."

---

## 4. Feedback Dinâmico
**Cenário:** Notificações de erro ou sucesso que aparecem após uma ação.

### 🔴 RUIM (Anti-padrão)
Mensagens injetadas no DOM programaticamente são ignoradas por leitores de tela se não houver um alerta ativo.

```tsx
// Notification.tsx
{error && (
  <div className="p-3 bg-red-100 text-red-700 border border-red-500">
    {error}
  </div>
)}
```

### ✅ ACESSÍVEL
Inclusão de atributos ARIA para garantir que a mudança de estado seja anunciada imediatamente.

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

> **Por que? (A11Y.md - Seção 3):** "Eventos dinâmicos baseados no estado... MUST ser lidos ou informados ativamente através de regiões aria-live ou role='alert'."

---

## Resumo de Severidade
| Problema | Nível | Impacto |
| :--- | :--- | :--- |
| Clique em `Div` | 🔴 **CRITICAL** | Bloqueia usuários de teclado. |
| Falta de `role="alert"` | 🟠 **HIGH** | Usuário cego não sabe se houve erro. |
| Fonte < 12px | 🟠 **HIGH** | Dificulta leitura e causa fadiga ocular. |
| Label desconectada | 🟠 **HIGH** | Perda de contexto em formulários. |
