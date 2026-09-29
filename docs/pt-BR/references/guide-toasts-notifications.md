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

## Comportamento esperado (cenários de verificação)

*O que a pessoa que verifica este componente precisa observar — com teclado, depois com leitor de tela no desktop e no celular. São os cenários por trás do `REPORT.md` §3: execute-os, registre o par leitor de tela + navegador, marque cada um como aprovado ou reprovado. Descrevem resultado, nunca implementação.*

**Teclado**
- DADO que estou digitando num campo, QUANDO um toast aparece, ENTÃO o foco continua no campo e nada do que digitei se perde.
- QUANDO um toast carrega uma ação ou um link, ENTÃO ele fica até eu dispensá-lo, e o `Tab` alcança a ação e um botão Fechar.
- QUANDO o toast está com foco e pressiono `Esc`, ENTÃO ele é dispensado.
- QUANDO um toast com "Desfazer" já sumiu, ENTÃO a mesma operação continua ao alcance em outro lugar — no menu do item ou no histórico.

**Leitor de tela, desktop (NVDA + Firefox, JAWS + Chrome ou VoiceOver + Safari)**
- QUANDO um toast aparece, ENTÃO ouço o texto dele uma vez, sem sair do que eu estava lendo; toast de erro interrompe, toast de status espera a vez.
- QUANDO três eventos iguais acontecem, ENTÃO ouço uma mensagem colapsada ("3 itens arquivados"), não três anúncios.
- QUANDO navego até o toast, ENTÃO ouço o texto e depois "Fechar, botão" — o controle de fechar tem nome.

**Leitor de tela, celular (TalkBack ou VoiceOver, navegação por deslize)**
- QUANDO um toast aparece, ENTÃO ouço o texto dele uma vez e minha posição na página não muda.
- QUANDO deslizo até um toast persistente, ENTÃO alcanço a ação e "Fechar, botão", e o toque duplo em Fechar o remove.

*Critérios de sucesso cobertos: 4.1.3 Mensagens de Status (AA) · 2.2.1 Tempo Ajustável (A) · 2.1.1 Teclado (A) · 1.4.13 Conteúdo em Hover ou Foco (AA)*
