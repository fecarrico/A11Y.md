# Declaração de Acessibilidade (Template)

A declaração pública da acessibilidade de um produto: o que ele promete, o que foi verificado, o que se sabe que está quebrado e quem responde por isso. O GitHub mostra este arquivo como a aba **Accessibility** do repositório quando ele está na raiz, em `.github/` ou em `docs/`. O mesmo texto serve à declaração pública que o EAA, a LBI e as regras de licitação pedem.

> **Regras:**
> 1. **Escrita a partir da evidência, nunca à frente dela.** Toda afirmação aqui vem do `REPORT.md` e do `EXCEPTIONS.md` atuais. O status declarado é o status do relatório. Uma declaração sem relatório por trás é promessa, não declaração, e a IA **MUST NOT** redigi-la.
> 2. **Barreiras conhecidas são as exceções abertas e os itens `[ ]` e `[!]` do relatório**, em linguagem simples, com o contorno. Nada registrado lá fica de fora daqui. Reter uma barreira é decisão de uma pessoa com o próprio jurídico, tomada às claras, nunca omissão do agente.
> 3. **Uma pessoa assina.** O agente redige; um responsável nomeado revisa, publica e responde. Responsável e prazo de primeira resposta são obrigatórios.
> 4. **Revisada por evento:** o relatório muda de status, uma exceção abre ou fecha, uma release sai. Carrega a data da última revisão e a versão do padrão.
> 5. **É registro versionado do projeto** — nunca entra no `.gitignore`.

---

## [Nome do produto] — declaração de acessibilidade

[Um parágrafo: o que é o produto, quais superfícies esta declaração cobre (aplicação web, site de documentação, app mobile, CLI) e onde está a evidência detalhada (link para o `REPORT.md`).]

### A que nos comprometemos
- **Padrão:** WCAG 2.2 no nível [A | AA | AAA], sob o perfil [Launchpad | Standard | Shield] do A11Y.md versão [x.y.z] *(a linha Versão no topo do `A11Y.md` que o projeto segue)*.
- **Referências legais, onde se aplicam:** [EN 301 549 / EAA · Section 508 / ADA · LBI art. 63 / ABNT NBR 17225 (regular | plena) · NBR 17060 para mobile] *(ver Governança §5–§6.1)*.
- **Status declarado:** [✅ PASS | ⚠️ CONDITIONAL | 🚫 FAIL] em [AAAA-MM-DD], verificação [cross-agent | fresh-context | self-reported ⚠️] por [quem], checkpoints humanos por [quem]. *(Copiado do `REPORT.md`; nunca promovido aqui.)*

### Ambientes suportados
[Os pares navegador + tecnologia assistiva que o relatório nomeia no §3: ex. NVDA 2026.1 + Firefox 141 · VoiceOver + Safari 18 · TalkBack + Chrome no Android 15 · só teclado · zoom de 200% e reflow a 320 px. Ambiente não listado não foi testado, o que é diferente de "não suportado".]

### Barreiras conhecidas
[Uma linha por exceção aberta e por item `[ ]`/`[!]` do relatório. Vazio só é resposta válida quando o relatório não tem nenhum item desses.]

| Barreira | Quem afeta | Contorno hoje | Rastreio | Revisar até |
| :--- | :--- | :--- | :--- | :--- |
| [o que a pessoa não consegue fazer, em palavras simples] | [ex. quem usa leitor de tela no checkout] | [a rota alternativa, ou "nenhuma ainda"] | [link da issue] | [AAAA-MM-DD, da expiração da exceção] |

### Como reportar uma barreira
- **Onde:** [um link de issue com template, um e-mail, um formulário que seja ele próprio acessível, um telefone onde a lei pedir].
- **O que incluir:** o que você tentava fazer, a tecnologia assistiva ou o método de entrada, o que aconteceu.
- **O que acontece depois:** primeira resposta em até [n] dias. Barreira confirmada entra no `EXCEPTIONS.md` com responsável e data de revisão até ser corrigida.

### Para quem contribui
[As regras a que uma mudança responde e onde vai a evidência, ex. "As interfaces seguem o A11Y.md no perfil Standard. Uma mudança sai com o `REPORT.md` atualizado, e um desvio aceito com uma entrada no `EXCEPTIONS.md`." Uma linha basta. O padrão é a versão longa.]

### Quem responde por isto
- **Responsável:** [uma pessoa, com um jeito de falar com ela]
- **Última revisão:** [AAAA-MM-DD] contra o A11Y.md [x.y.z]
- **Próxima revisão:** [na próxima release, ou uma data]
