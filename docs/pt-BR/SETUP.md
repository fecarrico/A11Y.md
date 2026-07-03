# Guia de Configuração (A11Y.md)

Este guia explica como configurar adequadamente seu assistente de IA (Cursor, Claude Code, GitHub Copilot, Gemini/Windsurf) para utilizar o padrão de acessibilidade `A11Y.md`.

> [!IMPORTANT]  
> **Regra de Ouro:** O arquivo de configuração do seu ambiente deve conter **APENAS** uma referência apontando para o `A11Y.md`. **NUNCA** copie ou duplique regras de acessibilidade fora do `A11Y.md` — isso previne a fragmentação de regras e garante que a IA sempre carregue o contexto completo.

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
Siga estritamente as regras de acessibilidade definidas no arquivo <aqui vai o caminho para o arquivo A11Y.md na sua máquina ou repositório>.
```
> [!NOTE]  
> `alwaysApply: true` é crucial. Acessibilidade é uma pré-condição estrita para todo código de UI e não deve depender de padrões glob para ser ativada.

## 2. Claude Code
Adicione uma seção ao seu arquivo `CLAUDE.md` raiz.

**Arquivo:** `CLAUDE.md`
```markdown
## Acessibilidade
Siga estritamente as regras de acessibilidade definidas no arquivo <aqui vai o caminho para o arquivo A11Y.md na sua máquina ou repositório>.
```

## 3. GitHub Copilot
Adicione a instrução ao arquivo de instruções customizadas do Copilot.

**Arquivo:** `.github/copilot-instructions.md`
```markdown
## Acessibilidade
Siga estritamente as regras de acessibilidade definidas no arquivo <aqui vai o caminho para o arquivo A11Y.md na sua máquina ou repositório>.
```

## 4. Gemini / Antigravity
Adicione a instrução ao arquivo de regras do agente.

**Arquivo:** `AGENTS.md` ou `.agents/AGENTS.md`
```markdown
Siga estritamente as regras de acessibilidade definidas no arquivo <aqui vai o caminho para o arquivo A11Y.md na sua máquina ou repositório>.
```

## 5. Windsurf
Crie um arquivo de regra no diretório de regras do Windsurf.

**Arquivo:** `.windsurf/rules/a11y.md`
```markdown
Siga estritamente as regras de acessibilidade definidas no arquivo <aqui vai o caminho para o arquivo A11Y.md na sua máquina ou repositório>.
```
