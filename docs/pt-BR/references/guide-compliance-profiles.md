# Perfis de Conformidade A11y

> **Escopo:** Geração por IA & Auditorias

> [!NOTE]
> **Normativo vs Regras da Casa.** Cada perfil mistura duas camadas: **Critérios de Sucesso da WCAG** no seu nível-alvo (citados por número de SC — pular um exige `EXCEPTIONS.md`) e **Regras da Casa†** — a política ergonômica mais estrita deste padrão (marcadas com †; flexibilizar uma é decisão de produto, registrada no `A11Y-DECISIONS.md`). A WCAG **não define fonte mínima** em nenhum nível, e o Nível A **não define critérios de contraste nem de tamanho de alvo** — todo valor nessas posições abaixo é Regra da Casa.

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

### Principais Requisitos (Além do AA)
- **Contraste (SC 1.4.6):** Texto deve ter um ratio de **7:1** contra o fundo. Textos grandes (18pt+) exigem **4.5:1**. Componentes de UI permanecem em 3:1 (SC 1.4.11 — a WCAG não possui critério AAA de contraste não-textual).
- **Sem Exceções de Densidade:** Mesmo badges pequenos devem atender ao ratio 7:1.
- **Targets (SC 2.5.5):** Elementos clicáveis devem ter pelo menos **44×44px** — o mínimo AAA, com as exceções do próprio SC (controle equivalente, alvo inline em texto, controle do user agent, apresentação essencial). **Regra da Casa†:** projete para **48×48px** (norma do Material) e não use exceções de densidade no Shield.
- **Foco (SC 2.4.13 + Regra da Casa†):** O indicador de foco deve ser altamente visível — linha sólida 2px com contraste 3:1 contra o fundo (Regra da Casa; o 3:1 normativo do SC é medido entre os estados focado/não-focado) — e não depender do padrão do navegador.
- **Timeouts:** Usuários devem conseguir completar tarefas sem limites de tempo arbitrários, ou ter mecanismos para estender sessões facilmente.

---

## 2. ⚖️ Perfil Standard (Nível AA)
*O benchmark global para conformidade legal (ADA, EAA).*

**Quando usar:** Este é o **padrão**. Use para qualquer software em produção, site público ou produto comercial.

### Principais Requisitos
- **Contraste (SC 1.4.3, 1.4.11):** Texto deve ter ratio **4.5:1**. Textos grandes, **3:1**. Elementos de UI (bordas, ícones) devem ter **3:1**.
- **Targets (SC 2.5.8):** Elementos clicáveis devem ter no mínimo **24×24px** — o piso normativo AA, com exceções para links inline e alvos espaçados. **Regra da Casa†:** projete para **44×44px** (norma da Apple HIG / Material).
- **Foco (SC 2.4.7):** O foco deve ser claramente visível.
- **HTML Semântico & ARIA:** Aderência estrita aos padrões APG para componentes complexos.
- **Responsividade (SC 1.4.4, 1.4.10):** Texto deve redimensionar até 200% sem perda de conteúdo ou função, e o conteúdo deve refazer o fluxo a 320 CSS px de largura (≈400% de zoom) sem rolagem bidimensional.

---

## 3. 🚀 Perfil Launchpad (Nível A)
*O piso absoluto. Abaixo disso, o software é considerado quebrado.*

**Quando usar:** Prototipação rápida, painéis internos, ou primeiras versões MVP.

> [!WARNING]  
> O perfil Launchpad **NÃO** significa "sem acessibilidade". Ele ainda exige HTML semântico, operabilidade por teclado e suporte a leitores de tela. Ele apenas flexibiliza critérios visuais estritos.

### Critérios Flexibilizados (Comparado ao AA)
- **Contraste (Regra da Casa†):** Apenas um ratio mínimo de **3:1** é forçado, para evitar ilegibilidade completa. (O Nível A não tem critério de contraste — este piso é política deste padrão, não da WCAG.)
- **Targets (Regra da Casa†):** Tamanhos de clique podem ser reduzidos para **24×24px**, se houver espaçamento. (O Nível A não tem critério de tamanho de alvo; 24×24 espelha o piso AA do SC 2.5.8.)
- **Tipografia (Regra da Casa†):** Fontes até **10px** são toleradas sem mitigação estrita de contraste, embora altamente desencorajadas. (A WCAG não define fonte mínima.)

### Regras Imutáveis (NUNCA flexibilizadas)
- ❌ `div` ou `span` com `onClick` (armadilha de teclado)
- ❌ Falta de `alt` em imagens críticas
- ❌ Falta de `label` em inputs de formulário
- ❌ Modais sem gerenciamento de foco (focus trap)
- ❌ Mudanças de estado sem avisos em `aria-live` ou role alerts

Qualquer uso do Launchpad em produção deve ser documentado no `EXCEPTIONS.md` como débito técnico a ser evoluído para o Standard (AA).

## 4. Mapeamento Brasil (ABNT NBR 17225)

Quando o produto serve o Brasil, o perfil declarado informa também seu nível NBR 17225:

| Perfil | Nível NBR 17225 |
| :--- | :--- |
| ⚖️ Standard (AA) | **Regular** — todos os 96 requisitos (declarada equivalente à WCAG 2.2 A+AA) |
| 🛡️ Shield (AAA) | **Plena** — requisitos + todas as 50 recomendações; cada recomendação não atendida carrega justificativa razoável no `EXCEPTIONS.md` |

Estrutura da norma e o checklist de itens críticos do Anexo A: [Governança §6.1](guide-governance.md).
