# Declaração de acessibilidade

🇺🇸 Read in English: [ACCESSIBILITY.md](./ACCESSIBILITY.md)

O A11Y.md é um padrão que agentes de IA leem antes de gerar uma interface. Este arquivo é a declaração que o padrão pede a todo adotante sobre o próprio produto, escrita aqui sobre as superfícies deste projeto: os documentos deste repositório, o site, a Wiki e os scripts em `tools/`. As regras estão em [`docs/pt-BR/A11Y.md`](docs/pt-BR/A11Y.md).

Você lê isto pelo GitHub. A acessibilidade dessa interface é [declaração do próprio GitHub](https://accessibility.github.com/). O que segue é o que este projeto controla.

## A que este projeto se compromete

- **Perfil:** Shield (AAA), o mais rígido dos três [perfis de conformidade](docs/pt-BR/references/guide-compliance-profiles.md) do padrão, para toda interface produzida a partir deste repositório.
- **Versão do padrão:** 2.3.0.
- **A mesma evidência que pedimos aos adotantes.** O site mantém em público os três artefatos que o padrão exige: um [relatório de verificação](https://github.com/fecarrico/a11ymd/blob/main/REPORT.md), um [log de exceções](https://github.com/fecarrico/a11ymd/blob/main/EXCEPTIONS.md) e um [registro de decisões](https://github.com/fecarrico/a11ymd/blob/main/A11Y-DECISIONS.md). O status da tabela é lido deles, não de memória.

## Onde as coisas estão

| Superfície | O que foi verificado | Status |
| :--- | :--- | :--- |
| [Site](https://fecarrico.github.io/a11ymd/) | axe-core 4.13.0 com o conjunto de regras AAA nas oito rotas, a 1280 px e a 320 px. Passada de teclado com estilos computados sobre o menu, o disclosure e o lightbox. Zoom de 200% e espaçamento de texto. O gate estático do padrão: PASS. | ⚠️ CONDITIONAL. A passada com leitor de tela ainda não foi feita por uma pessoa. |
| O padrão e os guias (`docs/`) | Markdown puro em duas edições mantidas em paridade pelo `tools/lint-standard.py`: mesmos arquivos, mesmos títulos, mesma contagem de regras. Os níveis de título não pulam em nenhum arquivo de `docs/` nem nos documentos da raiz, nenhum link diz "clique aqui" e as imagens do README têm texto alternativo. | Mantido. Sem auditoria de terceiro. |
| Scripts em `tools/` | A saída é texto puro, sem cor. A última linha diz PASS ou FAIL por extenso e dá as contagens. | Mantido. O nível de cada achado vem por um marcador, não por palavra (ver barreiras conhecidas). |
| [Wiki](https://github.com/fecarrico/A11Y.md/wiki) | Markdown com as mesmas convenções de `docs/`. | Sem auditoria. |

A pasta `benchmark/` é material de pesquisa. As páginas que os estudos geraram estão publicadas como dataset com DOI próprio, e muitas delas são inacessíveis de propósito, porque é isso que os estudos medem. Nada ali é exemplo a seguir.

## Barreiras conhecidas

Tudo aqui também é item aberto no relatório ou no log de exceções do site. Nada fica de fora desta lista.

1. **O site ainda não foi testado com leitor de tela por uma pessoa.** Todo checkpoint automatizado e de teclado passa. O padrão proíbe que um agente alegue um teste de leitor de tela que ele não pôde ouvir, então o status fica CONDITIONAL até alguém rodar o roteiro do [REPORT §3](https://github.com/fecarrico/a11ymd/blob/main/REPORT.md#3-comportamento-e-retorno-de-tarefa). Se você usa NVDA, JAWS, VoiceOver ou TalkBack e tem vinte minutos, essa é a contribuição mais útil que este projeto pode receber. Seu nome entra no relatório.
2. **Nenhum simulador de deficiência de visão de cores rodou no site.** As razões de contraste são medidas e recalculadas pelo gate. A perda funcional por cor, não.
3. **Três decisões do site esperam o autor:** o texto alinhado à direita na linha do tempo, o espaçamento entre parágrafos na home (duas flexibilizações de Regra da Casa frente à NBR 17225 5.12.5 e 5.12.3) e se os logos da linha do tempo são decorativos. Até a terceira ser confirmada, esses logos carregam alt vazio.
4. **Os títulos dos READMEs começam com emoji.** O leitor de tela anuncia o símbolo antes do texto do título. A estrutura por baixo está correta. Eles ficam pela leitura visual rápida, e não temos certeza de que é a escolha certa. Se isso custa para você, diga.
5. **Os scripts marcam o nível de cada achado com um símbolo.** Linha de erro começa com `✗` e aviso com `!`. As palavras aparecem só no resumo do fim.

## Como reportar uma barreira

Abra uma [issue](https://github.com/fecarrico/A11Y.md/issues/new) neste repositório. Não precisa de template. Diga o que você tentava fazer, qual tecnologia assistiva ou método de entrada usava e o que aconteceu. Barreira no site também pode ser reportada aqui, e nós mesmos a levamos para o repositório do site.

Se issue não é o meio certo para você, abra um tópico em [Discussions](https://github.com/fecarrico/A11Y.md/discussions).

A primeira resposta chega em até **7 dias**, o mesmo prazo da [política de segurança](SECURITY.md). Barreira confirmada vira entrada no log de exceções, com responsável e data de revisão, até ser corrigida. A correção é creditada no [CHANGELOG](CHANGELOG.md).

## Se você contribui

Interface construída para este projeto nasce sob a própria frase de invocação do padrão e o perfil Shield, e sai com os mesmos três artefatos esperados de qualquer adotante. Para Markdown, a régua é a que foi medida na tabela: níveis de título sem pulo, texto de link que diz aonde leva, imagem com texto alternativo ou marcada como decorativa, e nenhum significado carregado só por cor ou só por emoji. O resto está no [guia de contribuição](CONTRIBUTING.md).

## Quem responde por isto

Felipe Carriço mantém este repositório e esta declaração. Ela é revisada sempre que o relatório do site muda de status, uma exceção abre ou fecha, ou uma release sai. Última revisão em 2026-10-08, contra a versão 2.3.0 do padrão.

Lendo isto com um agente de IA? As regras que ele deve seguir estão em `docs/pt-BR/A11Y.md`, e a linha única para a configuração dele está no [README](README.pt-BR.md#-quick-start-menos-de-2-minutos).
