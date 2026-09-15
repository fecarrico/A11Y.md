# Errata no OSF — o que fazer no registro pg6r5

## O que é possível e o que não é

O registro é congelado de propósito — é isso que dá valor ao carimbo de tempo.
O OSF resolve isso com **Update** (não "Edit", não um registro novo):

- **Update** é um pedido de revisão do registro publicado. Você edita só os
  campos que precisam mudar e escreve uma **justificativa obrigatória**.
- A atualização aprovada passa a ser o que o leitor vê por padrão, com uma
  **caixa laranja no topo** mostrando a data e o motivo. É exatamente o efeito
  que uma errata precisa ter.
- O registro original continua acessível pelo histórico de versões. Nada é
  apagado.
- **Arquivos não podem ser adicionados nem removidos numa atualização.** A
  errata em si não vai para dentro do OSF: ela mora no pacote do Zenodo e no
  repositório, e o registro aponta para lá.
- Depois de submeter, há uma janela de **48 horas** para os administradores do
  registro aprovarem ou rejeitarem. Sendo você o único admin, aprova você mesmo
  (ou espera a aprovação automática).

## Passo 1 — abrir o registro logado

    https://osf.io/pg6r5

## Passo 2 — botão "Update" / "Request update"

Fica no topo do registro, na barra de ações, visível para quem é admin.
Ele abre o formulário do registro com os campos editáveis.

## Passo 3 — justificativa

Campo obrigatório, é o texto que aparece na caixa laranja:

    Two instruments that this registration defines were never run: the
    deterministic per-task checklist (co-primary violation outcome nº 2) and
    the registered second engine. Both have now been run over the same 400
    pages and published. This update also records a limitation the
    registration never stated: no detectable-effect-size calculation was made,
    and the design detects a 24% reduction in roughly one attempt in nine.
    No published result is retracted or revised.

## Passo 4 — onde escrever no corpo do registro

**Não reescrever nada do protocolo.** O que ele previa continua sendo o que ele
previa; o que falhou foi a execução, e é isso que se declara.

Procurar o campo mais adequado entre os que o formulário mostrar — tipicamente
o de **análise**, o de **outras informações** ou o campo livre no fim — e
**acrescentar ao final**, sem apagar o que está lá:

    ERRATUM (2026-09-15). The violation outcome above is defined by two
    instruments, and a second engine is registered as a robustness check. Only
    axe-core was run for the published results. Both missing instruments have
    since been run over the same 400 pages, without modification, and are
    published in dataset v4: https://doi.org/10.5281/zenodo.22772831

    The deterministic checklist agrees with the published result and
    strengthens it (pass rate 67.0% bare to 92.1% with the standard). The
    second engine disagrees on the raw count and the disagreement is reported
    rather than resolved, as this registration requires.

    This registration also justified its sample size by collection
    feasibility and never by detectable effect size. A post-hoc power analysis
    is now published with the dataset: the design detects a real 24% reduction
    in roughly one attempt in nine, which reframes the null reported on the
    D-B contrast — the contrast this registration calls decisive. That null is
    not evidence against the standard; it is evidence that the study could not
    answer the question it called decisive.

    Full text: ERRATA-study1.md, inside the dataset package and at
    https://github.com/fecarrico/A11Y.md

## Passo 5 — submeter e aprovar

Submeter a atualização e, na janela de 48 horas, aprová-la como admin.

## Passo 6 — conferir

Abrir https://osf.io/pg6r5 numa janela anônima e ver se a caixa laranja aparece
com a justificativa do passo 3, e se o texto do passo 4 está no corpo.

---

**Antes de escrever qualquer coisa nos campos, me manda uma captura da tela do
formulário.** No Zenodo eu te dei instruções para uma tela que não era a que
você estava vendo, e isso custou tempo. Aqui eu prefiro olhar os campos reais.
