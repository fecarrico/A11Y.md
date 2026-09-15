# Nova versão no Zenodo — passo a passo

**Não é um "New upload"** — isso criaria um registro novo, com DOI novo e sem
relação nenhuma com o que já está no ar.
**Também não é "Edit"** — esse botão só muda metadados (título, descrição,
autores) e não deixa trocar arquivo de um registro publicado.
**É "New version"**: cria uma versão nova do mesmo registro, com DOI próprio,
ligada ao anterior. É o único caminho que troca arquivos sem quebrar citação.

**Atenção ao número da versão.** O registro já está na **v3** (publicada em
25/08, DOI 10.5281/zenodo.22088369). As versões 2 e 3 atualizaram os arquivos do
Estudo 2; o pacote do Estudo 1 não mudou desde agosto. Então:

- o **registro** vai de v3 para **v4**;
- o **arquivo do Estudo 1** vai de `dataset-v1.zip` para `dataset-v2.zip`.

Os dois números são diferentes de propósito, e é o mesmo padrão que já está lá:
o registro v3 carrega um `a11ymd-study2-dataset-v3.zip`.

O que acontece com os DOIs:

- Cada versão publicada mantém o DOI dela para sempre. A v3
  (`10.5281/zenodo.22088369`) continua resolvendo para a v3.
- O concept DOI `10.5281/zenodo.22073025` passa a resolver para a v4.
- A v4 ganha um DOI próprio, gerado na hora de publicar.

---

## Passo 1 — achar o registro certo na sua lista

Na tela "My uploads" há duas entradas. **Não é a de cima.**

- `A11Y.md Efficacy Benchmark — Study 3: The v2.0.0 Audit` · 6 de setembro (v1)
  → **não é esta**
- `A11Y.md Benchmark — Studies 1 & 2: full dataset` · 25 de agosto (v3)
  → **é esta**

Clicar em **View**, na linha dela.

## Passo 2 — botão verde "New version"

Fica no painel da direita, na página do registro. Ele cria um rascunho e já
abre o formulário, marcado como *New version draft*.

## Passo 3 — trazer os arquivos da v1

**O rascunho começa sem arquivo nenhum.** Na seção de arquivos há um botão
**"Import files"** — ele traz os 6 arquivos da v1 sem duplicar armazenamento.
Clicar nele antes de qualquer outra coisa.

Depois de importar, devem aparecer estes seis (é o conteúdo da v3):

    a11ymd-benchmark-screenshots-v1.zip      77.93 MB
    a11ymd-benchmark-dataset-v1.zip           3.97 MB   ← o único que sai
    a11ymd-study2-screenshots-v2.zip         72.12 MB
    a11ymd-study2-dataset-v3.zip              1.61 MB
    MANIFEST.json                             0.17 MB
    MANIFEST-study2-v3.json                   0.14 MB

Se a lista vier diferente disso, parar e me avisar: significa que alguma coisa
mudou no registro depois de 25/08 e o pacote precisa ser remontado sobre ela.

## Passo 4 — remover só um arquivo

Remover **`a11ymd-benchmark-dataset-v1.zip`** (ícone de lixeira na linha dele).

Por quê: o v2 contém as 885 entradas do v1 byte a byte, verificadas por SHA-256
na montagem, e a v1 continua baixável no DOI dela. Manter os dois lado a lado
só criaria dúvida sobre qual é o pacote bom.

**Não mexer nos outros cinco.** O `MANIFEST.json` fica porque descreve o pacote
do Estudo 1 na versão v1 e continua correto para ele. Os arquivos do Estudo 2
não têm nada a ver com esta errata.

## Passo 5 — subir os dois arquivos novos

    /var/home/fecarrico/Documentos/lab/a11y/benchmark/runs/dataset/a11ymd-benchmark-dataset-v2.zip
    /var/home/fecarrico/Documentos/lab/a11y/benchmark/runs/dataset/MANIFEST-v2.json

Depois do upload o Zenodo mostra o md5 de cada um. Conferir contra estes:

    2aa577ae0095b7d257285289ff8ddd30   a11ymd-benchmark-dataset-v2.zip
    3243ea6e78682a02cf898d5681859f8b   MANIFEST-v2.json

Se algum não bater, parar e me avisar antes de publicar.

## Passo 6 — campo "Version"

Trocar de `v3` para:

    v4

## Passo 7 — descrição e notas

O registro já separa as duas coisas, e vale manter: a **Description** diz o que o
dataset é, e o **Additional notes** carrega o histórico de versões. A errata
inteira não vai em nenhum dos dois — ela viaja dentro do pacote, como
`ERRATA-study1.md`.

### 7a. Description — uma edição de uma linha

Na frase do Estudo 1, onde hoje se lê:

    ...every generated page, axe-core 4.13.0 report, full-page screenshot,
    collection log with per-call model versions...

passar a ler:

    ...every generated page, axe-core 4.13.0 report, deterministic per-task
    checklist and second-engine (HTML_CodeSniffer) results, full-page
    screenshot, collection log with per-call model versions...

Só isso. O resto da descrição continua correto e não se mexe.

### 7b. Additional notes — acrescentar uma entrada

No mesmo formato da que já está lá (`v2 (2026-08-24): ...`), **acima** dela:

    v4 (2026-09-15): erratum for Study 1. The two instruments the protocol
    registers and that had never been run — the deterministic per-task checklist
    (co-primary outcome nº 2) and the second engine (HTML_CodeSniffer) — are now
    run over the same 400 pages and included. Adds a post-hoc power analysis the
    protocol never specified: this design detects a 24% reduction in roughly one
    attempt in nine, which reframes the published null on the contrast the
    protocol calls decisive. No published result is retracted or revised. Study 1
    dataset goes v1 to v2, carrying all 885 entries byte for byte, SHA-256
    verified at build. Full text in ERRATA-study1.md. Study 2 files unchanged.

## Passo 8 — conferir o que não deve mudar

Antes de publicar, olhar se continuam lá:

- Licença **CC BY 4.0**
- Os três *related identifiers*, todos como **isSupplementTo**:
  `https://osf.io/pg6r5`, `https://osf.io/mqs7x`, `https://github.com/fecarrico/A11Y.md`
- Autoria e título — o título continua o mesmo, o "v2" vai no campo Version

## Passo 9 — publicar

**Publicar é irreversível.** Não existe despublicar no Zenodo: a partir daí a
versão existe para sempre e só os metadados podem ser editados depois. Os
arquivos, não.

Antes de clicar, valem duas conferências de 30 segundos: os md5 do passo 5, e
se o `a11ymd-benchmark-dataset-v2.zip` está lá e o `-v1.zip` não está.

## Passo 10 — auditar por API

Como nas três publicações anteriores. Trocar `<novo-id>` pelo número que aparece
na URL da versão nova:

    curl -s "https://zenodo.org/api/records/<novo-id>" | python3 -c "
    import json,sys
    d=json.load(sys.stdin)
    print('versão:', d['metadata'].get('version'), '· doi:', d['doi'])
    for f in d['files']:
        print(' ', f['checksum'].replace('md5:',''), f['key'])"

## Passo 11 — me mandar o DOI novo

Três lugares passam a apontar para a versão velha se ninguém mexer: o
`DEVIATIONS.md`, o manifesto espelhado no repositório e as referências do
relatório. Eu atualizo os três quando você me passar o DOI.
