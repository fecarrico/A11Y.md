# A11y Verification Report (Template)

Este relatório compila as evidências de conformidade para uma determinada *Feature*, garantindo que seu desenvolvimento atingiu a definição de "Certification Ready".

---

## 📌 Contexto da Validação
- **Funcionalidade/Épico:** [Ex: Checkout Integrado]
- **Data do Teste:** [DD/MM/AAAA]
- **Status de Conformidade:** [✅ PASS | ⚠️ CONDICIONAL (Passa com Exceções) | 🚫 FAIL]

## 1. Verificação Técnica (Automated & Semantics)
Evidências obtidas via validadores estáticos para garantir base técnica estrutural.
- [ ] **Axe-Core / Lighthouse:** Zero violações "Critical" ou "Serious"? *(Anexar print ou score - Ex: Score 98)*
- [ ] **Semântica HTML:** Substituição apropriada de `div`s genéricas por endpoints interativos (`button`, `a`, etc.)?
- [ ] **Hierarquia de Títulos (H1-H6):** Respeitada e sem saltos de nível?

## 2. Tab Order e Focus Management
Validação puramente por teclado (sem uso do mouse).
- [ ] **Indicador de Foco:** O anel de foco (Focus Ring) nunca foi suprimido e atende ao requisito de contraste visual (mínimo 3:1)?
- [ ] **Navegação Lógica:** A tecla `Tab` segue a ordem visual correta da interface?
- [ ] **Foco Capturado (Modals/Overlays):** Ao abrir modais, o foco é preso dentro do componente e pode ser fechado via tecla `Escape`?

## 3. Comportamento e Retorno de Tarefas
Caminhos críticos da funcionalidade e validação via Leitores de Tela.
- [ ] **Screen Reader Test:** Realizou a tarefa principal usando VoiceOver/NVDA?
- [ ] **Mudança de Status (`aria-live`):** Erros de formulário, loading states ou atualizações não visuais são corretamente anunciadas?
- [ ] **Preenchimento de Formulários:** Labels corretas e relacionadas (`for` e `id`) em todos os inputs?

## 4. Percepção Visual e Compreensão
Testes que validam contraste e estrutura visual (sem dependência de cores).
- [ ] **Contraste de Texto & UI:** Todos os textos possuem ratio 4.5:1 e componentes essenciais 3:1?
- [ ] **Redundância:** Erros e alertas não comunicam informações exclusivas por meio de cores *(ex: sempre usam Cor + Ícone + Texto)*.
- [ ] **Scale / Zoom:** Ao ampliar a tela em 400%, tudo continuou operável e sem bloqueios (overrides de tela)?

---
## 📝 Notas de Avaliação ou Bloqueios Conhecidos
*Descreva se houve algum comportamento de exceção detectado ou quais medidas foram abertas no `EXCEPTIONS.md`*

- **Nota 1:** [Escreva a nota...]
- **Nota 2:** [Escreva a nota...]
