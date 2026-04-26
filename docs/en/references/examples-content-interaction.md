# Accessibility: Content, Interaction & Timing

A acessibilidade não termina na estrutura HTML. A forma como o conteúdo é escrito e como as interações temporais ocorrem define o sucesso de usuários com deficiências cognitivas, auditivas e de visão.

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

## 4. Sensoriais e Multimídia
- **Linguagem Sensorial:** **MUST NOT** dar instruções baseadas apenas em sentidos (ex: "Clique no botão redondo à direita" ou "Ouça o sinal para começar"). Use referências de texto/contexto (ex: "Clique no botão Enviar ao final do formulário").
- **Legendas e Transcrições:** Áudios e vídeos **MUST** possuir alternativas em texto ou legendas sincronizadas.

## 5. Dica para a IA de Conteúdo
Ao gerar textos para a interface, a IA deve validar se a instrução sobrevive sem o contexto visual: *"Se eu não estivesse vendo a tela, essa instrução ainda faria sentido?"*.
