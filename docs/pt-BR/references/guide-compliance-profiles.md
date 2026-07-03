# Perfis de Conformidade A11y

> **Escopo:** Geração por IA & Auditorias

Acessibilidade não é um monólito. Enquanto a **WCAG 2.2 AA** é o padrão da indústria e base legal, diferentes estágios de um projeto exigem diferentes níveis de rigor.

Este guia detalha os três perfis de conformidade suportados pelas regras do `A11Y.md`.

---

## Os Perfis

| Perfil | Padrão Alvo | Caso de Uso Principal | Foco |
| :--- | :--- | :--- | :--- |
| **🛡️ Shield (AAA)** | WCAG 2.2 AAA | Indústrias reguladas, software especializado | Inclusividade máxima, zero barreiras |
| **⚖️ Standard (AA)** | WCAG 2.2 AA | Apps de produção (Padrão) | Conformidade legal, usabilidade ampla |
| **🚀 Launchpad (A)** | WCAG 2.2 A | MVPs, ferramentas internas, protótipos | Base mínima absoluta |

---

## 1. 🛡️ Perfil Shield (Nível AAA)
*O mais alto padrão de acessibilidade web.*

**Quando usar:** Aplicações para governo, saúde, educação, ou públicos especializados.
**Instrução IA:** `"Apply Shield Profile (AAA)"`

### Principais Requisitos (Além do AA)
- **Contraste:** Texto deve ter um ratio de **7:1** contra o fundo. Textos grandes (18pt+) exigem **4.5:1**.
- **Sem Exceções de Densidade:** Mesmo badges pequenos devem atender ao ratio 7:1.
- **Targets:** Todos os elementos clicáveis devem ter pelo menos **48×48px**.
- **Foco:** O indicador de foco deve ser altamente visível (ex: linha sólida 2px com alto contraste) e não depender do padrão do navegador.
- **Timeouts:** Usuários devem conseguir completar tarefas sem limites de tempo arbitrários.

---

## 2. ⚖️ Perfil Standard (Nível AA)
*O benchmark global para conformidade legal (ADA, EAA).*

**Quando usar:** Este é o **padrão**. Use para qualquer software em produção, site público ou produto comercial.
**Instrução IA:** `"Apply Standard Profile (AA)"`

### Principais Requisitos
- **Contraste:** Texto deve ter ratio **4.5:1**. Elementos de UI (bordas, ícones) devem ter **3:1**.
- **Targets:** Elementos clicáveis devem ter no mínimo **44×44px**. Exceções existem para links inline.
- **Foco:** O foco deve ser claramente visível.
- **HTML Semântico & ARIA:** Aderência estrita aos padrões APG para componentes complexos.
- **Responsividade:** Deve suportar zoom de até 200% sem perda de conteúdo.

---

## 3. 🚀 Perfil Launchpad (Nível A)
*O piso absoluto. Abaixo disso, o software é considerado quebrado.*

**Quando usar:** Prototipação rápida, painéis internos, ou primeiras versões MVP.
**Instrução IA:** `"Apply Launchpad Profile (A)"`

> [!WARNING]  
> O perfil Launchpad **NÃO** significa "sem acessibilidade". Ele ainda exige HTML semântico, operabilidade por teclado e suporte a leitores de tela. Ele apenas flexibiliza critérios visuais estritos.

### Critérios Flexibilizados (Comparado ao AA)
- **Contraste:** Apenas um ratio mínimo de **3:1** é forçado.
- **Targets:** Tamanhos de clique podem ser reduzidos para **24×24px**, se houver espaçamento.
- **Tipografia:** Fontes até **10px** são toleradas sem compensação estrita de contraste AAA.

### Regras Imutáveis (NUNCA flexibilizadas)
- ❌ `div` ou `span` com `onClick` (armadilha de teclado)
- ❌ Falta de `alt` em imagens críticas
- ❌ Falta de `label` em inputs de formulário
- ❌ Modais sem gerenciamento de foco (focus trap)
- ❌ Mudanças de estado sem avisos em `aria-live` ou role alerts

Qualquer uso do Launchpad em produção deve ser documentado no `EXCEPTIONS.md` como débito técnico a ser evoluído para o Standard (AA).
