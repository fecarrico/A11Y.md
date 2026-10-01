# Guia de Configuração (A11Y.md)

Este guia explica como configurar adequadamente seu assistente de IA (Cursor, Claude Code, GitHub Copilot, Gemini/Windsurf) para utilizar o padrão de acessibilidade `A11Y.md`.

> [!IMPORTANT]  
> **Regra de Ouro:** O arquivo de configuração do seu ambiente deve conter **APENAS** uma referência apontando para o `A11Y.md`. **NUNCA** copie ou duplique regras de acessibilidade fora do `A11Y.md` — isso previne a fragmentação de regras e garante que a IA sempre carregue o contexto completo.
>
> A referência pode apontar para a **URL deste repositório** ou para uma **cópia local** — as três formas de entrada estão comparadas abaixo. Falantes de inglês podem apontar para `docs/en/A11Y.md`.

## Três formas de o padrão entrar num projeto

| | Como | Quando é a melhor | O que você assume |
| :--- | :--- | :--- | :--- |
| **1. Link para o upstream** | a regra aponta para a URL raw em `main` | zero arquivos copiados, sempre a edição atual | rede na hora da leitura; o padrão pode mudar debaixo de você — fixe uma tag na URL (`/v2.2.0/` no lugar de `/main/`) para congelar |
| **2. Cópia fixada, regra no seu arquivo de agente** | copie `docs/<idioma>/A11Y.md` com `references/` e `templates/` para o repositório (`docs/a11y/` é um bom lugar); a regra no `CLAUDE.md`, `.cursorrules` ou equivalente aponta para o caminho local | trabalho offline, atualização revisada como diff, times que clonam o repositório e precisam herdar as regras | a atualização é sua: uma nota de procedência com commit de origem, versão e licença, e a atualização tratada como qualquer mudança revisada |
| **3. Cópia fixada, regra no `AGENTS.md`** | a mesma cópia, com a regra num `AGENTS.md` neutro de ferramenta, em vez de um `CLAUDE.md` que não é seu | o `CLAUDE.md` pertence a outro fluxo, ou vários agentes leem o repositório | dois arquivos de instrução para manter coerentes: o `CLAUDE.md` diz como o projeto trabalha, o `AGENTS.md` diz a regra de acessibilidade |

Seja qual for a porta: a regra é **uma linha**, e as regras de acessibilidade em si vivem só no `A11Y.md`. Com cópia, o `REPORT.md` registra a *Versão do padrão* a partir da linha *Versão* da própria cópia, e o `tools/verify-a11y.py` pode ficar ao lado dela para o gate rodar offline. *(As três opções como o agente de um time adotante as apresentou ao autor antes de uma revisão, em 29/09/2026 — o autor escolheu a terceira.)*

## Referência Rápida

| Ambiente | Arquivo de Configuração | Localização |
| :--- | :--- | :--- |
| **Cursor** | Arquivo de regra `.mdc` | `.cursor/rules/a11y.mdc` |
| **Claude Code** | Referência em `CLAUDE.md` | `CLAUDE.md` (raiz) |
| **GitHub Copilot** | Arquivo de instruções | `.github/copilot-instructions.md` |
| **Gemini / Antigravity**| Regra em `AGENTS.md` | `AGENTS.md` ou `.agents/AGENTS.md` |
| **Windsurf** | Diretório de regras | `.windsurf/rules/a11y.md` |

---

## 1. Cursor
Crie um arquivo `.mdc` dentro do diretório `.cursor/rules/`.

**Arquivo:** `.cursor/rules/a11y.mdc`
```yaml
---
description: "Contexto persistente de acessibilidade — delega todas as regras para o A11Y.md"
alwaysApply: true
---
Siga estritamente as regras de acessibilidade do arquivo <caminho ou URL do seu A11Y.md — ex.: https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/pt-BR/A11Y.md, ou uma cópia local>.
```
> [!NOTE]  
> `alwaysApply: true` é crucial. Acessibilidade é uma pré-condição estrita para todo código de UI e não deve depender de padrões glob para ser ativada.

## 2. Claude Code
Adicione uma seção ao seu arquivo `CLAUDE.md` raiz.

**Arquivo:** `CLAUDE.md`
```markdown
## Acessibilidade
Siga estritamente as regras de acessibilidade do arquivo <caminho ou URL do seu A11Y.md — ex.: https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/pt-BR/A11Y.md, ou uma cópia local>.
```

## 3. GitHub Copilot
Adicione a instrução ao arquivo de instruções customizadas do Copilot.

**Arquivo:** `.github/copilot-instructions.md`
```markdown
## Acessibilidade
Siga estritamente as regras de acessibilidade do arquivo <caminho ou URL do seu A11Y.md — ex.: https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/pt-BR/A11Y.md, ou uma cópia local>.
```

## 4. Gemini / Antigravity
Adicione a instrução ao arquivo de regras do agente.

**Arquivo:** `AGENTS.md` ou `.agents/AGENTS.md`
```markdown
Siga estritamente as regras de acessibilidade do arquivo <caminho ou URL do seu A11Y.md — ex.: https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/pt-BR/A11Y.md, ou uma cópia local>.
```

## 5. Windsurf
Crie um arquivo de regra no diretório de regras do Windsurf.

**Arquivo:** `.windsurf/rules/a11y.md`
```markdown
Siga estritamente as regras de acessibilidade do arquivo <caminho ou URL do seu A11Y.md — ex.: https://raw.githubusercontent.com/fecarrico/A11Y.md/main/docs/pt-BR/A11Y.md, ou uma cópia local>.
```
