# Registro de Decisões A11Y (Memória de Padrões)

> **Propósito:** memória entre turnos das escolhas entre **alternativas igualmente conformes**. Duas implementações podem passar no `A11Y.md` e no axe e ainda divergir (`role` diferente, padrão de foco diferente, texto de anúncio diferente) — vinte modais conformes, zero coerência. Este arquivo evita isso.

## Regras para a IA

1. **Registre apenas o que não é derivável** das regras do `A11Y.md` nem do próprio código. Landmarks, headings e presença de alt são verificáveis por máquina — **NÃO** pertencem a este arquivo.
2. **Indexe por padrão, nunca por tela.** ✅ *"Modal de confirmação destrutiva → `alertdialog`"* · ❌ *"O modal de contestação faz X"*.
3. **Uma linha por decisão:** padrão → escolha → porquê curto.
4. **Leia antes de construir:** antes de gerar qualquer componente interativo, consulte este registro e reutilize o padrão registrado (ver *Component Reuse* no AI Behavior Contract).
5. **Nunca bifurque em silêncio:** se um requisito novo contradiz uma decisão registrada, pergunte ao usuário — não crie uma variante paralela.
6. **Mantenha enxuto:** dezenas de linhas, não centenas. Este arquivo divide o orçamento de contexto com o Lazy Loading; se passar de ~40 entradas, consolide.

## Decisões

<!-- Adicione entradas abaixo. Formato: - **Padrão** → escolha — porquê. (data) -->

- **Modal de confirmação destrutiva** → `role="alertdialog"`, foco inicial no botão não-destrutivo, foco retorna ao acionador — semântica de interrupção conforme APG. *(exemplo — substitua pela primeira decisão real do seu projeto)*
