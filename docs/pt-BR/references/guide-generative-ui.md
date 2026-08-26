# Guia de Interfaces Generativas & Conversacionais

> **Escopo:** Interfaces de chat, saída de modelo em streaming e UI que um modelo monta em tempo de execução — o caso em que a interface **é** a IA.

## 0. A regra da qual todas as outras decorrem

**Saída em streaming e regiões vivas são inimigas naturais.** Uma resposta que chega token a token dentro de um `aria-live="polite"` produz um leitor de tela que ou gagueja a cada fragmento ou recomeça a mensagem inteira a cada mutação. É a falha definidora das UIs de chat geradas, e ela passa em todo verificador automático, porque a marcação está corretíssima.

```tsx
// ❌ Anuncia a mensagem dezenas de vezes enquanto ela cresce
<div aria-live="polite">{textoEmStreaming}</div>

// ✅ O stream renderiza em silêncio; uma região pequena anuncia só a mudança de estado
<div aria-busy={gerando}>{textoEmStreaming}</div>
<div role="status" aria-live="polite" className="sr-only">
  {gerando ? "Gerando resposta" : ultimaConcluida ? "Resposta pronta, 240 palavras" : ""}
</div>
```

**Anuncie as transições, renderize o conteúdo.** A pessoa chega ao texto com os próprios comandos de leitura, quando quiser — que é como ela lê qualquer outro documento.

## 1. A conversa é um log, não um feed

- A lista de mensagens é `role="log"` (um `aria-live="polite"` implícito com `aria-relevant="additions"`): entradas novas são anunciadas, as existentes não são relidas. Nunca `role="alert"`, nunca `aria-live="assertive"` — uma interrupção por mensagem torna a interface inutilizável.
- **Toda mensagem declara quem está falando, em texto.** Cor do avatar, alinhamento e formato do balão são invisíveis para leitor de tela e ambíguos em modo de alto contraste. Um prefixo `Você:` / `Assistente:` visualmente oculto, ou um cabeçalho por turno, resolve inteiro.
- Dê a cada turno um marco ou cabeçalho para conversas longas serem navegáveis por cabeçalho — rolar não é navegar.
- Horários como `<time datetime="…">`, com rótulo legível: "há 2 minutos" sozinho não é resolvível fora de contexto.

## 2. Streaming, parada e espera

1. **`aria-busy="true"`** na região sendo escrita, limpo quando o stream termina.
2. **Um controle de "Parar geração" é requisito, não cortesia** — uma resposta que escreve por quarenta segundos e não pode ser interrompida é conteúdo em movimento do qual a pessoa não consegue escapar (SC 2.2.2). Precisa ser alcançável por teclado *enquanto* o stream roda, e precisa ser o mesmo controle para todo mundo.
3. **Nunca mova o foco por conta própria.** Puxar o foco para a resposta que chega destrói o que a pessoa estava fazendo — digitando, relendo uma resposta anterior. Anuncie que ficou pronta e ofereça um caminho explícito ("Ir para a última resposta") para quem quiser.
4. **Nada pode depender de o stream ter terminado.** Copiar, tentar de novo e citações precisam existir também para resposta parcial, ou quem interrompe cedo fica sem saída.
5. **Sem limite de tempo no compositor.** Sessões que expiram no meio do raciocínio falham a SC 2.2.1 e são piores aqui, onde a entrada é longa.

## 3. O que o modelo renderiza é marcação, não enfeite

Saída de modelo vira UI de verdade, e a semântica precisa sobreviver à conversão:

- **Cabeçalhos viram cabeçalhos de verdade**, no nível certo da página — não `<p><strong>`. Uma resposta com seis pseudo-títulos em negrito é inavegável.
- **Listas viram `<ul>`/`<ol>`**; tabelas viram `<table>` com cabeçalhos (ver [Tabelas](guide-tables.md)).
- **Blocos de código** ganham rótulo de linguagem em texto, um `<pre><code>` de verdade e um botão de copiar com nome acessível único. Containers com rolagem horizontal seguem a regra de foco condicional (`A11Y.md` §6 — *Armadilhas de Foco que Ninguém Pediu*).
- **Imagens e diagramas que o modelo gera carregam a mesma obrigação de qualquer outra imagem** — ver [Imagens](guide-images.md) e *Image Evidence* (`A11Y.md` §2). Um assistente que emite `alt=""` num gráfico que ele acabou de desenhar está fabricando uma classificação de decorativo.
- **Matemática, gráficos e artefatos embutidos** não são isentos por serem gerados: o que aparece no DOM é responsabilidade do produto, não do modelo.

## 4. Ações por mensagem precisam de nomes distintos

Uma conversa com vinte respostas produz vinte botões "Copiar", vinte "Regenerar", vinte "joinha". Para quem lista os controles com leitor de tela, são indistinguíveis.

```tsx
<button aria-label={`Copiar resposta ${indice + 1}`}>Copiar</button>
```

Mantenha o texto visível curto e ponha a distinção no nome acessível — e lembre que o nome **precisa conter** o texto visível (SC 2.5.3, `A11Y.md` §3): `aria-label="Copiar resposta 3"` num botão escrito "Copiar" está correto; `aria-label="Duplicar"` é falha de Label in Name.

## 5. UI que o modelo monta em tempo de execução

Quando um modelo compõe componentes ao vivo — um formulário gerado, um gráfico renderizado, um dashboard dinâmico —, **nenhuma revisão de código jamais vê aquela saída.** As checagens mecânicas que o pipeline roda no repositório não alcançam marcação que não existia em tempo de build.

- Restrinja a geração a um **conjunto de componentes homologado** em vez de marcação livre: a acessibilidade passa a ser propriedade da biblioteca, verificada uma vez, e não de cada geração.
- **Verifique depois de renderizar, não só antes de publicar:** rode uma passada automática (axe ou equivalente) contra o DOM composto nos ambientes em que isso é possível, e trate o que ela achar como defeito do gerador, não da sessão.
- O que o gerador não consegue garantir — o alt de uma imagem, a legenda de uma mídia, o equivalente em dados de um gráfico — **MUST** ser pedido ao humano no circuito, exatamente como exigem *Image Evidence* e *Media Evidence*. Gerar não cria isenção; remove o revisor, que é o oposto.
- É o mesmo raciocínio da *Independent Verification* (`A11Y.md` §2) aplicado uma camada abaixo: o componente que produziu a marcação não é a testemunha de que ela está conforme.

## 6. Carga cognitiva é a parede mestra aqui

Interface conversacional joga todo o peso da estrutura sobre quem lê. Aplique [Acessibilidade Cognitiva](guide-cognitive.md) por inteiro, e especificamente:

- **Linguagem simples no texto do próprio produto** — rótulos, estados vazios, mensagens de erro. A resposta do modelo é conteúdo; a interface em volta é sua.
- **Nada que precise ser lembrado entre turnos**: se o assistente pede algo que já foi informado, é Entrada Redundante (SC 3.3.7) em roupa conversacional.
- **Erro e recusa são conteúdo, não silêncio.** "Algo deu errado" numa região `role="status"`, com o que fazer em seguida — um stream que simplesmente para não deixa sinal nenhum de que algo aconteceu.
- **Diga o que o assistente é** dentro da interface. Quem não enxerga o enquadramento visual merece a mesma informação que todo mundo recebe do layout.

## Fontes

- **Mecânica das regiões vivas** — o comportamento em que o §0 e o §1 se apoiam (a região precisa existir antes da primeira mensagem; como adições são processadas): [WAI-ARIA — role `log`](https://www.w3.org/TR/wai-aria-1.2/#log) · Sara Soueidan, [*Accessible notifications with ARIA Live Regions*](https://www.sarasoueidan.com/blog/accessible-notifications-with-aria-live-regions-part-1/).
- **Por que streams de token gaguejam ou recomeçam de forma diferente por leitor** — o tratamento de regiões vivas diverge mensuravelmente entre pares leitor/navegador, e é por isso que este guia anuncia transições em vez de transmitir conteúdo: [a11ysupport.io — resultados de teste do `aria-live`](https://a11ysupport.io/tech/aria/aria-live_attribute).
- **UI montada em runtime precisa de verificação no render (§5):** *Accessible GenAI UI Generation with Post-Render Verification*, ICCHP 2026 ([Springer](https://link.springer.com/chapter/10.1007/978-3-032-31285-3_47)) — padrões estáticos não alcançam marcação que só existe em tempo de execução; uma segunda checagem precisa rodar onde a interface é composta.
- **Carga cognitiva em interfaces conversacionais (§6):** Hervás et al., *Cognitive Accessibility in Generative AI Interfaces* — revisão sistemática, International Journal of Human–Computer Interaction, 2026 ([Taylor & Francis](https://www.tandfonline.com/doi/full/10.1080/10447318.2026.2618562)) — as interfaces textuais de IA generativa atuais impõem carga cognitiva excessiva e carecem de previsibilidade e scaffolding.

*Critérios de sucesso cobertos: 4.1.3 Mensagens de Status (AA) · 2.2.2 Pausar, Parar, Ocultar (A) · 2.2.1 Tempo Ajustável (A) · 1.3.1 Informação e Relações (A) · 2.4.3 Ordem de Foco (A) · 2.5.3 Label in Name (AA) · 1.1.1 Conteúdo Não Textual (A)*
