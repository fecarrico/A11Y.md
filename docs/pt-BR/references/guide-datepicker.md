# Guia de Date Picker & Calendário

> **Escopo:** Campos de data, grades de calendário e seletores de intervalo — adote em vez de reinventar (`A11Y.md` §6).

## 0. A regra da qual todas as outras decorrem

**O campo de texto é a funcionalidade. O calendário é um recurso em cima dele.**

Quem já sabe a data digita em um segundo. Obrigar essa pessoa a navegar por uma grade de trinta células é mais lento para todo mundo e hostil para quem usa teclado, controle por voz e leitor de tela — que agora precisa percorrer um mês inteiro com setas para inserir algo que soletraria. Um picker que remove a entrada digitada é a forma mais comum de um campo de data ficar inutilizável.

```tsx
// ❌ O calendário como única porta de entrada
<div className="campo-data" onClick={abrirCalendario}>{valor || "Selecione uma data"}</div>

// ✅ Um input de verdade, com o calendário como companheiro opcional
<label htmlFor="checkin">Data de entrada</label>
<span id="checkin-fmt">Formato: DD/MM/AAAA</span>
<input id="checkin" name="checkin" type="text" inputMode="numeric"
       aria-describedby="checkin-fmt" autoComplete="off" />
<button type="button" aria-label="Escolher data de entrada no calendário"
        aria-expanded={aberto} aria-controls="checkin-cal">📅</button>
```

**Aceite o que as pessoas de fato digitam.** Interprete `01/02/2026`, `1/2/26`, `2026-02-01` e a colagem vinda de outro campo; não rejeite por pontuação. Bloquear colagem num campo de data falha a SC 3.3.8 pelo mesmo motivo que falha numa senha: transforma um "copiar" em teste de memória.

## 1. O formato vem antes do campo, não depois do erro

O formato esperado **MUST** estar visível antes de a digitação começar, fora do campo (`A11Y.md` §6 — *Placeholder Labels*). Formato que só aparece como erro de validação é uma armadilha que a pessoa precisa acionar primeiro. Amarre com `aria-describedby` para o leitor de tela ouvir enquanto o campo está vazio, não só depois da falha. Mesma regra para restrições que importam — "no máximo 30 dias a partir de hoje" fica ao lado do rótulo, não dentro da recusa.

## 2. A grade do calendário

Use o [padrão Date Picker Dialog da APG](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/datepicker-dialog/). O que ele exige, em resumo:

1. **Estrutura:** o mês é uma `role="grid"` (ou uma `<table>` de verdade), linhas são semanas, células são dias. Os cabeçalhos dos dias da semana são cabeçalhos de coluna, não letrinhas decorativas.
2. **Uma parada de tabulação, setas por dentro** — a grade tem uma única célula tabulável (`tabindex="0"` na data focada, `-1` no resto); ← → andam por dia, ↑ ↓ por semana, `Home`/`End` vão às bordas da semana, `PageUp`/`PageDown` mudam de mês, `Shift` + essas mudam de ano.
3. **Toda célula declara a data completa**: `aria-label="15 de março de 2026"` — "15" sozinho não significa nada fora da grade visual. Marque hoje com `aria-current="date"` e o dia escolhido com `aria-selected="true"`.
4. **Abrir move o foco** para dentro da grade, sobre a data selecionada, ou sobre hoje quando não há seleção. **`Esc` fecha e devolve o foco ao gatilho.** Escolher uma data fecha, devolve o foco ao input, e o input carrega o valor como texto.
5. **Datas indisponíveis usam `aria-disabled="true"`, não remoção:** continuam alcançáveis para o leitor distinguir "indisponível" de "não existe", e o motivo entra no rótulo — *"3 de março de 2026, indisponível, estadia mínima de duas noites"*. Nunca sinalize disponibilidade só por cor (SC 1.4.1).

## 3. Anuncie a mudança de mês

Passar do fim do mês com as setas, ou apertar o botão de próximo mês, troca a grade inteira em silêncio — o motivo clássico de as pessoas se perderem num picker gerado. Anuncie o mês novo por região viva, e mantenha a legenda visível (`<h2 id="cal-label">Março de 2026</h2>`) como nome acessível da grade:

```tsx
<div role="status" aria-live="polite" className="sr-only">{rotuloDoMes}</div>
```

## 4. Intervalos

- Dois inputs rotulados (*Data inicial*, *Data final*), nunca um campo em que se espera que a pessoa clique duas vezes.
- Anuncie o estado da seleção: *"Início 12 de março selecionado. Escolha a data final."*
- O intervalo escolhido precisa ser visível sem depender só de um fundo colorido — marque também os extremos com texto ou forma.
- Se a segunda data é limitada pela primeira, diga a limitação em voz alta quando ela mudar; não se limite a esmaecer metade da grade.

## 5. Quando o input nativo é a resposta melhor

O `<input type="date">` entrega o picker da própria plataforma — já operável por teclado, já localizado, já familiar ao leitor de tela da pessoa, e de graça no mobile. É o padrão certo sempre que você não precisa de seleção de intervalo, datas desabilitadas customizadas ou identidade visual específica. Os motivos para *não* usá-lo (estilização inconsistente, sem suporte a intervalo, formato preso ao locale) são decisões de produto — registre em `A11Y-DECISIONS.md` em vez de redecidir a cada tela. Em plataforma nativa, use o picker do sistema: ver [Tradução para Plataformas Nativas](guide-platform-native.md).

*Critérios de sucesso cobertos: 1.3.1 Informação e Relações (A) · 2.1.1 Teclado (A) · 2.1.2 Sem Armadilha de Teclado (A) · 3.3.2 Rótulos ou Instruções (A) · 3.3.8 Autenticação Acessível (AA) · 1.4.1 Uso de Cor (A) · 4.1.2 Nome, Função, Valor (A)*
