# Guia de Drag & Drop

> **Escopo:** Listas reordenáveis, quadros kanban, zonas de soltar arquivo, qualquer coisa ordenável — o padrão de interação mais difícil da APG, e o mais entregue como só-ponteiro.

## 0. A regra da qual todas as outras decorrem

**Arrastar é um atalho, nunca o mecanismo.** A SC 2.5.7 (Dragging Movements, Nível AA) exige que toda operação de arraste tenha uma **alternativa de ponteiro único, sem arrastar** — e a operabilidade por teclado (SC 2.1.1) exige mais um caminho além desse. Construa o desfecho primeiro (mover o item X para a posição Y) e deixe o arraste ser um de três jeitos de chegar lá.

1. **O modelo de teclado:** focar a alça do item → `Espaço`/`Enter` pega (estado anunciado) → setas movem, anunciando cada posição → `Espaço` solta → **`Esc` cancela**, devolvendo o item à origem e dizendo isso. Instruções persistentes alcançáveis via `aria-describedby` na alça — o padrão não é adivinhável.
2. **Os três anúncios** por uma região `role="status"`, desfecho e não evento: *"Fatura.pdf pego, posição 2 de 5"* → *"movido para a posição 3 de 5"* → *"solto na posição 3"* (ou *"reordenação cancelada, devolvido à posição 2"*). Silêncio em qualquer um dos três momentos é como quem usa leitor de tela perde um item no ar.
3. **A alternativa de ponteiro único** (SC 2.5.7): uma affordance explícita que não exige gesto — *Mover para cima / Mover para baixo / Mover para…* no menu do item, ou seleção numerada de posição. É também o caminho de quem usa controle por voz, acionador e toque com limitação motora; em plataforma nativa, exponha como custom actions (ver [Tradução para Plataformas Nativas](guide-platform-native.md)).
4. **A alça é um botão de verdade** com nome acessível que nomeia o item — `aria-label="Reordenar Fatura.pdf"` — nunca um ícone decorativo com listener de mouse. O foco visível acompanha o item durante o movimento inteiro (SC 2.4.7).
5. **Alvos de soltura não falam por cor:** alvos válidos ganham indicador visível a 3:1 (SC 1.4.11) mais uma pista não-cromática (contorno, padrão, linha de inserção), e o alvo atual é nomeado no anúncio, não só destacado.
6. **Zonas de soltar arquivo** são a mesma regra disfarçada: a zona MUST vir acompanhada de um `<input type="file">` de verdade (ou botão que abre um) — "arraste os arquivos para cá" como único caminho é a SC 2.5.7 falhando na primeira interação do fluxo.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 2.5.7 Dragging Movements | AA | todo desfecho de arraste alcançável por ponteiro único, sem arrastar |
| 2.1.1 Teclado | A | pegar, mover, soltar e cancelar sem mouse |
| 4.1.3 Mensagens de Status | AA | pego / movido / solto anunciados |
| 2.4.7 Foco Visível | AA | o foco acompanha visivelmente o item movido |
| 1.4.11 Contraste Não Textual | AA | indicadores de soltura a 3:1, nunca só cor |
