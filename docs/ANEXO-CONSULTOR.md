# Anexo do Consultor — mapa-ia-pppm

> **Uso interno.** Este documento não acompanha o PDF entregue ao cliente.
> É o caderno de bordo do consultor durante a aplicação das Aulas 1, 2 e 3
> do curso de IA em PPPM do Prof. Dr. José Bezerra (BSBr).

## Ponte entre as Aulas 1, 2 e 3 (Aula 3 · slide de fechamento)

```
AULA 1                    AULA 2                    AULA 3
"Onde estamos"            "Onde aplicar"            "Por que vale investir"
Diagnóstico +             Casos + Priorização +     Business Case +
Mapa Inicial              Governança HITL           ROI + Decisão comitê
```

**Princípio da Aula 3:** *"Ideia boa só vira investimento quando demonstra
valor, risco controlado e retorno esperado."*

**Papel do consultor (Aula 3 · slide 5):** *"Traduzir tecnologia em decisão
de investimento."* Não vender entusiasmo — reduzir incerteza para o comitê.

## Para que serve este anexo

O app `mapa-ia-pppm` é o esqueleto formal: formulários, cálculos e cortes
obrigatórios. Os **prompts** deste anexo são muletas cognitivas usadas
**FORA do app** (em ChatGPT, Claude ou Gemini) para transformar entrevistas,
atas e planilhas soltas em informação estruturada que você DIGITA nos campos
do app.

Fluxo padrão (Aula 3 · slide "Como transformar dados dispersos em
recomendação"):

```
Dados dispersos     →  Síntese com IA    →  Análise executiva  →  Recomendação
(atas, relatórios,     (padrões, causas,     (valor, custo,        (decisão, piloto,
cronogramas,           sinais, hipóteses)    risco, premissas)     indicadores,
riscos, feedbacks)                                                 controles)
```

**Importante:** o app **NÃO executa** nenhum prompt. O botão "Carregar progresso"
só aceita arquivo `.json` exportado por sessão anterior — não aceita PDF nem
texto solto. O caminho é sempre: **documento → ChatGPT (com prompt) → você lê
a saída → digita a essência nos campos do app**.

O app é 100% determinístico — aritmética direta sobre os inputs digitados.

---

# Mapa de Uso — qual prompt preenche o quê no app

Esta é a resposta objetiva à pergunta *"pra que serve cada prompt e onde a saída
vai no app?"*. As colunas Streamlit e HTML citam a aba/etapa correspondente.

| Prompt | O que a IA produz | Onde a saída é usada no app |
|---|---|---|
| **Prompt 1.1** — Entrevista estruturada | Notas 0-6 por dimensão + trecho literal | Diagnóstico *(Streamlit: Aba 2 · HTML: Etapa 2)* |
| **Prompt 1.2** — Mapa Inicial | 5 blocos de texto (Contexto · Dor · Dados · Riscos · Valor) | Mapa Inicial *(Streamlit: Aba 3 · HTML: Etapa 3)* |
| **Prompt 2.1** — Geração de casos | Tabela de 3-5 casos com rótulo, dor, fluxo, dono, dados | Cadastro de casos *(Streamlit: Aba 4 · HTML: Etapa 4)* |
| **Prompt 2.2** — HITL por caso | Nível HITL + responsável + rastreabilidade por caso | Governança *(Streamlit: Aba 5 · HTML: Etapa 7)* |
| **Ferramenta 1 (Prof)** / **Prompt 3.1 SMART** — Diagnóstico executivo | Problema · objetivo · alternativas · consequências · trade-offs | Blocos 1-3 do Business Case (Problema descrito · Linha de base · Caso de uso) *(Streamlit: Aba 6 · HTML: Etapa 10)* |
| **Ferramenta 2 (Prof)** / **Prompt 3.2 SMART** — Riscos e governança | Tabela de riscos baixo/médio/alto com controle e HITL | Bloco 6 do Business Case (Riscos e controles) *(Streamlit: Aba 6 · HTML: Etapa 10)* + Governança *(Streamlit: Aba 5 · HTML: Etapa 7)* |
| **Ferramenta 3 (Prof)** / **Prompt 3.3 SMART** — Priorização e ROI | Comparação entre 2+ casos com nota justificada + estimativa grosso de ROI/payback | Uso auxiliar — te ajuda a decidir quais casos merecem Business Case detalhado. O app calcula o ROI final sozinho na Etapa 10 / Aba 6 depois que você digita os números. |
| **Prompt 3.4 SMART** — Premortem *(adição, fora do slide)* | 5 causas prováveis de fracasso do piloto | Uso 100% interno do consultor. Não vai no app nem no PDF. Serve para você ajustar o escopo antes do comitê. |
| **Ferramenta 4 (Prof)** / **Prompt 3.5 SMART** — Plano executivo | Recomendação de 1 página com 10 seções para comitê | Documento COMPLEMENTAR ao PDF do app. O PDF do app tem tudo; o plano executivo é a capa de 1 página que o comitê lê em 90 segundos. |

## Ranking no app — resposta a uma dúvida comum

O app TEM ranking automático:

- **HTML** — Etapa 5 gera score ponderado 1-5 por caso · Etapa 6 posiciona na matriz Impacto × Viabilidade · Etapa 8 seleciona os 3 prioritários
- **Streamlit** — Aba 4 exibe tabela ordenada com score, faixa (Fazer agora / Preparar / Não priorizar) e quadrante

A **Ferramenta 3** do Prof não substitui esse ranking — ela ADICIONA justificativa
qualitativa de cada nota + estimativa preliminar de ROI/payback (grosso, sem os
dados detalhados de custo). Útil quando você tem 5 candidatos e precisa decidir
quais 3 merecem entrar no Business Case detalhado da Etapa 10 / Aba 6.

---

# Padrão SMART dos prompts

Todos os prompts SMART seguem o template **S · M · A · R · T**:

| Letra | Bloco | O que declara |
|---|---|---|
| **S** | Situação | Quem é você, onde está, o que faz |
| **M** | Mensagem | Ação exata da IA — verbo específico e escopo delimitado |
| **A** | Alvo | Público-alvo e objetivo final da resposta |
| **R** | Referência | Estilo, tom, framework ou exemplo a seguir |
| **T** | Tipo | Formato, tamanho, idioma e CTA da resposta |

Complementos de engenharia de prompt aplicados nas versões SMART:

- **80/20** — 80% do prompt é prevenção (o que evitar); 20% é instrução
- **CoT 2026** — não pedir "pense passo a passo"; dar os critérios explícitos
- **Saída estruturada** — quando o output vira input de outro sistema, exigir formato
- **Reasoning ON** para análise/decisão; OFF para brainstorm/redação criativa

---

# Aula 1 — Diagnóstico e Mapa Inicial

**Objetivo da aula:** medir maturidade em 5 dimensões (nota 0-6, nível 0-3),
identificar gargalo prioritário e montar o Mapa Inicial em 5 blocos
(Contexto · Dor · Dados · Riscos · Valor).

## Prompt 1.1 — Entrevista estruturada de diagnóstico

**Quando usar:** logo após a primeira reunião com o cliente, para transformar
notas de entrevista soltas em nota de 0-6 nas 5 dimensões do app.

**Por que usar:** o aluno tende a dar notas "no achismo" ao preencher a
Aba/Etapa 2. O prompt força atribuição da nota a evidência textual — reduz
viés de disponibilidade e ancoragem.

**Como usar:** colar transcrição da reunião OU respostas ao questionário
inicial. Rodar com reasoning **ON**.

**Onde vai a saída:** Diagnóstico *(Streamlit: Aba 2 · HTML: Etapa 2)*.

```
S — Situação: Sou consultor aplicando o diagnóstico de maturidade em IA da
    Aula 1 do Prof. Bezerra (BSBr) em uma empresa de porte [PORTE] do setor
    [SETOR]. Terminei a primeira entrevista com o sponsor e tenho as notas
    abaixo.
M — Mensagem: Para CADA uma das 5 dimensões (Estratégia · Dados · Talento
    · Governança · Cultura), atribua nota 0-6 com JUSTIFICATIVA em 1 linha
    citando trecho literal da entrevista. Ao final, aponte a dimensão de
    MENOR nota como gargalo prioritário. NÃO invente evidência — se a
    entrevista não cobrir uma dimensão, escreva "sem evidência coletada,
    revisitar em entrevista 2". NÃO use jargão consultor genérico
    (transformação digital, jornada, unlock).
A — Alvo: Consultor (uso interno); objetivo é preencher o Diagnóstico do
    app com nota justificada por evidência.
R — Referência: Escala 0-6 do slide 26 (0-1 inicial · 2-3 desenvolvendo ·
    4-5 definido · 6 otimizado); vocabulário da Aula 1.
T — Tipo: Tabela Markdown 5 linhas × 3 colunas (Dimensão · Nota · Trecho
    literal); após a tabela, 1 parágrafo curto nomeando o gargalo. pt-BR.

Entrada: [colar transcrição da entrevista OU respostas ao questionário]
```

## Prompt 1.2 — Mapa Inicial em 5 blocos

**Quando usar:** depois do diagnóstico (Aba/Etapa 2 preenchida), para gerar
o rascunho dos 5 blocos do Mapa Inicial.

**Por que usar:** o Mapa Inicial é a peça de comunicação com o sponsor.
Sem prompt, o aluno escreve blocos desiguais (Contexto longo, Riscos vazio).

**Como usar:** colar notas da entrevista + as notas de 0-6 já atribuídas.
Reasoning **OFF** (é redação executiva).

**Onde vai a saída:** Mapa Inicial *(Streamlit: Aba 3 · HTML: Etapa 3)*.

```
S — Situação: Terminei o diagnóstico de maturidade em IA da Aula 1 e
    preciso montar o Mapa Inicial em 5 blocos.
M — Mensagem: Produza um bloco de 3-5 linhas para cada uma das 5 seções:
    (1) Contexto do negócio, (2) Dor mensurável, (3) Dados disponíveis
    e lacunas, (4) Riscos e restrições, (5) Valor potencial. Cada bloco
    deve terminar com UMA frase de arremate. NÃO ultrapasse 5 linhas por
    bloco. NÃO use bullets — texto corrido. NÃO cite fornecedor de IA
    específico (OpenAI, Google) no bloco Contexto.
A — Alvo: Sponsor do cliente; objetivo é ele reconhecer o próprio negócio
    em 30 segundos de leitura.
R — Referência: Estilo executivo direto; vocabulário da Aula 1 (dor
    mensurável, dados, HITL, valor potencial).
T — Tipo: Markdown com 5 subseções nomeadas (## Contexto · ## Dor · ##
    Dados · ## Riscos · ## Valor); pt-BR; máximo 400 palavras totais.

Entrada: [colar notas de 0-6 das 5 dimensões + trechos da entrevista]
```

---

# Aula 2 — Casos de Uso, Priorização e Governança HITL

**Objetivo da aula:** cadastrar N casos de uso com dor mensurável e dono
declarado, priorizar por score ponderado (5 critérios) e definir nível de
HITL (leve · estruturada · executiva) por caso.

## Prompt 2.1 — Geração de casos de uso a partir da dor

**Quando usar:** quando o cliente identifica uma dor (Bloco 2 do Mapa) mas
não sabe traduzir em caso de uso concreto de IA.

**Por que usar:** evita o erro clássico do slide 8 da Aula 2 — pular direto
para "vamos usar IA generativa" sem definir entrada, processamento e saída.

**Como usar:** colar a dor + o gargalo do diagnóstico. Reasoning **ON**.

**Onde vai a saída:** Cadastro de casos *(Streamlit: Aba 4 · HTML: Etapa 4)*.

```
S — Situação: O cliente tem a dor mensurável abaixo e o gargalo prioritário
    identificado no diagnóstico da Aula 1. Preciso gerar 3-5 casos de uso
    candidatos de IA que serão cadastrados no app mapa-ia-pppm.
M — Mensagem: Para cada caso, descreva: (1) rótulo curto (até 8 palavras),
    (2) dor específica endereçada, (3) fluxo entrada → processamento → saída
    em 1 linha, (4) dono humano da decisão (cargo, não nome), (5) dados
    necessários. NÃO gere caso que dependa de dado inexistente na empresa.
    NÃO proponha "chatbot genérico" ou "assistente virtual" — exija verbo
    de ação (classificar, priorizar, prever, resumir, alertar). NÃO ultra-
    passe 5 casos — melhor 3 casos densos que 5 rasos.
A — Alvo: Consultor; objetivo é ter 3-5 linhas prontas para digitar no
    CRUD de casos.
R — Referência: 7 domínios da Aula 2 (slides 16-22); princípio "IA no
    processo de decisão, não no lugar da decisão".
T — Tipo: Tabela Markdown 5 colunas (Rótulo · Dor · Fluxo · Dono · Dados);
    pt-BR.

Entrada:
- Dor mensurável: [colar]
- Gargalo prioritário: [colar]
- Setor/porte da empresa: [colar]
```

## Prompt 2.2 — Definição de HITL por caso

**Quando usar:** depois de cadastrar os casos (Aba/Etapa 4), antes de definir
governança.

**Por que usar:** a Aula 2 tem regra clara — "quanto maior o impacto da
decisão, maior a validação humana". Sem prompt, o aluno escolhe HITL "leve"
por default.

**Como usar:** colar a lista de casos com dono e dor. Reasoning **ON**.

**Onde vai a saída:** Governança *(Streamlit: Aba 5 · HTML: Etapa 7)*.

```
S — Situação: Tenho N casos de uso cadastrados e preciso definir o nível
    de HITL (Human In The Loop) de cada um antes de preencher a Governança.
M — Mensagem: Para cada caso, classifique HITL em (a) LEVE — humano revisa
    amostragem periódica, (b) ESTRUTURADA — humano aprova cada saída antes
    de aplicar, (c) EXECUTIVA — humano decide, IA só recomenda. Para cada
    classificação, aponte: (1) motivo em 1 linha, (2) responsável nominal
    (cargo), (3) evidência de rastreabilidade obrigatória (log · ata · e-mail
    · sistema). NÃO classifique como LEVE qualquer caso que afete cliente
    final ou decisão financeira acima de R$ 10 mil. NÃO deixe caso sem
    responsável — se não há dono, marque "BLOQUEADO — sem dono humano".
A — Alvo: Consultor + sponsor; objetivo é passar no corte obrigatório da
    Aula 2 (slide 30).
R — Referência: 3 níveis de HITL da Aula 2 (slides 32-36); princípio de ouro
    "impacto ↑ = validação humana ↑".
T — Tipo: Tabela Markdown 5 colunas (Caso · HITL · Motivo · Responsável ·
    Rastreabilidade); pt-BR.

Entrada: [colar lista de casos com rótulo, dono e dor]
```

---

# Aula 3 — Business Case, ROI e Decisão do Comitê

**Objetivo da aula:** transformar o caso priorizado em business case
preliminar com 8 blocos, benefício em 3 camadas, custo em 5 camadas,
riscos com controle, ROI/Payback em 3 cenários e decisão registrada.

## Os 9 blocos do business case (slide "Estrutura" + linha de base v1.2)

| # | Bloco | Pergunta central | Onde no app |
|---|---|---|---|
| 01 | Problema descrito | O que dói hoje (com contexto)? | Etapa 10 / Aba 6 · seção Problema |
| 02 | Linha de base | Qual o valor atual do KPI (número, prazo, custo, frequência)? | Etapa 10 / Aba 6 · campo Linha de base |
| 03 | Caso de uso | Como a IA atuará no processo ou decisão? | Etapa 10 / Aba 6 · seção Caso de uso |
| 04 | Dados necessários | Quais dados a IA vai consumir e como serão validados? | Etapa 10 / Aba 6 · seção Dados |
| 05 | Benefícios esperados | Perda × %redução (auto) + receita adicional + custo evitado + operacional + estratégico | Etapa 10 / Aba 6 · 3 camadas de benefício |
| 06 | Custos estimados | Quais custos além da licença? | Etapa 10 / Aba 6 · 5 camadas de custo |
| 07 | Riscos e controles | O que pode dar errado e como controlar? | Etapa 10 / Aba 6 · seção Riscos |
| 08 | ROI / Payback | Qual retorno esperado e em quanto tempo? | **Calculado automaticamente pelo app** |
| 09 | Decisão solicitada | O que queremos aprovar agora? | Etapa 10 / Aba 6 · seletor de decisão |

**Pergunta executiva-chave (slide "Conceito-chave"):** *"Com base nisso,
devemos investir, ajustar, testar ou abandonar?"*

## Filtro top-3 na entrada da Aula 3

O slide "Passo a passo da atividade" da Aula 3 sugere explicitamente:
*"Tempo sugerido: 25 min individual/grupo + 20 min discussão de **2 ou 3
casos**."*

Isso valida o afunilamento: **da lista completa da Aula 2 → só 2-3 casos
viram business case denso na Aula 3.** Melhor 3 casos densos que 5 rasos.
No HTML, isso é feito na Etapa 8 (Seleção dos 3 prioritários).

Critérios de corte cumulativos:

- **A** — dono humano declarado (Aula 2 · slide 30 · herdado)
- **B** — score ≥ 3,0
- **C** — top-3 por score

Casos excluídos NÃO deletar — mostrar em bloco cinza com motivo. Isso ensina
o afunilamento, que é o coração da Aula 3.

---

## Prompts LITERAIS do Prof. Bezerra (Aula 3 · slides "Ferramenta 1 a 4")

Preservados sem reescrita para fidelidade pedagógica. Use estes quando
estiver **ensinando** o método. Para consultoria real, use as versões
SMART logo abaixo.

### Ferramenta 1 · Prompt para diagnóstico executivo

**Onde a saída vai no app:** Blocos 1-3 do Business Case (Problema descrito +
Linha de base + Caso de uso) na Etapa 10 / Aba 6. Pode também informar o Diagnóstico
(Etapa 2 / Aba 2) e o Mapa Inicial (Etapa 3 / Aba 3) da Aula 1.

> Atue como consultor sênior em PPPM. Com base nas informações abaixo,
> identifique:
> 1) problema central;
> 2) causas prováveis;
> 3) indicadores afetados;
> 4) impacto financeiro ou operacional;
> 5) hipótese de caso de uso de IA;
> 6) dados necessários para validar a hipótese.
> Responda em formato executivo.

**Entrada recomendada (rodapé do slide):** histórico de projetos, indicadores,
entrevistas, atas, riscos e reclamações recorrentes.

### Ferramenta 2 · Prompt para riscos e governança

**Onde a saída vai no app:** Bloco 6 do Business Case (Riscos e controles) na
Etapa 10 / Aba 6 + Governança (Etapa 7 / Aba 5). Preenche os campos "nível
baixo/médio/alto" e "controle textual" de cada risco.

> Avalie o caso de uso de IA descrito abaixo sob a ótica de riscos, ética,
> dados, segurança e governança. Classifique os riscos em baixo, médio e
> alto. Indique controles mínimos, ponto de intervenção humana, responsáveis,
> evidências de rastreabilidade e critérios para interromper o piloto.

**Regra de arremate do slide:** *"IA recomenda. Humano valida, decide e
responde."*

### Ferramenta 3 · Prompt para priorização e ROI

**Onde a saída vai no app:** uso auxiliar — te ajuda a decidir quais casos
merecem business case detalhado. O ranking próprio do app já existe (Etapa
5-6-8 no HTML / Aba 4 no Streamlit). O ROI/Payback é calculado pelo app na
Etapa 10 / Aba 6 depois que você digita os números — a Ferramenta 3 dá
apenas uma estimativa preliminar grosso.

> Compare os casos de uso abaixo usando os critérios: impacto, viabilidade,
> dados, risco e valor. Atribua notas de 1 a 5, explique cada nota, estime
> benefício, custo, ROI e payback quando houver dados suficientes. Ao final,
> recomende onde começar e quais premissas precisam ser validadas no piloto.

**Rodapé do slide:** *"Use com a matriz da Aula 2: impacto, viabilidade,
dados, risco e valor."*

### Ferramenta 4 · Prompt para plano executivo

**Onde a saída vai no app:** documento COMPLEMENTAR ao PDF do app, não vai
dentro dele. O PDF do app tem 10+ seções; o Plano Executivo é uma peça de
1 página só que vai por cima como capa para o comitê decidir em 90 segundos.

> Com base neste business case preliminar, produza uma recomendação executiva
> de até uma página contendo: problema, solução de IA, benefícios esperados,
> investimento, ROI estimado, riscos, governança, cronograma do piloto,
> responsáveis, indicadores e decisão solicitada ao comitê.

**Resultado esperado (rodapé do slide):** *"Uma peça executiva que permita
decidir, não apenas entender."*

---

## Versões SMART (uso em consultoria real)

Interpretação dos 4 prompts do Prof, reescritos em SMART com 80/20 de
prevenção e critérios explícitos. Use quando o cliente é pagante e você
precisa de saída auditável.

### Prompt 3.1 · Diagnóstico executivo (SMART)

**Quando usar:** ANTES de escrever o business case, para transformar dados
dispersos em diagnóstico estruturado.

**Por que usar:** o business case exige dor mensurável. Sem prompt, o aluno
escreve "processo lento" — sem número, sem fonte. Este força métrica e
percorre as 5 etapas de decisão.

**Onde vai a saída:** Blocos 1-2 do Business Case (Etapa 10 / Aba 6) —
mesmo destino da Ferramenta 1 literal, com output mais estruturado.

```
S — Situação: Sou consultor sênior em PPPM aplicando o método da Aula 3
    do Prof. Bezerra (BSBr) para transformar dados dispersos em diagnóstico
    estruturado antes de escrever o business case.
M — Mensagem: Analise as evidências abaixo e produza diagnóstico que
    percorra as 5 etapas de decisão: (1) definir problema central em uma
    frase, (2) especificar objetivo mensurável, (3) listar até 3 alternativas
    de caso de uso de IA, (4) discutir consequências de cada uma (impacto
    financeiro/operacional, dados necessários, risco principal), (5) nomear
    trade-offs explícitos. NÃO invente números — marque como "estimativa"
    qualquer valor sem fonte na entrada. NÃO use jargão consultor genérico
    (sinergia, alavancar, unlock, transformar).
A — Alvo: Comitê executivo do sponsor; objetivo é reduzir incerteza para
    decidir se o caso merece business case completo.
R — Referência: Estilo objetivo, tom analítico; vocabulário da Aula 3
    (dor mensurável · caso de uso · dados · benefício em 3 camadas · HITL).
T — Tipo: Markdown com 5 seções nomeadas (Problema · Objetivo · Alternativas
    · Consequências · Trade-offs); no máximo 400 palavras; pt-BR.

Entrada: [colar histórico de projetos, indicadores, entrevistas, atas,
riscos e reclamações recorrentes]
```

### Prompt 3.2 · Riscos e governança (SMART)

**Quando usar:** DEPOIS de propor a solução, ANTES de estimar custos.

**Por que usar:** obriga a pressionar o caso pela ótica de risco antes de o
sponsor assumir compromisso financeiro. Aciona o checklist de vieses.

**Onde vai a saída:** Bloco 6 do Business Case (Etapa 10 / Aba 6) — nível
baixo/médio/alto e controle textual de cada risco.

```
S — Situação: Sou consultor pressionando o caso de uso de IA já proposto
    pela ótica de risco, ética e governança antes que o sponsor assuma
    compromisso financeiro (Aula 3 · Ferramenta 2).
M — Mensagem: Avalie o caso descrito e (1) classifique cada risco em
    baixo/médio/alto com JUSTIFICATIVA de 1 linha, (2) para cada risco alto
    aponte controle mínimo obrigatório, ponto de intervenção humana (HITL),
    responsável nominal e evidência de rastreabilidade, (3) defina 3
    critérios objetivos que interrompem o piloto ("kill switches"). Rode
    mentalmente o checklist de vieses: excesso de confiança, confirmação,
    groupthink — nomeie se detectar. NÃO liste risco sem controle
    correspondente. NÃO use "monitorar" ou "acompanhar" como controle —
    exija verbo de ação (validar, aprovar, auditar, bloquear).
A — Alvo: GP e sponsor; objetivo é ter tabela de risco pronta para
    validação humana e comitê.
R — Referência: Framework HITL da Aula 2 (leve · estruturada · executiva)
    + catálogo de risco da Aula 3 (dados sensíveis · decisão indevida ·
    baixa adoção · viés ou erro).
T — Tipo: Tabela Markdown 6 colunas (Risco · Nível · Justificativa ·
    Controle · HITL · Kill switch); após a tabela, 3 bullets com vieses
    detectados na proposta. pt-BR.

Entrada: [colar descrição do caso de uso, dados envolvidos, decisões
afetadas]
```

### Prompt 3.3 · Priorização entre casos (SMART)

**Quando usar:** quando há 2+ casos candidatos e é preciso comparar antes
de recomendar por onde começar.

**Por que usar:** o app calcula ROI/Payback determinístico, mas não faz
comparação qualitativa nem checa premissas. Este prompt cobre essa lacuna.

**Onde vai a saída:** uso auxiliar externo — te ajuda a escolher quais casos
merecem Business Case detalhado. A saída não vai para nenhum campo do app.

```
S — Situação: Tenho 2+ casos de uso candidatos e preciso recomendar por
    onde começar antes de gastar orçamento de piloto (Aula 3 · Ferramenta
    3). O app já calcula ROI/Payback determinístico — este prompt NÃO
    recalcula, apenas compara qualitativamente e checa premissas.
M — Mensagem: Compare os casos usando os 5 critérios da Aula 2 (Impacto ·
    Viabilidade · Dados · Risco · Valor estratégico) com nota 1-5 e
    JUSTIFICATIVA por nota. Ao final: (a) recomende UM caso para começar
    com racional explícito, (b) liste as premissas que precisam ser
    validadas no piloto para o ROI se sustentar, (c) nomeie qual heurística
    de decisão poderia estar contaminando o ranking (disponibilidade,
    representatividade, afeto, ancoragem). NÃO empate — se dois casos
    tiverem score igual, use "menor risco de reputação" como desempate.
    NÃO recalcule ROI — assuma os valores já vindos do app.
A — Alvo: Comitê de portfólio; objetivo é 1 decisão de "por onde começar"
    com premissas auditáveis.
R — Referência: Matriz Impacto × Viabilidade da Aula 2 + princípio Aula 3
    "reduzir incerteza, não vender entusiasmo".
T — Tipo: Tabela comparativa (linhas = casos, colunas = 5 critérios +
    total) + 3 seções após a tabela (Recomendação · Premissas do piloto ·
    Heurística contaminante). pt-BR, até 500 palavras.

Entrada: [colar lista de casos com dor, solução, dados, ROI calculado
pelo app]
```

### Prompt 3.4 · Premortem (SMART · adição, fora do slide)

**Quando usar:** DEPOIS de decidir "por onde começar", ANTES de gerar o
plano executivo do comitê.

**Por que usar:** força o consultor a imaginar o fracasso ANTES de vender
o sucesso. Combate direto ao excesso de confiança.

**Aviso:** este prompt NÃO consta na Aula 3 do Prof. É adição minha baseada
na técnica de Gary Klein (*Sources of Power*). Uso 100% interno — não vai
no app nem no PDF do cliente.

**Onde vai a saída:** análise interna do consultor; ajusta o escopo do piloto
antes de submeter ao comitê.

```
S — Situação: Já decidi qual caso vai virar piloto e o business case está
    completo no app mapa-ia-pppm. ANTES de escrever o plano executivo
    para o comitê, preciso rodar um premortem para pressionar a decisão.
M — Mensagem: Escreva o cenário: "Seis meses depois do go-live, o piloto
    foi cancelado com prejuízo." Liste (1) as 5 causas mais prováveis do
    fracasso em ordem de probabilidade, (2) para cada causa, o SINAL
    ANTECIPADO que o comitê poderia ter visto na semana 2, (3) para cada
    causa, o ajuste no escopo do piloto que preveniria. NÃO minimize
    causas com "gestão de mudança" ou "comunicação insuficiente" — esses
    são sintomas, não causas. NÃO cite falha de tecnologia genérica —
    aponte qual componente específico falha.
A — Alvo: Consultor (uso interno); objetivo é ajustar o plano executivo
    antes de submeter ao comitê.
R — Referência: Técnica de premortem de Gary Klein (*Sources of Power*).
T — Tipo: Tabela Markdown 3 colunas (Causa · Sinal semana 2 · Ajuste
    preventivo); pt-BR; exatamente 5 linhas.

Entrada: [colar caso recomendado + business case completo do app]
```

### Prompt 3.5 · Plano executivo de 1 página (SMART)

**Quando usar:** DEPOIS do premortem, para gerar a peça final que vai ao
comitê.

**Por que usar:** o comitê decide em 90 segundos. Sem prompt, o aluno
entrega 3 páginas de contexto e 1 parágrafo de decisão. Este inverte.

**Onde vai a saída:** documento COMPLEMENTAR ao PDF do app. Vai por cima
como capa executiva; o PDF do app entra como anexo detalhado.

```
S — Situação: Business case preliminar do caso está preenchido no app
    (números de ROI/Payback já calculados) e o premortem foi rodado.
    Preciso gerar a peça de 1 página para o comitê que decide (Aula 3 ·
    Ferramenta 4).
M — Mensagem: Produza recomendação executiva de 1 página com estas seções
    OBRIGATÓRIAS na ordem: (1) Problema com indicador impactado, (2)
    Solução de IA em 2 frases, (3) Benefícios nas 3 camadas (financeiro R$
    · operacional horas · estratégico texto), (4) Investimento total e
    detalhamento por camada, (5) ROI e Payback no cenário provável + faixa
    conservador-otimista, (6) 3 riscos principais com controle e HITL, (7)
    Cronograma do piloto (marcos + datas), (8) Responsáveis nominais, (9)
    Indicadores de sucesso mensuráveis (com linha de base, fórmula, dono,
    fonte, frequência), (10) Decisão solicitada ao comitê em UMA frase.
    NÃO adicione seção de "conclusão" ou "próximos passos genéricos". NÃO
    altere os números do app — cite-os como vieram. Se faltar dado para
    alguma seção, escreva "PENDENTE — [o que falta]".
A — Alvo: Comitê executivo do sponsor com poder de aprovar orçamento;
    leitura em 90 segundos.
R — Referência: Roteiro de 5 minutos da Aula 3 (problema · solução ·
    ROI · riscos · decisão) + princípio de ouro da governança
    (impacto ↑ = validação humana ↑).
T — Tipo: Markdown com 10 seções numeradas exatamente como listadas;
    máximo 1 página A4 (~450 palavras); pt-BR; tom decisório.

Entrada:
- Business case do app: [colar]
- Resultado do premortem: [colar]
```

---

# Memória de Cálculo — Como o Comitê Chega às Conclusões

Esta seção documenta EXATAMENTE como o app calcula cada número do painel
de indicadores da Etapa 10 / Aba 6 e do PDF final. Nenhum número vem de LLM;
tudo é aritmética determinística sobre os inputs digitados pelo consultor.

Código-fonte de referência (versão Streamlit): `src/business_case.py`.
Mesma lógica portada para o `index.html` da versão HTML.

## Fórmula oficial (Aula 3 · slide "ROI · A pergunta financeira essencial")

```
ROI = (Benefícios líquidos − Investimento) ÷ Investimento × 100

Benefícios líquidos = Economia + receita adicional + custos evitados
Investimento        = Tecnologia + pessoas + dados + mudança + governança
Tempo               = Janela de análise: 6, 12 ou 24 meses
```

**Regra do slide:** *"A regra é simples: explicite premissas, estime cenários
e não confunda potencial com resultado garantido."*

## Exemplo calculado pelo Prof. (Aula 3 · slide "Exemplo calculado — Mini business case: IA para reduzir retrabalho")

| Item | Estimativa anual |
|---|---:|
| Retrabalho atual | R$ 600.000 |
| Redução esperada com IA | 25% |
| **Benefício estimado** | **R$ 150.000** |
| **Investimento total** | **R$ 60.000** |
| ROI | **150%** |
| Payback | **4,8 meses** |

**Cálculo:**

```
Benefício líquido = R$ 150.000 − R$ 60.000 = R$ 90.000
ROI               = R$ 90.000 ÷ R$ 60.000 × 100 = 150%
Payback           = R$ 60.000 ÷ (R$ 150.000 ÷ 12) = 4,8 meses
```

**Frase de arremate do slide:** *"O executivo não compra a ferramenta. Ele
compra o resultado esperado."*

## 1. Benefício bruto anual (R$)

Soma o benefício **financeiro** com o benefício **operacional monetizado**.
O benefício **estratégico** NÃO entra na conta (é qualitativo por decisão
da Aula 3 · slide "Valor estratégico").

```
FIN = economia_anual + receita_adicional_anual + custo_evitado_anual

OP  = horas_economizadas_mes × 12 × pessoas_impactadas × custo_hora

Benefício bruto anual = FIN + OP
```

**Exemplo do slide "Produtividade — Como transformar tempo economizado em
valor":**

```
12 pessoas × 5 h/mês × R$ 120/h × 12 meses = R$ 86.400/ano
```

## 2. Investimento total (R$)

Soma das 5 camadas de custo (Aula 3 · slide "Custos: o investimento real
quase nunca é só licença").

```
Investimento = Tecnologia + Dados + Pessoas + Mudança + Governança
```

| Camada | O que entra |
|---|---|
| Tecnologia | licenças, API, infraestrutura, integração |
| Dados | limpeza, acesso, qualidade, segurança |
| Pessoas | treinamento, curadoria, tempo de especialistas |
| Mudança | comunicação, adoção, suporte e ajustes |
| Governança | validação humana, auditoria, registro e controles |

**Regra do slide:** *"ROI confiável começa com custo honesto."*

## 3. Cenários conservador / provável / otimista — a explicação

O app aplica um multiplicador ao benefício bruto para simular 3 cenários
distintos. Serve para o consultor não vender o "cenário otimista" como se
fosse garantido:

| Cenário | Multiplicador | Interpretação |
|---|---|---|
| conservador | **0,5** | benefício sai pela metade — clientes cautelosos, adoção lenta, dados incompletos |
| **provável** | **1,0** | premissa realista — é o cenário que o corte "Aprovar piloto" checa |
| otimista | **1,3** | 30% acima do provável — só se todas as premissas forem confirmadas no piloto |

Fórmula:

```
Benefício ajustado = Benefício bruto anual × (janela ÷ 12) × multiplicador
Benefício líquido  = Benefício ajustado − Investimento total
```

O painel de cenários aparece na Etapa 10 / Aba 6 mostrando os 3 lado a lado.

## 4. ROI (%) e Payback (meses)

```
ROI     = (Benefício líquido ÷ Investimento total) × 100

Payback = Investimento total ÷ (Benefício bruto anual ÷ 12 × multiplicador)
```

Se o investimento for zero, ROI = **indefinido** (o app mostra "—"). É
matematicamente incorreto dividir por zero e o app não força um número falso
para não ancorar o comitê.

## 5. Cortes obrigatórios de decisão — a explicação

A decisão "Aprovar piloto" só é liberada no seletor quando os **3 cortes**
passam simultaneamente. Se qualquer um falhar, a opção fica bloqueada com
⛔ e o app lista a pendência específica:

| # | Corte | De onde vem | Se falhar |
|---|---|---|---|
| 1 | Benefício líquido > 0 no cenário **provável** | Aula 3 · slide "ROI" | "Aprovar" bloqueado. Só pode Ajustar antes do piloto, Estudar melhor ou Não recomendar neste momento. |
| 2 | Dono humano da decisão declarado | Aula 2 · slide 30 (herdado) | "Aprovar" bloqueado. Alerta pede nome do responsável. |
| 3 | Controle textual em TODO risco marcado como "alto" | Aula 3 · slide "Bloco 5" | "Aprovar" bloqueado. Lista quais riscos altos não têm controle. |

**Regra do slide "Bloco 5":** *"O risco não invalida a IA. Risco sem controle
invalida o investimento."*

As outras 3 decisões (**Ajustar antes do piloto · Estudar melhor · Não recomendar
neste momento**) NÃO têm cortes — sempre liberadas. São expressões honestas de
imaturidade do caso:

- **Estudar melhor** — a evidência ainda não é suficiente; adiar reduz risco
- **Ajustar antes do piloto** — o caso tem valor mas o recorte atual não fecha ROI
- **Não recomendar neste momento** — a análise mostrou que o custo/risco não
  justifica agora; reavaliar quando dados, contexto ou risco mudarem

## 6. Valor estratégico — a explicação (Aula 3 · slide "Valor estratégico")

4 categorias qualitativas que **NÃO entram na conta financeira** mas devem
ser declaradas no business case:

| Categoria | Descrição |
|---|---|
| Velocidade de decisão | decidir antes, com mais evidência |
| Governança | rastrear premissas, saídas e validações |
| Stakeholders | reduzir ruído, resistência e desalinhamento |
| Aprendizado | capturar lições e melhorar a maturidade |

**Regra do slide:** *"Benefício estratégico deve ser conectado a objetivos,
riscos e indicadores de gestão."*

No app: seção "Benefícios estratégicos" da Etapa 10 / Aba 6 tem 4 campos
texto para o consultor descrever cada categoria. Não vira R$.

## 7. Painel mínimo de valor — 5 metadados por métrica (Aula 3 · slide "Indicadores")

Toda métrica declarada no business case deve carregar 5 metadados. Sem eles,
o indicador vira número sem responsável:

| Metadado | Pergunta |
|---|---|
| Linha de base | Qual o valor atual, antes da IA? |
| Fórmula | Como se calcula? |
| Dono | Quem responde por essa métrica? |
| Fonte de dados | De onde vem o dado? |
| Frequência de medição | Com que periodicidade se mede? |

**Regra do slide:** *"Se ninguém é dono, ninguém cuida."*

Indicadores canônicos:

| Indicador | Mede | Exemplo |
|---|---|---|
| ROI | Retorno financeiro | 150% em 12 meses |
| Payback | Tempo de recuperação | 4,8 meses |
| Produtividade | Tempo economizado | -30% no ciclo |
| Qualidade | Erro / retrabalho | -25% retrabalho |
| Risco | Exposição reduzida | -40% incidentes |

**Nota de implementação:** o app hoje não tem campos separados para os 5
metadados. Recomendação: o consultor documenta os 5 metadados no plano
executivo (Prompt 3.5) e leva ao comitê separadamente do PDF do app.

## 8. Quantificação de perdas — 4 categorias (Aula 3 · slide "Perdas")

Como quantificar retrabalho, atraso e desperdício:

| Categoria | Fórmula |
|---|---|
| Retrabalho | horas reexecutadas × custo/hora |
| Atraso | dias de atraso × custo diário / penalidade |
| Erro de decisão | impacto esperado × probabilidade |
| Risco evitado | perda potencial × redução de exposição |

**Regra do slide:** *"A IA não precisa parecer sofisticada. Ela precisa
reduzir perdas relevantes."*

**Nota de implementação:** o app agrega tudo em "custo evitado" (camada
Financeiro). O consultor faz o cálculo por categoria FORA do app e digita
apenas o total consolidado.

## 9. O que NÃO entra na conta — a explicação (limites explícitos)

Registrado para o consultor não prometer o que o app não calcula:

| Item | Motivo |
|---|---|
| Benefício estratégico | Texto livre, não vira R$ (é qualitativo por decisão da Aula 3) |
| Custo de oportunidade | Se o time fosse fazer outra coisa, esse valor não entra |
| Risco monetizado | O app pede nível e controle textual; não converte risco em desconto financeiro |
| Custo de captação | Venda, marketing, comercial — fora do escopo da Aula 3 |
| VPL / TIR | O app usa ROI simples do slide 14; não desconta fluxo no tempo |

Se o cliente exigir análise mais rigorosa (VPL, TIR, Monte Carlo, sensitividade
formal), esses temas ficam para uma segunda camada de análise fora deste app.

---

## Template do business case preliminar (Aula 3 · slide "Entregável")

| Campo | Resposta esperada |
|---|---|
| Problema | Dor, indicador afetado e linha de base |
| Solução de IA | O que a IA fará e como será validada |
| Benefícios | Financeiros, operacionais e estratégicos |
| Custos | Tecnologia, dados, pessoas, mudança e governança |
| Riscos | Riscos principais e controles mínimos |
| ROI estimado | Premissas, cálculo, payback e cenários |
| Decisão | Aprovar piloto, ajustar, estudar ou descartar |

**Regra do slide:** *"O business case preliminar é vivo: deve melhorar
conforme dados reais do piloto aparecem."*

## Como apresentar o business case em 5 minutos (Aula 3 · slide "Comunicação executiva")

| Tempo | Conteúdo |
|---|---|
| 1 min | Problema e impacto atual |
| 1 min | Solução de IA e escopo do piloto |
| 1 min | Benefícios, custos e ROI |
| 1 min | Riscos, controles e HITL |
| 1 min | Decisão solicitada e próximos passos |

**Regra do slide:** *"No final, o comitê deve saber exatamente o que
aprovar."*

## 3 estudos simulados do Prof (Aula 3 · slides "Estudo simulado 1-3")

| # | Business case | Decisão solicitada |
|---|---|---|
| 1 | IA para reduzir risco no go-live de ERP | Aprovar piloto de 4 semanas com indicadores de atraso, retrabalho e riscos mitigados |
| 2 | IA para priorização de portfólio | Aprovar piloto na próxima janela de planejamento com valor esperado, capacidade e ROI por iniciativa |
| 3 | IA para comunicação e engajamento | Aprovar piloto restrito a 2 stakeholders com validação obrigatória antes do envio |

Frase de arremate do estudo 2: *"A IA não decide o portfólio. Ela melhora
a qualidade da conversa executiva."*

---

## Ordem de execução recomendada da consultoria

```
Reunião inicial cliente
        │
        ▼
[Prompt 1.1] Diagnóstico → digita Aba 2 / Etapa 2
        │
        ▼
[Prompt 1.2] Mapa Inicial → digita Aba 3 / Etapa 3
        │
        ▼
[Prompt 2.1] Geração de casos → digita Aba 4 / Etapa 4
        │
        ▼
[Prompt 2.2] HITL por caso → digita Aba 5 / Etapa 7
        │
        ▼
Filtro top-3 (score ≥ 3.0 + dono declarado)
        │
        ▼
[Ferramenta 1 · Prof / Prompt 3.1 SMART] Diagnóstico executivo por caso
        │
        ▼
[Ferramenta 2 · Prof / Prompt 3.2 SMART] Riscos e governança por caso
        │
        ▼
Digita business case → Aba 6 / Etapa 10 (app calcula ROI/Payback)
        │
        ▼
[Ferramenta 3 · Prof / Prompt 3.3 SMART] Priorização entre casos (se 2+)
        │
        ▼
[Prompt 3.4 SMART] Premortem do caso vencedor (uso interno)
        │
        ▼
[Ferramenta 4 · Prof / Prompt 3.5 SMART] Plano executivo → 1 pág para comitê
        │
        ▼
Registra decisão na Aba 6 / Etapa 10 → exporta PDF na Aba 7 / Etapa 11
```

---

## Referência bibliográfica

- **Bezerra, J.** — Curso de IA em Projetos, Programas e Portfólio · Aulas 1, 2 e 3 · BSBr (2026)
- Prompts SMART — template Situação · Mensagem · Alvo · Referência · Tipo
- **Klein, G.** — *Sources of Power* (premortem technique)
- **Bazerman, M.** — *Judgment in Managerial Decision Making* (7 vieses cognitivos)
