# Accessibility: Acessibilidade Cognitiva, Linguagem & Necessidades Conflitantes

> Escopo: memória, atenção, linguagem, tempo e carga de decisão — os critérios que a WCAG 2.2 acrescentou para cognição, o espaçamento de texto, e o protocolo para quando duas necessidades de acessibilidade se contradizem.

## 1. SC 3.3.8 Autenticação Acessível (AA) — o mais violado por código gerado

O critério proíbe exigir um **teste de função cognitiva** em qualquer etapa da autenticação — lembrar uma senha, transcrever caracteres, resolver um quebra-cabeça, fazer um cálculo — a menos que exista alternativa, mecanismo de assistência, reconhecimento de objeto ou conteúdo pessoal fornecido pelo próprio usuário.

Na prática de implementação, quase sempre falha por uma destas quatro linhas:

### ❌ Incorreto

```html
<!-- 1. Bloquear colar impede o gerenciador de senhas: o "teste de memória" volta -->
<input type="password" onpaste="return false" oncopy="return false">

<!-- 2. Sem autocomplete, o preenchimento automático não sabe o que preencher -->
<input type="password" name="pwd">

<!-- 3. Pedaço de senha por posição é teste de memória puro -->
<label>Digite o 3º e o 7º caractere da sua senha</label>

<!-- 4. CAPTCHA de transcrição sem alternativa -->
<img src="captcha.png"><input name="captcha" placeholder="Digite os caracteres">
```

### ✅ Correto

```html
<input type="email" name="username" autocomplete="username">
<input type="password" name="password" autocomplete="current-password">
<!-- colar permitido, gerenciador de senhas funciona, campo identificado -->
```

- **Nunca bloqueie colar em campo de senha.** É a mitigação mais barata do critério e a regressão mais comum: quem depende de gerenciador de senhas passa a ter que memorizar.
- **`autocomplete` correto** (`username`, `current-password`, `new-password`, `one-time-code`) é o que permite ao navegador e ao gerenciador atuarem como o "mecanismo de assistência" que o critério aceita.
- **CAPTCHA:** se for inevitável, ofereça pelo menos duas modalidades (ex.: visual + áudio) ou prefira desafios de *reconhecimento de objeto*, explicitamente permitidos pelo critério. Transcrição de texto distorcido não passa.
- No perfil **Shield**, a SC 3.3.9 (AAA) remove também as exceções de reconhecimento de objeto e conteúdo pessoal.

## 2. SC 3.3.7 Entrada Redundante (A)

Informação que o usuário já forneceu **no mesmo processo** MUST ser preenchida automaticamente ou oferecida para seleção — não pedida de novo.

- Falha clássica: checkout que pede o endereço na etapa 2 e de novo na etapa 4; formulário multi-etapa que perde tudo ao voltar; cadastro que pede o e-mail e depois "confirme seus dados" digitando tudo outra vez.
- **Exceções do próprio critério:** reinserir é essencial (confirmação de senha), é requisito de segurança, ou a informação anterior deixou de ser válida.
- Em código: o estado do formulário sobrevive à navegação entre etapas e ao botão Voltar. Se você está gerando um wizard, o estado é parte do requisito de acessibilidade, não um refinamento de UX.

## 3. SC 3.2.6 Ajuda Consistente (A)

Se um mecanismo de ajuda — contato humano, telefone, chat, formulário, ajuda automatizada — existe em múltiplas páginas, ele MUST aparecer na **mesma ordem relativa** em todas elas.

- Não exige que a ajuda exista; exige que, existindo, ela não mude de lugar. Quem tem dificuldade de memória espacial reencontra a ajuda pela posição.
- Em código: o ponto de ajuda vive no layout compartilhado (header/footer/template), nunca posicionado caso a caso por página.
- "Mesma ordem relativa" não é a mesma coordenada em pixels: o layout pode responder ao viewport desde que a ordem entre os elementos se preserve.

## 4. SC 1.4.12 Espaçamento de Texto (AA)

O conteúdo MUST sobreviver sem perda de informação ou função quando o usuário força, via folha de estilo própria: entrelinha **1,5×** o tamanho da fonte, espaço após parágrafo **2×**, espaçamento entre letras **0,12×** e entre palavras **0,16×**.

É o critério que serve diretamente a dislexia e baixa visão, e é quebrado por três padrões de CSS gerado:

```css
/* ❌ altura fixa em contêiner de texto — o texto vaza ou é cortado */
.card { height: 120px; overflow: hidden; }

/* ❌ entrelinha travada contra a preferência do usuário */
p { line-height: 1.2 !important; }

/* ✅ o contêiner acompanha o conteúdo */
.card { min-height: 120px; }
p { line-height: 1.5; }
```

## 5. SC 2.2.1 Tempo Ajustável (A)

Todo limite de tempo MUST poder ser **desligado**, **ajustado** para pelo menos 10× o padrão, ou **estendido**: aviso com pelo menos 20 segundos de antecedência e possibilidade de estender ao menos 10 vezes, por uma ação simples ("pressione a barra de espaço").

Sessões bancárias, carrinhos com reserva de estoque e provas cronometradas são os casos reais. *(A mecânica de conteúdo em movimento — carrosséis, autoplay — é a SC 2.2.2, no [guia de Mídia Temporal](guide-media.md).)*

## 6. Linguagem

A WCAG só exige nível de leitura em AAA (SC 3.1.5), o que deixa a clareza fora da conformidade AA — e não fora da obrigação de uso. Quando a IA gera texto de interface:

- **Voz ativa, frase curta, uma ideia por frase.** "Não deixe de confirmar" vira "Confirme".
- **Sem dupla negação** e sem condicional empilhada.
- **Literal, não figurado.** Metáfora, ironia e expressão idiomática são barreiras diretas para parte do público autista e para quem lê em segunda língua.
- **A palavra mais comum que serve.** "Usar" em vez de "utilizar"; "antes" em vez de "previamente".
- **O rótulo diz o resultado**, não o mecanismo: "Salvar rascunho", não "Submeter".
- **Instrução crítica não vive em `placeholder` nem em tooltip.** Ela precisa estar visível quando a pessoa está decidindo.
- **Erro nomeia a saída.** "CPF inválido" é diagnóstico; "O CPF tem 11 dígitos — verifique se faltou algum" é instrução.
- **Linguagem Sensorial (SC 1.3.3):** instruções **MUST NOT** depender só dos sentidos — "clique no botão redondo à direita", "aguarde o sinal sonoro". Nomeie o controle pelo rótulo visível: "clique em **Enviar**, no fim do formulário". Instruções de formato ("DD/MM/AAAA") vivem fora do campo, ligadas via `aria-describedby`.

## 7. Necessidades de acesso conflitantes

Nem todo conflito é acessibilidade contra negócio. Alguns são **acessibilidade contra acessibilidade**, e é onde um agente silenciosamente escolhe uma população e chama o resultado de conformidade.

| Eixo | Uma necessidade | A necessidade oposta |
| :--- | :--- | :--- |
| Movimento | animação de transição sustenta a continuidade para quem tem dificuldade de rastrear mudança de contexto | translação e parallax disparam náusea em distúrbio vestibular |
| Linguagem | simplificar reduz carga cognitiva | simplificar remove precisão de que o usuário especialista depende |
| Contraste | contraste máximo serve baixa visão | contraste máximo agride sensibilidade a brilho (Irlen, enxaqueca) |
| Tempo | limite curto protege sessão sensível | limite curto exclui quem lê ou digita devagar |
| Densidade | mais informação por tela reduz navegação para quem tem dor crônica ou limitação motora | mais informação por tela aumenta a carga para quem tem déficit de atenção |

### O protocolo

1. **Detecte e diga.** Quando a mitigação de uma necessidade cria barreira para outra, a IA **MUST** nomear as duas populações em vez de otimizar uma delas em silêncio.
2. **Prefira o mecanismo à arbitragem.** Se existe um canal em que o próprio usuário decide — `prefers-reduced-motion`, `prefers-contrast`, uma preferência da conta, o zoom do sistema —, a resposta é implementar o canal, nunca escolher pelo usuário. É assim que o conflito de movimento já está resolvido no [guia de Mídia](guide-media.md).
3. **Sem mecanismo, escale.** A IA **MUST NOT** decidir sozinha qual deficiência é atendida. Apresente o conflito, as duas populações e as opções ao desenvolvedor — mesma forma do *Image Evidence*: a máquina prepara a evidência, o humano estabelece a decisão.
4. **Registre no `A11Y-DECISIONS.md`,** indexado por padrão, com **as duas necessidades nomeadas** e o motivo da escolha. Um conflito resolvido e não registrado volta como divergência no próximo componente.
5. **Maioria não é critério.** "A maioria dos usuários prefere" é argumento de usabilidade, não de acessibilidade: a população menor é justamente a que o padrão existe para não perder.

## 8. Os oito objetivos do W3C (mapa de cobertura)

O [W3C Cognitive Accessibility Guidance](https://www.w3.org/WAI/WCAG2/supplemental/#cognitiveaccessibilityguidance) organiza o campo em oito objetivos. Eles não são normativos — servem para descobrir a barreira que nenhum SC nomeia:

1. Ajudar a entender o que as coisas são e como usá-las
2. Ajudar a encontrar o que se procura
3. Usar conteúdo claro e compreensível
4. Ajudar a evitar erros e a corrigi-los
5. Ajudar a manter o foco
6. Garantir que processos não dependam de memória
7. Oferecer ajuda e suporte
8. Apoiar adaptação e personalização

*Critérios de sucesso cobertos: 1.3.3 Características Sensoriais (A) · 3.2.6 Ajuda Consistente (A) · 3.3.7 Entrada Redundante (A) · 2.2.1 Tempo Ajustável (A) · 3.3.8 Autenticação Acessível (Mínimo) (AA) · 1.4.12 Espaçamento de Texto (AA) · 3.3.2 Rótulos ou Instruções (A) · 3.3.3 Sugestão de Erro (AA) · 3.3.9 Autenticação Acessível (Melhorada) (AAA (perfil Shield)) · 3.1.5 Nível de Leitura (AAA)*
