# Accessibility: Content, Interaction & Timing

> Escopo: Microcopy, gestão de timeouts, feedback aria-live, linguagem sensorial e orientações para IA de conteúdo. *(Vídeo, áudio e movimento estão em [Mídia Temporal & Movimento](guide-media.md).)*

## 1. Microcopy & Clareza
A linguagem deve ser a mais simples possível para reduzir a carga cognitiva.
- **Instruções Claras:** Evite jargões. Use verbos de ação (ex: "Enviar" em vez de "Processar").
- **Identificação de Campos:** Instruções sobre formatos (ex: "DD/MM/AAAA") devem estar fora do input e lincadas via `aria-describedby`.
- **Heading Content:** O texto dos títulos deve descrever claramente a seção que o segue.

## 2. Gestão de Tempo (Timeouts)
Muitos usuários levam mais tempo para ler ou interagir com o sistema.
- **Não Remova o Tempo sem Aviso:** Se uma sessão for expirar, o usuário **MUST** ser avisado com antecedência e ter a opção de estender o tempo.
- **Conteúdo em Movimento:** Carrosséis ou conteúdos que se atualizam sozinhos **MUST** ter um botão de "Pausa".

## 3. Feedback Sistêmico & Mensagens de Status (Aria-live)
Mudanças dinâmicas que não causam recarregamento de página precisam ser anunciadas.
- **Status Updates:** Use `aria-live="polite"` para notificações não críticas (ex: "Item adicionado ao carrinho").
- **Erros Críticos:** Use `aria-live="assertive"` ou `role="alert"` para erros que impedem o progresso imediato.
- **Progresso:** Se uma ação demorar, use um indicador de progresso programático que informe o status da tarefa.

## 4. Linguagem Sensorial
- **Linguagem Sensorial:** **MUST NOT** dar instruções baseadas apenas em sentidos (ex: "Clique no botão redondo à direita" ou "Ouça o sinal para começar"). Use referências de texto/contexto (ex: "Clique no botão Enviar ao final do formulário").
- **Mídia temporal** (legendas, transcrições, audiodescrição, vídeo de fundo, autoplay e parallax) tem guia próprio: [Mídia Temporal & Movimento](guide-media.md). A regra que dispara quando a mídia entra no código é a *Media Evidence*, Seção 2 do arquivo central.

## 5. Dica para a IA de Conteúdo
Ao gerar textos para a interface, a IA deve validar se a instrução sobrevive sem o contexto visual: *"Se eu não estivesse vendo a tela, essa instrução ainda faria sentido?"*.
