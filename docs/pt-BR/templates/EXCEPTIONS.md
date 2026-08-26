# A11y Exceptions Log (Template)

Este documento registra os desvios conhecidos em relação aos padrões de acessibilidade (WCAG 2.2 AA / EN 301 549) que foram aceitos temporariamente.

> **Objetivo:** Fornecer transparência técnica e legal, documentando *onde*, *por que* e *como* mitigamos temporariamente diretrizes que não puderam ser cumpridas devido a limitações técnicas, de plataforma ou escopo.

> **Regras:**
> 1. Exceção é **temporária** e não muda o requisito.
> 2. Toda exceção MUST ter **dono do risco**, **aprovador**, **issue de rastreio** e **data de expiração** — "dependente de third-party" também ganha data de revisão.
> 3. O escopo é o **mínimo praticável**: um componente/seletor, nunca uma regra inteira.
> 4. Na expiração, a exceção é revisada: corrigida e removida, ou renovada conscientemente com nova data. **Nunca suprimida em silêncio.**
> 5. **Dever da IA:** em modo revisão, a IA MUST sinalizar qualquer exceção vencida como débito técnico 🟠 HIGH.
> 6. Este log é um **registro versionado do projeto** — nunca adicione ao `.gitignore`. Exceções precisam aparecer nos pull requests e ser auditáveis depois; registro de risco escondido do controle de versão não protege ninguém.

---

## 🛑 Registro de Exceção

### 1. Detalhes Básicos
- **ID da Exceção:** [Ex: EXT-2026-001]
- **Componente / Página:** [Ex: Tabela Dinâmica do Dashboard Financeiro]
- **Diretriz WCAG Afetada:** [Ex: 2.1.1 Keyboard (A) e 1.4.3 Contrast (Minimum) (AA)]
- **Severidade (Impacto no Usuário):** [🔴 Critical | 🟠 High | 🟡 Medium | 🔵 Low]
- **Dono do Risco:** [Quem responde por este desvio — uma pessoa, não um time]
- **Aprovado por:** [Quem assinou a aceitação do risco — lead/PO/QA]
- **Issue de Rastreio:** [Link do item de backlog onde esta dívida é cobrada]

### 2. Descrição Técnica do Bloqueio
- **O que está quebrado?** [Explique detalhadamente o que o usuário não consegue fazer].
- **Por que ocorreu?** [Declare a limitação: Ferramenta de terceiros sem suporte, arquitetura de UI antiga impossível de refatorar no ciclo atual, etc].

### 3. Solução de Contorno (Fallback / Remediation)
- **Como o usuário ainda pode concluir a tarefa?** [Acessibilidade é precondição. Se o gráfico não é acessível com teclado, existe uma tabela em texto narrando os resultados? Existe uma opção via suporte?]

### 4. Plano de Resolução e Expiração
- **Expiração (data de revisão):** [AAAA-MM-DD — obrigatória. Nesta data a exceção é corrigida, ou renovada conscientemente com nova data]
- **Critério para Resolução:** [O que precisa acontecer para que essa exceção deixe de existir?]
