# Guia de Consent & Cookie Banners

> **Escopo:** Avisos de consentimento, banners de cookies e sobreposições de privacidade — o primeiro elemento que o usuário encontra, e o mais gerado automaticamente sem revisão.

## 1. Decida primeiro: ele bloqueia ou não?

Esta é a bifurcação que define todo o resto. Implementar o padrão errado é a falha mais comum.

| Se o banner… | Então ele é… | E deve |
| :--- | :--- | :--- |
| impede interagir com a página até haver resposta | **diálogo modal** | mover o foco para dentro, contê-lo (SC 2.1.2), fechar com `Esc`, devolver o foco ao ponto de origem — ver [Modals](guide-modals.md) |
| deixa a página utilizável, ocupando uma faixa | **região não-modal** | **NÃO** capturar o foco; ser alcançável na ordem natural de tabulação; anunciar-se por `role="region"` com nome acessível |

O erro clássico é o híbrido: uma faixa que não prende o foco mas escurece a página e ignora cliques — visualmente modal, semanticamente inexistente. Quem usa leitor de tela navega uma página que "parece" disponível e não responde.

## 2. O banner MUST NOT cobrir o indicador de foco (SC 2.4.11)

Uma faixa fixa no rodapé — o formato mais comum de banner de cookie — cobre o elemento focado quando o usuário tabula até o fim da página. **Isso é falha de Nível AA**, e é invisível para quem testa com mouse.

- Reserve espaço no layout (`padding-bottom` no `<body>` equivalente à altura do banner) em vez de apenas sobrepor.
- Verifique tabulando a página inteira com o banner aberto: nenhum elemento focado pode ficar totalmente encoberto.

## 3. Paridade entre aceitar e recusar

**Regra da Casa†:** se "Aceitar tudo" é um botão de um clique, "Recusar tudo" **MUST** ser um botão de um clique, no mesmo nível de navegação e com o mesmo peso visual.

Recusa escondida atrás de "Gerenciar preferências" → lista de 40 fornecedores → "Salvar" é uma barreira de esforço que atinge desproporcionalmente pessoas com limitação motora e com fadiga cognitiva. A WCAG não nomeia isso; o EAA e o RGPD nomeiam, e o Principle Zero deste padrão já responde: se completar a tarefa exige percorrer um labirinto, a tarefa está quebrada.

## 4. Regras técnicas

1. **Botões nativos.** `<button>` para as ações, nunca `<div onClick>`. Vale também para o "X" de fechar.
2. **Sem armadilha de teclado (SC 2.1.2):** o usuário sempre consegue sair do banner pelo teclado — para a página, se for não-modal; pelo `Esc` ou por uma ação, se for modal.
3. **Sem limite de tempo.** Banner que se fecha sozinho, ou que assume consentimento após N segundos, falha a SC 2.2.1 e a base legal junto.
4. **Anúncio na aparição tardia:** se o banner entra no DOM depois do carregamento, ele **MUST** ser anunciado (`role="dialog"` com foco movido, ou `role="status"` se for não-modal e não urgente).
5. **Alvo e contraste:** os botões seguem o perfil ativo como qualquer outro controle — o banner não é exceção de densidade.
6. **Linguagem:** o texto do banner é o caso mais denso de jargão jurídico da interface inteira. Aplique a Seção 6 do [guia Cognitivo](guide-cognitive.md): frase curta, voz ativa, o rótulo diz o resultado.

## 5. Scripts de terceiros

A maior parte dos banners vem de uma plataforma de consentimento (CMP). **A obrigação não é transferida junto com o script.**

- Verifique o banner do fornecedor com teclado e leitor de tela **antes** de instalá-lo, não depois.
- Se o CMP é inacessível e não pode ser trocado no ciclo atual, isso é uma entrada no `EXCEPTIONS.md` — com dono do risco, issue e expiração —, não um problema de outra pessoa.
- Muitos CMPs expõem opções de acessibilidade desligadas por padrão (foco inicial, rótulos, contraste). Elas fazem parte da configuração, não do backlog.

## Critérios de sucesso mapeados

| SC | Nível | O que exige aqui |
| :--- | :--- | :--- |
| 2.1.2 Sem Armadilha de Teclado | A | sempre há saída pelo teclado, modal ou não |
| 2.4.11 Foco Não Obscurecido (Mínimo) | AA | a faixa fixa não pode encobrir o elemento focado |
| 2.2.1 Tempo Ajustável | A | sem autofechamento e sem consentimento por decurso de prazo |
| 4.1.3 Mensagens de Status | AA | aparição tardia anunciada |
| 2.5.8 Tamanho do Alvo | AA | botões do banner seguem o piso do perfil ativo |
