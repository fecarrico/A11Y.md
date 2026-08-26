# A11y Verification Report (Template)

Este relatório compila as evidências de conformidade para uma determinada *Feature*, garantindo que seu desenvolvimento atingiu a definição de "Certification Ready".

> Este relatório é um **registro versionado do projeto** — nunca adicione ao `.gitignore`. Evidência escondida do controle de versão não é evidência: QA e liderança verificam antes do release, e auditorias leem depois.

> **Legenda de marcação (obrigatória):**
> `[x]` verificado, com a evidência descrita ao lado · `[!]` verificado e **reprovado** (corrija, ou abra entrada no `EXCEPTIONS.md`) · `[~]` verificado parcialmente, com o que falta escrito · `[ ]` **não verificado** — o motivo MUST estar escrito ao lado.
> Marcar `[x]` sem evidência reproduzível invalida o relatório inteiro.

> **Agentes headless.** Uma IA sem navegador MUST gerar este relatório mesmo assim, marcando com `[ ]` todo checkpoint que exija navegador ou tecnologia assistiva, com o motivo e quem deve executá-lo. Relatório parcial e honesto é evidência; relatório ausente não é. O status geral é CONDICIONAL — nunca PASS — enquanto restar qualquer `[ ]` ou `[!]`.

---

## 📌 Contexto da Validação
- **Funcionalidade/Épico:** [Ex: Checkout Integrado]
- **Data do Teste:** [DD/MM/AAAA — a data desta revisão; atualize sempre que a interface mudar]
- **Cobre a interface em:** [commit / build / versão contra a qual este relatório foi verificado]
- **Status de Conformidade:** [✅ PASS | ⚠️ CONDICIONAL (Passa com Exceções) | 🚫 FAIL]
- **Independência da Verificação:** [cross-agent | fresh-context | self-reported] — *quem verificou: [modelo/agente e sessão, ex.: "Claude Code, sessão nova sobre o repo" ou "Copilot auditando saída gerada pelo Cursor"]*

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
- [ ] **Screen Reader Test:** Realizou a tarefa principal com **pelo menos um par leitor de tela + navegador**, nomeado aqui? *(Registre o par, não só o leitor: NVDA + Firefox, JAWS + Chrome e VoiceOver + Safari divergem em comportamento ARIA, e "usei NVDA" não é evidência reproduzível. Se o produto tem público corporativo em Windows, JAWS + Chrome é o par que falta na maioria dos relatórios.)*
  - Par(es) usado(s): [ex.: NVDA 2026.1 + Firefox 141 · macOS VoiceOver + Safari 18]
  - Quem executou e quando: [nome — AAAA-MM-DD]
- [ ] **Controle por Voz:** Todo controle visível pode ser acionado **falando o rótulo visível dele**? *(SC 2.5.3 — um `aria-label` que substitui o texto visível torna o controle inalcançável por voz. Nomeie a ferramenta usada, ou declare que os nomes foram conferidos contra os rótulos por leitura.)*
  - Ferramenta ou método: [ex.: Voice Control do iOS · Voice Access do Android · leitura dos nomes acessíveis contra os rótulos visíveis]
- [ ] **Mudança de Status (`aria-live`):** Erros de formulário, loading states ou atualizações não visuais são corretamente anunciadas?
- [ ] **Preenchimento de Formulários:** Labels corretas e relacionadas (`for` e `id`) em todos os inputs?

## 4. Percepção Visual e Compreensão
Testes que validam contraste e estrutura visual (sem dependência de cores).
- [ ] **Contraste de Texto & UI:** Todos os textos possuem ratio 4.5:1 e componentes essenciais 3:1?
- [ ] **Redundância:** Erros e alertas não comunicam informações exclusivas por meio de cores *(ex: sempre usam Cor + Ícone + Texto)*.
- [ ] **Scale / Zoom:** Texto redimensionado a 200% sem perda (SC 1.4.4) e conteúdo em reflow a 320 CSS px — ≈400% de zoom num viewport de 1280px (SC 1.4.10) — com tudo operável e sem rolagem bidimensional?

## 5. Mídia Temporal e Movimento
*Se esta interface não tem vídeo, áudio nem movimento disparado por scroll, escreva "N/A — sem mídia temporal" aqui e pule o bloco.*
- [ ] **Classificação:** Todo vídeo/áudio classificado **junto com o desenvolvedor** como informativo, funcional ou decorativo *(Media Evidence, §2 — a IA não decide isso sozinha; casos de fronteira registrados no `A11Y-DECISIONS.md`)*.
- [ ] **Alternativas:** Legendas sincronizadas (SC 1.2.2), transcrição disponível, audiodescrição onde o visual carrega o que a trilha não diz (SC 1.2.5) — **revisadas por humano**, nunca entregues como saída bruta de máquina.
- [ ] **Autoplay e Conteúdo em Movimento:** Nenhum áudio começa sozinho sem controle (SC 1.4.2); movimento automático acima de 5 segundos tem mecanismo de pausar/parar/ocultar (SC 2.2.2); nada pisca mais de três vezes por segundo (SC 2.3.1).
- [ ] **Movimento Reduzido:** Interface validada uma vez com `prefers-reduced-motion: reduce` ativo — a mídia não toca sozinha, o parallax degrada para composição estática.
- [ ] **Texto sobre Mídia:** Contraste do texto sobre vídeo medido contra o scrim, no pior caso composto (o frame mais claro visto através da camada) — não estimado a olho.

## 6. Carga Cognitiva e Fluxo
*Aplica-se a qualquer fluxo com mais de uma etapa, autenticação ou limite de tempo.*
- [ ] **Nada para lembrar:** Nenhum passo exige que o usuário guarde informação de outra tela. Campos de senha aceitam colar e declaram `autocomplete`; nenhum CAPTCHA de transcrição sem alternativa (SC 3.3.8).
- [ ] **Nada para redigitar:** Informação já fornecida no mesmo processo é preenchida automaticamente ou oferecida para seleção; o estado sobrevive ao botão Voltar (SC 3.3.7).
- [ ] **Ajuda no mesmo lugar:** Existindo mecanismo de ajuda, ele aparece na mesma ordem relativa em todas as telas do fluxo (SC 3.2.6).
- [ ] **Espaçamento de texto:** Nada é cortado ou sobreposto com entrelinha 1,5×, parágrafo 2×, letras 0,12× e palavras 0,16× (SC 1.4.12).
- [ ] **Tempo:** Todo limite pode ser desligado, ajustado ou estendido, com aviso (SC 2.2.1).
- [ ] **Necessidades conflitantes:** Se alguma decisão atendeu uma necessidade de acessibilidade às custas de outra, as duas populações estão nomeadas e a escolha está registrada no `A11Y-DECISIONS.md`.

---
## 7. Desempenho Funcional *(opcional — EN 301 549 / NBR 17225 Anexo B / VPAT)*
*Preencha quando o relatório embasa uma declaração formal. Para cada afirmação, registre como o produto sustenta o uso:*
- **Sem visão:** [ ]
- **Com visão limitada:** [ ]
- **Sem percepção de cor:** [ ]
- **Sem audição:** [ ]
- **Com audição limitada:** [ ]
- **Sem capacidade vocal:** [ ]
- **Com manipulação ou força limitadas:** [ ]
- **Com alcance limitado:** [ ]
- **Minimizando gatilhos de crise fotossensível:** [ ]
- **Com cognição limitada:** [ ]

---
## 📝 Notas de Avaliação ou Bloqueios Conhecidos
*Descreva se houve algum comportamento de exceção detectado ou quais medidas foram abertas no `EXCEPTIONS.md`*

- **Nota 1:** [Escreva a nota...]
- **Nota 2:** [Escreva a nota...]
