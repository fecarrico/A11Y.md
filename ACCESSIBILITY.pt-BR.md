# Declaração de acessibilidade

🇺🇸 Read in English: [ACCESSIBILITY.md](./ACCESSIBILITY.md)

O A11Y.md é um conjunto de documentos Markdown: um padrão que agentes de IA leem antes de gerar uma interface, os guias e templates para os quais ele aponta, e dois scripts pequenos. Não existe aplicativo aqui. Esta declaração cobre o que uma pessoa que usa tecnologia assistiva vai encontrar ao ler, rodar ou contribuir com esses documentos, e onde a única interface do projeto, o site, guarda a própria evidência.

## O que você encontra aqui, e em que forma

- **Markdown puro, em duas edições.** Tudo em `docs/` existe em inglês e em português, mantidos em paridade pelo `tools/lint-standard.py`: mesmos arquivos, mesmos títulos, mesmo número de regras. O leitor de tela recebe a mesma estrutura em qualquer das duas línguas.
- **Estrutura navegável.** Os níveis de título não pulam em nenhum arquivo de `docs/` nem nos documentos da raiz. O texto do link diz aonde ele leva. Os exemplos de código ficam sob títulos que dizem "Good Examples" e "Bad Examples", em palavras.
- **Nada carregado só por cor ou símbolo.** Os níveis de severidade juntam o ponto colorido à palavra (🔴 CRITICAL). Os perfis de conformidade juntam o ícone ao nome.
- **Imagens.** A única imagem é o banner do README, com texto alternativo. Os badges abaixo dele são imagens com texto alternativo.
- **Os scripts** imprimem texto puro, sem cor, e a última linha diz PASS ou FAIL por extenso.
- **Leitura por agente.** O padrão foi feito para ser dado a um agente de IA, e o agente lê o mesmo Markdown que uma pessoa. A linha única que faz isso está no [README](README.pt-BR.md#-quick-start-menos-de-2-minutos).
- **A página em volta deste texto é do GitHub.** Sobre a acessibilidade do GitHub em si, vale a declaração deles, em [accessibility.github.com](https://accessibility.github.com/).

A pasta `benchmark/` é material de pesquisa. As páginas que os estudos geraram estão publicadas como dataset com DOI próprio, e muitas delas são inacessíveis de propósito, porque é isso que os estudos medem. Nada ali é exemplo a seguir.

## O site

A única interface do projeto é [fecarrico.github.io/a11ymd](https://fecarrico.github.io/a11ymd/). Ele vive em [repositório próprio](https://github.com/fecarrico/a11ymd) e é construído sob o perfil Shield (AAA) deste padrão, com os três artefatos que o padrão exige mantidos em público: o [relatório de verificação](https://github.com/fecarrico/a11ymd/blob/main/REPORT.md), o [log de exceções](https://github.com/fecarrico/a11ymd/blob/main/EXCEPTIONS.md) e o [registro de decisões](https://github.com/fecarrico/a11ymd/blob/main/A11Y-DECISIONS.md). O status de hoje é ⚠️ **CONDITIONAL**: o axe-core 4.13.0 com o conjunto de regras AAA passa nas oito rotas, a 1280 px e a 320 px, a passada de teclado e a de zoom a 200% estão feitas, o gate estático do padrão diz PASS, e a passada com leitor de tela ainda não foi feita por uma pessoa.

## Barreiras conhecidas

Nada fica de fora desta lista. Os itens do site também estão abertos no relatório ou no log de exceções dele.

Neste repositório:

1. **Os títulos dos READMEs começam com emoji.** O leitor de tela anuncia o símbolo antes do texto do título. A estrutura por baixo está correta. Eles ficam pela leitura visual rápida, e não temos certeza de que é a escolha certa. Se isso custa para você, diga.
2. **Os scripts marcam o nível de cada achado com um símbolo.** Linha de erro começa com `✗` e aviso com `!`. As palavras aparecem só no resumo do fim.

No site:

1. **Ninguém fez a passada com leitor de tela.** O padrão proíbe que um agente alegue um teste de leitor de tela que ele não pôde ouvir, então o status fica CONDITIONAL até alguém rodar o roteiro do [REPORT §3](https://github.com/fecarrico/a11ymd/blob/main/REPORT.md#3-comportamento-e-retorno-de-tarefa). Se você usa NVDA, JAWS, VoiceOver ou TalkBack e tem vinte minutos, essa é a contribuição mais útil que este projeto pode receber. Seu nome entra no relatório.
2. **Nenhum simulador de deficiência de visão de cores rodou.** As razões de contraste são medidas e recalculadas pelo gate. A perda funcional por cor, não.
3. **Três decisões esperam o autor:** o texto alinhado à direita na linha do tempo, o espaçamento entre parágrafos na home (duas flexibilizações de Regra da Casa frente à NBR 17225 5.12.5 e 5.12.3) e se os logos da linha do tempo são decorativos. Até a terceira ser confirmada, esses logos carregam alt vazio.

## Como reportar uma barreira

Abra uma [issue](https://github.com/fecarrico/A11Y.md/issues/new) neste repositório. Não precisa de template. Diga o que você tentava fazer, qual tecnologia assistiva ou método de entrada usava e o que aconteceu. Barreira no site também pode ser reportada aqui, e nós mesmos a levamos para o repositório do site.

Se issue não é o meio certo para você, abra um tópico em [Discussions](https://github.com/fecarrico/A11Y.md/discussions).

A primeira resposta chega em até **7 dias**, o mesmo prazo da [política de segurança](SECURITY.md). Barreira confirmada vira entrada no log de exceções, com responsável e data de revisão, até ser corrigida. A correção é creditada no [CHANGELOG](CHANGELOG.md).

## Se você contribui

O Markdown daqui responde à forma descrita na primeira seção: níveis de título sem pulo, texto de link que diz aonde leva, imagem com texto alternativo ou marcada como decorativa, e nenhum significado carregado só por cor ou só por emoji. Issues e pull requests usam os formulários do próprio GitHub. Uma interface construída para o projeto, hoje o site, segue o [A11Y.md](https://github.com/fecarrico/A11Y.md) versão 2.3.0 no perfil Shield, nasce sob a própria frase de invocação do padrão, e sai com os mesmos três artefatos esperados de qualquer adotante. O resto está no [guia de contribuição](CONTRIBUTING.md).

## Quem responde por isto

Felipe Carriço mantém este repositório e esta declaração. Ela é revisada sempre que o relatório do site muda de status, uma exceção abre ou fecha, ou uma release sai. Última revisão em 2026-10-08, contra a versão 2.3.0 do padrão.

Lendo isto com um agente de IA? As regras que ele deve seguir estão em `docs/pt-BR/A11Y.md`, e a linha única para a configuração dele está no [README](README.pt-BR.md#-quick-start-menos-de-2-minutos).
