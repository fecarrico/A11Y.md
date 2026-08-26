# Guia de Toasts & Notificações

> **Escopo:** Toasts, snackbars, banners, mensagens de status.

## 0. A regra da qual todas as outras decorrem

**Um toast que a pessoa não consegue perceber, alcançar ou que não sobrevive a ela é uma mensagem que nunca foi enviada.** Toasts falham de três jeitos independentes — não anunciado (invisível para leitor de tela), anunciado mas inalcançável (a ação dentro dele some antes de quem usa teclado chegar) e rápido demais para ler. Um toast precisa sobreviver aos três, ou não carregar nada que importe.

1. **`role="status"` é o padrão; `role="alert"` é a exceção** — reservado a erros que exigem atenção imediata. Nunca os dois juntos, e nunca `aria-live` empilhado em cima de qualquer um (o *redundant-alert* que o tooling acusa). A região viva **existe no DOM antes** da primeira mensagem; injete o texto numa região de pé, não injete a região.
2. **Nunca mova o foco para um toast.** Ele sequestra a digitação e o contexto do leitor de tela para algo que se diz passivo. Se uma resposta exige ação *agora*, isso é um diálogo (ver [Modals](guide-modals.md)), não um toast.
3. **Auto-fechamento é só para o inerte.** Toast que carrega **ação ou link MUST persistir** até ser dispensado — ação com cronômetro é limite de tempo (SC 2.2.1) que quem usa zoom, leitor de tela ou reage devagar perde. Toasts puramente informativos que se fecham sozinhos ficam tempo suficiente para serem lidos (base de ~6 segundos, crescendo com o tamanho da mensagem).
4. **A ação também mora em algum lugar permanente.** "Desfazer" que só existe num toast de 5 segundos é funcionalidade com prazo de validade; a mesma operação pertence ao menu do item ou ao histórico. O toast é atalho de conveniência, não o endereço da funcionalidade.
5. **Dispensável por teclado:** um `<button>` de fechar de verdade, com nome, alcançável por `Tab` — e `Esc` dispensa o toast focado.
6. **Mesmo canal, mesmo lugar:** toasts aparecem em posição consistente no produto inteiro; repetições colapsam (*"3 itens arquivados"*) em vez de empilhar uma torre que o leitor anuncia uma a uma.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 4.1.3 Mensagens de Status | AA | a mensagem é anunciada sem receber foco |
| 2.2.1 Tempo Ajustável | A | nada acionável desaparece por cronômetro |
| 2.1.1 Teclado | A | dispensar e agir sem mouse |
| 1.4.13 Conteúdo em Hover ou Foco | AA | pausar no hover não pode ser o único jeito de segurar o toast |
