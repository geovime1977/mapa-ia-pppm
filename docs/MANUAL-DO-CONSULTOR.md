# Manual do Consultor — mapa-ia-pppm

Guia de uso completo dos apps `mapa-ia-pppm` como ferramenta de consultoria.
Baseado nas Aulas 1, 2 e 3 do curso de IA em PPPM do Prof. Bezerra (BSBr).

## Duas versões do mesmo app

O `mapa-ia-pppm` existe em duas versões que compartilham a mesma metodologia,
os mesmos cálculos e o mesmo PDF final. A escolha é logística:

| Aspecto | Streamlit | HTML standalone |
|---|---|---|
| URL | `https://mapa-ia-pppm.streamlit.app/` (público) ou `localhost:8513` | `index.html` local, abre no browser |
| Navegação | **7 abas** (topo) | **11 etapas** (wizard sequencial) |
| Requer internet | Sim (na versão hospedada) | Não — 100% offline após abrir |
| Instalação | Zero (URL) ou Python + Streamlit local | Zero — 1 arquivo HTML |
| Persistência | `session_state` (some ao fechar) | `session_state` (some ao fechar) |
| Import/Export JSON | Sim | Sim (schema compatível com Streamlit) |
| Distribuição para turma | Link para todos | E-mail ou OneDrive do `.html` |
| Público-alvo | Consultor com acesso à internet | Aluno / cliente em ambiente restrito |

**Regra:** use HTML quando o cliente tem restrição de rede (banco, órgão público,
site remoto), Streamlit quando você está apresentando ao vivo com projetor.

## Mapa de navegação — Streamlit × HTML

| Método (Aula) | Streamlit | HTML |
|---|---|---|
| Contexto do cliente | Aba 1 | Etapa 1 |
| Diagnóstico 5 dimensões | Aba 2 | Etapa 2 |
| Mapa Inicial 5 blocos | Aba 3 | Etapa 3 |
| Cadastro de casos de uso | Aba 4 | Etapa 4 |
| Avaliação por 5 critérios | Aba 4 | Etapa 5 |
| Matriz Impacto × Viabilidade | (integrada Aba 4) | Etapa 6 |
| Governança & HITL | Aba 5 | Etapa 7 |
| Seleção dos 3 prioritários | (implícita) | Etapa 8 |
| Recomendação executiva | (integrada exportação) | Etapa 9 |
| Business Case + ROI | Aba 6 | Etapa 10 |
| Exportar PDF | Aba 7 | Etapa 11 |

**Ao longo do manual usarei o nome do método** (ex: "Diagnóstico") **em vez de
aba/etapa**. Quando precisar apontar para um lugar específico do app, cito ambos
entre parênteses: *(Streamlit: Aba 2 · HTML: Etapa 2)*.

## O que este manual cobre

1. Como preencher cada uma das 11 etapas da metodologia
2. Regras dos cortes obrigatórios da Aula 2 e da Aula 3
3. Como o app calcula ROI, Payback e cenários
4. **Prompts SMART do consultor** (Aulas 1, 2 e 3) — quando, por que e como usar
5. Anexo com memória de cálculo detalhada

---

## 1. Contexto do cliente *(Streamlit: Aba 1 · HTML: Etapa 1)*

Sim, aqui vão os dados do **cliente**, não os seus. O objetivo é identificar
inequivocamente para quem esse mapa foi construído. Como esses campos entram
diretamente na capa do PDF exportado, escreva com o rigor que você quer que
apareça na entrega ao cliente.

| Campo | O que colocar | Exemplo |
|---|---|---|
| Nome do cliente | Nome do interlocutor principal (quem contratou / quem decidiu) | Camila Fernandes |
| Empresa / órgão | Razão social ou nome fantasia da organização | LogiSul Transportes |
| Cargo / papel | Cargo do interlocutor na organização | Gerente de PMO |
| Porte | Classificação padrão (MEI, PME, Média, Grande, Órgão público) | Média |
| Nº de projetos ativos | Quantos projetos rodam simultaneamente hoje | 12 |
| PMO ativo | Se já existe estrutura formal de PMO | ☐ ou ☑ |

**Por que isso importa:** o consultor que atende PME de 10 pessoas dá recomendação
completamente diferente do consultor que atende Grande empresa com CoE de IA. O
Contexto é o filtro que sustenta todas as recomendações que virão nas próximas
5 abas.

Botão **"Salvar contexto"** grava o marcador `contexto_salvo = True` na sessão
— serve como checkpoint visual, não é obrigatório para gerar o PDF.

---

## 2. Aba "Diagnóstico" — as 5 dimensões e a escala 0-3

Aula 1 · slides 26 e 27. Você pontua o cliente em cada uma das 5 dimensões
(nota 0 a 6). O app soma tudo e classifica em 1 dos 4 níveis de maturidade.

### O que cada dimensão significa

| Dimensão | Pergunta central que você faz ao cliente |
|---|---|
| **Estratégia e valor** | A IA está alinhada aos objetivos de negócio e à estratégia de portfólio? Alguém no C-level patrocina? |
| **Dados e processos** | Existem dados limpos, acessíveis e processos que sustentam a análise? Ou tudo mora em planilha isolada? |
| **Casos de uso** | Há casos concretos, com dor identificada e dono, rodando ou pilotados? Ou só ideia solta em reunião? |
| **Governança e HITL** | Existe validação humana, ética, rastreabilidade e controle sobre as decisões da IA? |
| **Benefícios e ROI** | O valor gerado é medido, comunicado e sustentado? Ou é intuitivo ("acho que está ajudando")? |

### Como pontuar 0 a 6

Não existe régua oficial slide-a-slide, mas na prática:

- **0** — inexistente. Nenhuma iniciativa nessa dimensão.
- **1-2** — reativo. Faz quando precisa, sem método.
- **3-4** — experimental. Alguns pilotos, sem escala.
- **5-6** — estruturado. Governança, métricas, escala consolidada.

Regra de bolso do consultor: se em dúvida entre duas notas, use a menor. Cliente
tende a superestimar sua própria maturidade e é papel seu ancorar o diagnóstico.

### Cálculo do total e classificação

O app soma automaticamente as 5 notas (total 0-30) e classifica em:

| Faixa | Nível | Rótulo | Significado |
|---|---|---|---|
| 0-5 | 0 | Inexistente | Nenhum uso estruturado de IA |
| 6-12 | 1 | Reativo | Uso pontual, sem método nem governança |
| 13-20 | 2 | Experimental | Pilotos isolados, aprendizado em curso |
| 21-30 | 3 | Estruturado | Governança, métricas e escala consolidadas |

### Gargalo prioritário

O app identifica automaticamente a dimensão com **menor nota** e destaca como
gargalo. Empate quebra pela ordem no JSON (Estratégia > Dados > Casos > Gov > ROI).

**É onde o cliente deveria investir primeiro para subir de nível.** Use como
gancho para o próximo bloco de consultoria: "seu gargalo está em Dados e
Processos, então nossa proposta começa por aí".

---

## 3. Aba "Mapa Inicial" — os 5 blocos da Aula 1 (slide 33)

Aqui o cliente descreve **um** projeto, processo ou área concreta. Não é uma
lista de tudo que ele quer fazer — é o Mapa daquele caso que vai virar piloto
prioritário. Se ele tem 3 candidatos, roda o app 3 vezes e exporta 3 mapas.

### O que cada bloco significa

| Bloco | Pergunta orientadora | Exemplo bom |
|---|---|---|
| **Contexto** | Qual projeto, processo ou área será analisado? | "Consolidação semanal do portfólio de 12 projetos ativos para o comitê executivo" |
| **Dor** | Qual problema real precisa ser resolvido? | "Consolidação consome 2 dias do PMO e chega ao comitê com atraso" |
| **Dados** | Que informações existem para apoiar a decisão? | "Status reports Jira, atas de comitê, plano de riscos, planilhas ROI" |
| **Riscos** | O que exige validação humana, ética ou segurança? | "Recomendação errada realoca CAPEX; dados sensíveis; comitê exige rastreabilidade" |
| **Valor** | Que benefício executivo pode ser gerado? | "Publicação D+1 aprovada pelo PMO em vez de D+3 hoje" |

### Regra de qualidade

Se o cliente responder um bloco em uma frase genérica ("melhorar processos" na
Dor, "todos os dados" em Dados), volte e refaça. Um Mapa Inicial de má
qualidade contamina todos os casos de uso da aba seguinte.

**Antipadrão frequente:** o cliente escreve na Dor a solução que ele já pensou
("preciso de um chatbot") em vez do problema. Insista: "qual é a dor que o
chatbot resolveria?".

---

## 4. Aba "Casos de Uso e Priorização" — o filtro executivo da Aula 2

Aqui é onde o mapa vira decisão. Cada caso é um piloto de IA candidato a
executar. O app pontua, ordena e bloqueia o que não tem dono.

### Por que aparece "5 erros a evitar antes de cadastrar seu caso"

Aula 2 · slides 8-12. São os erros clássicos que fazem projetos de IA falharem
no PMBOK real. **Ler antes de cadastrar** evita que o cliente proponha caso
óbvio-mas-errado:

1. **Começar pela ferramenta** — "qual IA?" é a pergunta errada; a certa é "qual dor?"
2. **Escolher pelo fascínio técnico** — caso chamativo nem sempre é estratégico
3. **Ignorar dados e processos** — sem dados confiáveis, IA recomenda com baixa precisão
4. **Confundir automação com decisão** — IA recomenda, humano decide
5. **Não medir valor nem risco** — sem métrica, o piloto vira opinião

### Por que existem "4 casos-exemplo da Empresa Alfa"

Aula 2 · slide 37. São casos canônicos que a apostila usa como referência:
relatório executivo automático, análise preditiva de atrasos, priorização de
portfólio, chatbot interno de metodologia. O cliente **copia o rótulo e adapta**
— acelera o cadastro e alinha vocabulário.

Não é obrigatório usar. É o "aqui está o que outras empresas fizeram, para você
não começar de zero".

### Sim, cada caso É uma tarefa/projeto/piloto da empresa

Um caso de uso não é um estudo abstrato — é um piloto concreto que vai ou não
para execução. Por isso o modelo pede **dono humano da decisão**: sem alguém
com nome que responda pela decisão, o caso não sai do PowerPoint.

### Como o ranking funciona

Cada caso recebe nota **1 a 5** em 5 critérios, com pesos fixos:

| Critério | Peso | O que significa |
|---|---|---|
| **Impacto no resultado** | 0.30 | Quanto melhora resultado, prazo, custo, qualidade, risco ou satisfação |
| **Viabilidade técnica** | 0.20 | Dá para implementar com tecnologia, orçamento, tempo e pessoas disponíveis |
| **Dados disponíveis** | 0.20 | Os dados existem, são acessíveis, confiáveis e suficientes |
| **Risco / segurança** | 0.15 | ⚠️ **INVERTIDO**: nota alta = risco BAIXO / bem controlado |
| **Valor potencial** | 0.15 | Benefício executivo demonstrável, mensurável e comunicável |

**Fórmula:** `score = Σ (nota × peso)` → resultado entre 1.0 e 5.0.

**Cuidado com o "Risco / segurança"** — se você pontuar 1 pensando "risco enorme",
o score cai (o oposto do que quer). Alto = risco baixo / bem controlado.

### As 3 faixas

| Score | Faixa | Cor | O que significa |
|---|---|---|---|
| `>= 4.0` | **Fazer agora** | 🟢 verde | Executa este trimestre |
| `>= 3.0` | **Preparar** | 🟡 âmbar | Vale resolver as pendências, planejar próximo trimestre |
| `< 3.0` | **Não priorizar** | 🔴 vermelho | Coloca no backlog frio |

### Os 4 quadrantes Impacto × Viabilidade (Aula 2 · slide 29)

Corte: nota ≥ 4 é "alto" nesse critério.

| | Viabilidade baixa (< 4) | Viabilidade alta (≥ 4) |
|---|---|---|
| **Impacto alto (≥ 4)** | 🔵 **Investigue** — não abandone, mas resolva a viabilidade antes | 🟢 **Comece aqui** — o ideal |
| **Impacto baixo (< 4)** | 🔴 **Evite agora** — não gasta bala com isso | ⚪ **Baixa prioridade** — fácil mas pouco vale, cuidado com viés de "começar pelo que é fácil" |

### Corte obrigatório: sem dono, não vai

Aula 2 · slide 30. Regra dura: se o campo **"Dono humano da decisão"** estiver
vazio, o caso é **bloqueado** e mostra ⛔ Não, independente do score.

Isso força o cliente a nomear pessoa. "A equipe" não conta. "O PMO" também não.
Precisa ser cargo ou nome de pessoa que responde por aquela decisão. É o filtro
anti-piloto-órfão — o principal motivo de piloto de IA morrer nas empresas.

---

## 5. Aba "Governança e HITL" — como classificar cada caso

Aula 2 · slides 32-36. Cada caso cadastrado na aba anterior aparece aqui para
receber sua camada de governança.

### Princípio de ouro

> "Quanto maior o impacto da decisão, maior deve ser a validação humana."
> Aula 2 · slide 33

### Como é feita a classificação HITL (automática)

O app deriva o **nível HITL** a partir da nota de impacto que você já deu na
aba 4. Zero trabalho extra:

| Nota de impacto | Nível HITL | Aprovador sugerido |
|---|---|---|
| 1-2 | **Leve** | PM ou analista |
| 3-4 | **Estruturada** | Especialista + PM |
| 5 | **Executiva** | Sponsor / comitê executivo |

Você não escolhe o nível manualmente — ele reflete a criticidade que você já
declarou na priorização.

### Como preencher os blocos de segurança (4 checkboxes)

Aula 2 · slide 32. Marque como coberto quando o cliente já tem a prática em pé.
Se não tem, deixe desmarcado — vai aparecer como pendência no PDF.

| Bloco | Marque quando... |
|---|---|
| **Dados sensíveis** | Existe política de classificação de informação; dados pessoais/proprietários estão identificados |
| **Acessos** | Está definido quem pode consultar, treinar, editar ou decidir com base na IA |
| **Ambiente seguro** | A ferramenta escolhida tem política de dados clara (ex: LLM enterprise, não conta grátis) |
| **Controle de uso** | Existe registro de finalidade, dono, permissões e limites do que a IA pode fazer |

### Como preencher rastreabilidade (5 campos)

Aula 2 · slide 34. Cada campo descreve **uma etapa do ciclo de decisão da IA**.
Preencha com o que o cliente realmente faz (ou vai fazer no piloto).

| Campo | O que descrever | Exemplo |
|---|---|---|
| **Entrada** | Que dados são usados como input | "Status reports Jira exportados semanalmente" |
| **Processamento** | Que modelo, prompt ou regra roda | "LLM Claude Sonnet com template estruturado" |
| **Saída** | Que artefato a IA gera | "Resumo executivo em Markdown + PDF" |
| **Validação** | Quem revisa e como | "PMO revisa em até 30min antes de publicar" |
| **Registro** | Onde a decisão fica arquivada | "Publicado no SharePoint com timestamp" |

Se algum campo ficar vazio, aparece como **pendência de rastreabilidade** no PDF.
Cobertura de 100% em ambos os grupos (segurança + rastreabilidade) + aprovador
declarado + decisão registrada = caso **pronto para produção**.

---

## 6. Aba "Exportar PDF" — o que sai

Sim, sai tudo detalhado. O PDF gerado é um dossiê executivo estruturado em 5
seções fixas + apêndice pedagógico:

### Estrutura do PDF

| Seção | Conteúdo | Vem de |
|---|---|---|
| **Capa** | Nome do cliente, empresa, porte, timestamp | Aba 1 |
| **1. Diagnóstico** | Leitura executiva + tabela 5 dimensões + total + nível + gargalo | Aba 2 |
| **2. Mapa Inicial** | 5 blocos (Contexto, Dor, Dados, Riscos, Valor) transcritos | Aba 3 |
| **3. Casos priorizados** | Tabela ranqueada por score, com faixa, quadrante, dono e pronto? | Aba 4 |
| **4. Governança e HITL** | Por caso: nível HITL, % segurança, % rastreabilidade, pronto para produção, lista de pendências | Aba 5 |
| **5. Referências pedagógicas** | Fixo: 5 erros a evitar + 4 casos-exemplo da Empresa Alfa | Aulas 2 |

O aluno leva tudo consolidado offline — pode imprimir, enviar por e-mail,
anexar em ata de reunião.

### Ver dados brutos

Abaixo do botão "Gerar PDF" tem expander **"Ver dados brutos (JSON)"** — mostra
o JSON completo do que será exportado. Útil para auditar antes de gerar o PDF
ou copiar para outro sistema.

---

## Perguntas úteis que aparecem depois

### Como salvar o progresso e continuar depois?

Sidebar → **"📥 Exportar JSON"** → salva o arquivo em qualquer lugar (Downloads,
Drive, e-mail). Em outra sessão, abre a URL do app, sidebar → **"Importar JSON"**
→ carrega o arquivo → continua exatamente de onde parou.

**Regra crítica:** o Streamlit Cloud **não persiste nada entre sessões**. Se
você fechar a aba sem exportar, o trabalho some.

### O app funciona em qualquer computador?

Sim. A URL `https://mapa-ia-pppm.streamlit.app/` é pública, sem login. Qualquer
navegador moderno funciona. **Detalhe:** app grátis do Streamlit Cloud hiberna
após ~7 dias sem acesso — a primeira pessoa a acessar depois disso espera ~30s
para o app acordar.

### Como demonstrar rápido para um cliente novo?

Sidebar → **"Exemplos prontos"** → 4 botões que carregam cenários completos com
1 clique:

- 🏭 **PME industrial · Nível 1** — cliente iniciante, dados em papel
- 🚚 **Logística · Nível 2** — média, PMO ativo, todos os quadrantes
- 🏦 **Banco · Nível 3** — grande, CoE de IA, HITL executivo
- 🏛️ **Prefeitura · Nível 2** — órgão público, LGPD + TCE

Serve para você projetar em reunião e mostrar como fica o PDF final antes do
cliente investir tempo preenchendo.

### E se eu rodar o app com dados sensíveis do cliente?

O app é 100% em `session_state` — nada é enviado para servidor de terceiro além
da própria hospedagem Streamlit Cloud. Se o cliente tem restrição forte, você
consegue rodar localmente sem custo:

```bash
git clone https://github.com/geovime1977/mapa-ia-pppm
cd mapa-ia-pppm
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py --server.port 8513
```

Roda em `localhost:8513`, offline após a instalação.

### Posso rodar o mesmo cliente com 3 pilotos diferentes?

Rode 3 vezes. Para cada piloto:
1. Reset → preenche Contexto (mesmo cliente, mesma empresa)
2. Preenche Mapa focado naquele piloto
3. Cadastra os casos relacionados
4. Exporta PDF nomeado `mapa-{cliente}-{piloto}.pdf`

Ou faça 1 rodada só, deixe o Mapa mais geral e cadastre os 3 pilotos como casos
distintos na aba 4. O ranking mostra qual dos 3 vale começar.

### Como usar isso em proposta comercial?

O PDF gerado é o **anexo de diagnóstico** da sua proposta. Sequência típica:

1. Reunião de discovery (30-45min) com o cliente
2. Você (consultor) preenche as 6 abas ao vivo, projetando a tela
3. Ao final, exporta PDF e envia junto com proposta comercial
4. Cliente vê valor demonstrado (não abstrato) e assina mais rápido

Isso é o padrão do funil consultivo: transformar discovery em proposta
assinada usando entrega tangível como âncora.

### Qual a diferença entre este app e o `consultor-ia-pppm`?

- **`mapa-ia-pppm`** (este) — foca nas Aulas 1 e 2, 1 sessão, ~30-45min por
  cliente, entrega o Mapa Executivo em PDF
- **`consultor-ia-pppm`** — cobre todas as aulas do curso do Prof. Bezerra;
  é o produto completo, indicado quando o cliente já quer engajamento longo

Use este quando o cliente é novo e você precisa entregar valor rápido.

### O que fazer quando o cliente resiste em nomear o "dono da decisão"?

Isso é diagnóstico em si. Se ninguém quer botar o nome, o piloto já está morto
antes de nascer — é o principal sinal de que a organização não está madura
para IA naquela dor. Duas saídas:

1. Sobe uma dimensão: leva a decisão para o sponsor do sponsor
2. Descarta o caso e marca no ranking como bloqueado — vira insight para o
   próprio cliente perceber a lacuna organizacional

Nunca preencha "PMO" ou "equipe" para satisfazer o app. Isso descaracteriza o
corte obrigatório e mata a utilidade do exercício.

---

## Referência rápida por aba

| Aba | Aula/Slide | O que produz | Tempo típico |
|---|---|---|---|
| 1. Contexto | (setup) | Capa do PDF | 2 min |
| 2. Diagnóstico | Aula 1 · slides 26-27 | Nível 0-3 + gargalo | 5 min |
| 3. Mapa Inicial | Aula 1 · slides 33, 35 | 5 blocos textuais | 10 min |
| 4. Casos de Uso | Aula 2 · slides 8-30, 37 | Ranking priorizado | 15 min |
| 5. Governança | Aula 2 · slides 32-36 | HITL + rastreabilidade | 10 min |
| 6. Business Case | Aula 3 · slides 9-19 | ROI + payback + decisão por caso | 15 min |
| 7. Exportar PDF | (saída) | Mapa Executivo em PDF | 1 min |
| **Total** | | | **~60 min** |

60min é o tempo típico de uma sessão de discovery + business case com cliente.
Se você só faz discovery, pode fechar em 45min pulando a aba 6. Se o cliente
já veio com dor mapeada, comece na aba 4 e feche em 30min.

Os 4 prompts executivos da Aula 3 (Ferramentas 1-4) e todos os prompts SMART
das Aulas 1 e 2 vivem agora no **Anexo do Consultor** — `docs/ANEXO-CONSULTOR.md`.
Uso interno; nunca acompanha o PDF do cliente.

---

## 8. Aba "Business Case" — a ponte da tese de valor até a decisão executiva

Aula 3 · slides 9-19. Aqui o consultor traduz o caso de uso priorizado da aba 4
em uma tese de valor com números, riscos e decisão. Um business case por caso —
todos herdam automaticamente o dono e o corte da Aula 2.

### O que vai em cada bloco

| Bloco | O que preencher | Fonte |
|---|---|---|
| Problema descrito | O que dói hoje. "Aprovação de crédito depende de análise manual e trava vendas." | Slide 9 |
| Linha de base | Valor atual do KPI. "SLA médio 4,2 dias · 480 análises/mês · custo R$ 62/análise." | Slide 9 |
| Caso de uso | Como a IA atua (entrada → processamento → saída), sem cair no fascínio técnico | Slide 10 |
| Dados | Quais dados a IA consome e como serão validados | Slide 10 |
| Benefícios · Financeiro | Perda atual × % redução → economia; + receita adicional; + custo evitado — em R$/ano | Slide 11 |
| Benefícios · Operacional | Horas economizadas/mês × pessoas × custo/hora | Slide 17 |
| Benefícios · Estratégico | Velocidade de decisão, stakeholders, governança (qualitativo) | Slide 19 |
| Custos (5 camadas) | Tecnologia · Dados · Pessoas · Mudança · Governança — cada um com valor + premissa | Slide 12 |
| Riscos | 4 riscos-padrão da aula, cada um em baixo/médio/alto + controle textual | Slide 13 |
| ROI e cenários | Janela 6/12/24 meses × cenário conservador (0.5) / provável (1.0) / otimista (1.3) | Slides 14-15 |
| Decisão solicitada | Aprovar piloto / Ajustar antes do piloto / Estudar melhor / Não recomendar neste momento | Slide 7 |

### Fórmula do ROI (mesma do slide 14)

`ROI = (Benefícios líquidos − Investimento) ÷ Investimento × 100`

- **Benefícios líquidos** = benefício financeiro anual + horas economizadas
  monetizadas, ajustado pela janela de análise e pelo cenário escolhido
- **Investimento** = soma das 5 camadas de custo
- **Cenário provável = 1.0**; conservador corta o benefício pela metade (0.5);
  otimista amplia em 30% (1.3)

### Auto-derivação da economia anual (v1.2)

Quando o aluno preenche **perda atual anual** (R$) **e** **% redução esperado** (0–100),
o app calcula automaticamente `economia_anual = perda × %/100` e sobrescreve o
campo manual. Se qualquer um dos dois estiver zero, o aluno mantém o número
digitado direto. A ideia é forçar o exercício mental "baseline × ganho esperado"
antes de aceitar um número final solto.

### Corte obrigatório novo da Aula 3

A decisão **"Aprovar piloto"** só é liberada quando **3 condições** valem juntas:

1. **Benefício líquido positivo** no cenário provável (BL > 0)
2. **Dono humano declarado** no caso (herdado da Aula 2)
3. **Controle textual preenchido** em todo risco marcado como "alto"

Se qualquer uma falha, o app deixa "Aprovar piloto" visível mas marcado como
bloqueado — o consultor tem que escolher "Ajustar antes do piloto", "Estudar
melhor" ou "Não recomendar neste momento". Isso é intencional: força o business
case a passar por um filtro antes de sair da sessão como recomendação de
investimento.

### Por que não tem método PO no cálculo

Decisão explícita do dono do projeto: o app não usa Monte Carlo, MILP, AHP nem
qualquer método de Pesquisa Operacional. Só a matemática direta do slide 14 do
Prof. Bezerra. Se o consultor precisa de análise probabilística mais fina,
usa uma ferramenta separada — este app cobre estritamente o escopo das
Aulas 1, 2 e 3.

---

## 9. Prompts do consultor — 9 prompts SMART para as 3 aulas

Os prompts foram retirados do app (não são mais uma aba/etapa) por 3 razões:

1. **Nunca eram executados pelo app** — só exibidos para copiar/colar em
   ChatGPT/Claude, sem estrutura SMART e sem prevenção contra vieses
2. **Não devem aparecer no PDF do cliente** — mostrar o prompt banaliza o
   entregável e revela método consultivo
3. **Precisavam de estrutura SMART** — o slide traz versões curtas; a
   consultoria real exige prevenção 80/20, critérios explícitos, formato
   de saída e checklist de vieses

Agora vivem aqui no manual (uso interno do consultor) e em `docs/ANEXO-CONSULTOR.md`
(versão mais detalhada com memória de cálculo).

**Regra de propriedade:** as versões SMART são diferencial competitivo do
consultor — não colar em canal público (Slack de cliente, e-mail sem NDA,
LinkedIn).

### Padrão SMART

Todos os prompts seguem **S · M · A · R · T**:

| Letra | Bloco | O que declara |
|---|---|---|
| **S** | Situação | Quem é você, onde está, o que faz |
| **M** | Mensagem | Ação exata da IA — verbo específico e escopo delimitado |
| **A** | Alvo | Público-alvo e objetivo final da resposta |
| **R** | Referência | Estilo, tom, framework ou exemplo a seguir |
| **T** | Tipo | Formato, tamanho, idioma e CTA da resposta |

Complementos de engenharia de prompt:
- **80/20** — 80% do prompt é prevenção; 20% é instrução
- **CoT 2026** — não pedir "pense passo a passo"; dar critérios explícitos
- **Reasoning ON** para análise/decisão; **OFF** para redação criativa

### Ordem cronológica de uso

```
Reunião cliente → [1.1] Diagnóstico → [1.2] Mapa Inicial
                → [2.1] Geração de casos → [2.2] HITL por caso
                → Filtro top-3
                → [3.1] Diagnóstico executivo (por caso)
                → [3.2] Riscos e governança (por caso)
                → App calcula ROI/Payback
                → [3.3] Priorização entre casos (se 2+)
                → [3.4] Premortem
                → [3.5] Plano executivo (1 página)
                → Comitê decide
```

---

### AULA 1 — Diagnóstico e Mapa Inicial

#### Prompt 1.1 — Entrevista estruturada de diagnóstico

- **QUANDO usar:** logo após a primeira reunião com o cliente
- **POR QUE usar:** força atribuição das notas 0-6 a evidência textual da
  entrevista — reduz viés de disponibilidade e ancoragem que aparecem quando
  o aluno pontua "no achismo"
- **COMO usar:** colar a transcrição ou respostas do questionário. Reasoning **ON**.
  Depois preenche direto no Diagnóstico *(Streamlit: Aba 2 · HTML: Etapa 2)*

```
S — Situação: Sou consultor aplicando o diagnóstico de
    maturidade em IA da Aula 1 do Prof. Bezerra (BSBr) em uma empresa de
    porte [PORTE] do setor [SETOR]. Terminei a primeira entrevista com o
    sponsor e tenho as notas abaixo.
M — Mensagem: Para CADA uma das 5 dimensões (Estratégia · Dados · Talento
    · Governança · Cultura), atribua nota 0-6 com JUSTIFICATIVA em 1 linha
    citando trecho literal da entrevista. Ao final, aponte a dimensão de
    MENOR nota como gargalo prioritário. NÃO invente evidência — se a
    entrevista não cobrir uma dimensão, escreva "sem evidência coletada,
    revisitar em entrevista 2". NÃO use jargão consultor genérico
    (transformação digital, jornada, unlock).
A — Alvo: Consultor (uso interno); objetivo é preencher o Diagnóstico
    com nota justificada por evidência.
R — Referência: Escala 0-6 do slide 26 (0-1 inicial · 2-3 desenvolvendo ·
    4-5 definido · 6 otimizado); vocabulário da Aula 1.
T — Tipo: Tabela Markdown 5 linhas × 3 colunas (Dimensão · Nota · Trecho
    literal); após a tabela, 1 parágrafo curto nomeando o gargalo. pt-BR.

Entrada: [colar transcrição da entrevista OU respostas ao questionário]
```

#### Prompt 1.2 — Mapa Inicial em 5 blocos

- **QUANDO usar:** depois do diagnóstico preenchido, antes de descrever o Mapa
- **POR QUE usar:** força blocos balanceados e uso do vocabulário da Aula 1;
  evita o vício de escrever "Contexto" longo e deixar "Riscos" vazio
- **COMO usar:** colar as notas 0-6 + trechos da entrevista. Reasoning **OFF**
  (é redação executiva; reasoning empobrece). Depois preenche no Mapa Inicial
  *(Streamlit: Aba 3 · HTML: Etapa 3)*

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

### AULA 2 — Casos de Uso, Priorização e Governança HITL

#### Prompt 2.1 — Geração de casos de uso a partir da dor

- **QUANDO usar:** quando o cliente identifica dor (Bloco 2 do Mapa) mas não
  sabe traduzir em caso de uso concreto
- **POR QUE usar:** evita o erro clássico do slide 8 da Aula 2 — pular direto
  para "vamos usar IA generativa" sem definir entrada, processamento e saída
- **COMO usar:** colar dor + gargalo do diagnóstico. Reasoning **ON**. Depois
  cadastra no CRUD *(Streamlit: Aba 4 · HTML: Etapa 4)*

```
S — Situação: O cliente tem a dor mensurável abaixo e o gargalo prioritário
    identificado no diagnóstico da Aula 1. Preciso gerar 3-5 casos de uso
    candidatos de IA para cadastrar no app mapa-ia-pppm.
M — Mensagem: Para cada caso, descreva: (1) rótulo curto (até 8 palavras),
    (2) dor específica endereçada, (3) fluxo entrada → processamento → saída
    em 1 linha, (4) dono humano da decisão (cargo, não nome), (5) dados
    necessários. NÃO gere caso que dependa de dado inexistente na empresa.
    NÃO proponha "chatbot genérico" ou "assistente virtual" — exija verbo
    de ação (classificar, priorizar, prever, resumir, alertar). NÃO ultra-
    passe 5 casos — melhor 3 casos densos que 5 rasos.
A — Alvo: Consultor; objetivo é ter 3-5 linhas prontas para digitar
    no CRUD de casos.
R — Referência: 7 domínios da Aula 2 (slides 16-22); princípio "IA no
    processo de decisão, não no lugar da decisão".
T — Tipo: Tabela Markdown 5 colunas (Rótulo · Dor · Fluxo · Dono · Dados);
    pt-BR.

Entrada:
- Dor mensurável: [colar]
- Gargalo prioritário: [colar]
- Setor/porte da empresa: [colar]
```

#### Prompt 2.2 — Definição de HITL por caso

- **QUANDO usar:** depois de cadastrar os casos, antes de definir governança
- **POR QUE usar:** aciona a regra "impacto ↑ = validação humana ↑"; evita
  o default preguiçoso de marcar todos como HITL "leve"
- **COMO usar:** colar lista de casos com dono e dor. Reasoning **ON**. Depois
  preenche na Governança *(Streamlit: Aba 5 · HTML: Etapa 7)*

```
S — Situação: Tenho N casos de uso cadastrados e preciso definir o nível de
    HITL (Human In The Loop) de cada um antes de preencher a Governança.
M — Mensagem: Para cada caso, classifique HITL em (a) LEVE — humano revisa
    amostragem periódica, (b) ESTRUTURADA — humano aprova cada saída antes
    de aplicar, (c) EXECUTIVA — humano decide, IA só recomenda. Para cada
    classificação, aponte: (1) motivo em 1 linha, (2) responsável nominal
    (cargo), (3) evidência de rastreabilidade obrigatória (log · ata · e-mail
    · sistema). NÃO classifique como LEVE qualquer caso que afete cliente
    final ou decisão financeira acima de R$ 10 mil. NÃO deixe caso sem
    responsável — se não há dono, marque "BLOQUEADO — sem dono humano".
A — Alvo: Consultor + sponsor; objetivo é passar no corte obrigatório
    da Aula 2 (slide 30).
R — Referência: 3 níveis de HITL da Aula 2 (slides 32-36); princípio de ouro
    "impacto ↑ = validação humana ↑".
T — Tipo: Tabela Markdown 5 colunas (Caso · HITL · Motivo · Responsável ·
    Rastreabilidade); pt-BR.

Entrada: [colar lista de casos com rótulo, dono e dor]
```

---

### AULA 3 — Business Case, ROI e Decisão do Comitê

#### Prompt 3.1 — Diagnóstico executivo (SMART)

- **QUANDO usar:** ANTES de escrever o business case
- **POR QUE usar:** o business case exige dor mensurável; sem prompt, o aluno
  escreve "processo lento" — sem número, sem fonte. Este força métrica e
  percorre as 5 etapas de decisão
- **COMO usar:** colar todo material disponível (entrevistas, KPIs, atas).
  Reasoning **ON**

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

#### Prompt 3.2 — Riscos e governança (SMART)

- **QUANDO usar:** DEPOIS de propor a solução, ANTES de estimar custos
- **POR QUE usar:** obriga a pressionar o caso pela ótica de risco antes de o
  sponsor assumir compromisso financeiro; aciona checklist de vieses
- **COMO usar:** colar descrição do caso + dados envolvidos. Reasoning **ON**

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

#### Prompt 3.3 — Priorização entre casos (SMART)

- **QUANDO usar:** quando há 2+ casos e é preciso escolher por onde começar
- **POR QUE usar:** o app calcula ROI/Payback determinístico, mas não faz
  comparação qualitativa nem checa premissas — este prompt cobre a lacuna
- **COMO usar:** colar lista de casos com ROI já calculado pelo app.
  Reasoning **ON**

```
S — Situação: Tenho 2+ casos de uso candidatos e preciso recomendar por
    onde começar antes de gastar orçamento de piloto (Aula 3 · Ferramenta
    3). O app já calcula ROI/Payback — este prompt NÃO recalcula, apenas
    compara qualitativamente e checa premissas.
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

#### Prompt 3.4 — Premortem (SMART, adição fora do slide)

- **QUANDO usar:** DEPOIS de decidir "por onde começar", ANTES do plano executivo
- **POR QUE usar:** força imaginar o fracasso ANTES de vender o sucesso;
  combate direto ao excesso de confiança
- **COMO usar:** colar caso recomendado + business case. Reasoning **ON**.
- **Aviso:** NÃO consta na Aula 3 do Prof. É adição do consultor baseada em
  Gary Klein (*Sources of Power*). Diferencial — não colocar no PDF do cliente

```
S — Situação: Já decidi qual caso vai virar piloto e o business case está
    completo no app. ANTES de escrever o plano executivo para o comitê,
    preciso rodar um premortem para pressionar a decisão.
M — Mensagem: Escreva o cenário: "Seis meses depois do go-live, o piloto
    foi cancelado com prejuízo." Liste (1) as 5 causas mais prováveis do
    fracasso em ordem de probabilidade, (2) para cada causa, o SINAL
    ANTECIPADO que o comitê poderia ter visto na semana 2, (3) para cada
    causa, o ajuste no escopo do piloto que preveniria. NÃO minimize
    causas com "gestão de mudança" ou "comunicação insuficiente" — esses
    são sintomas, não causas. NÃO cite falha de tecnologia genérica —
    aponte qual componente específico falha.
A — Alvo: Consultor (uso interno); objetivo é ajustar o plano
    executivo antes de submeter ao comitê.
R — Referência: Técnica de premortem de Gary Klein; regra 5 de reparos
    cognitivos (`~/.claude/rules/processos-decisorios.md`).
T — Tipo: Tabela Markdown 3 colunas (Causa · Sinal semana 2 · Ajuste
    preventivo); pt-BR; exatamente 5 linhas.

Entrada: [colar caso recomendado + business case completo do app]
```

#### Prompt 3.5 — Plano executivo de 1 página (SMART)

- **QUANDO usar:** DEPOIS do premortem, para gerar a peça final que vai ao comitê
- **POR QUE usar:** o comitê decide em 90 segundos; sem prompt, o aluno entrega
  3 páginas de contexto e 1 parágrafo de decisão — este inverte
- **COMO usar:** colar business case + resultado do premortem. Reasoning **OFF**

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

### Versões literais dos 4 prompts do Prof. Bezerra

Preserva a fidelidade pedagógica quando você estiver **ensinando** a metodologia
(vs. **aplicando** em consultoria real). Para consultoria real, prefira as
versões SMART acima.

- **Ferramenta 1 · Diagnóstico executivo:** *"Atue como consultor sênior em
  PPPM. Com base nas informações abaixo, identifique: 1) problema central;
  2) causas prováveis; 3) indicadores afetados; 4) impacto financeiro ou
  operacional; 5) hipótese de caso de uso de IA; 6) dados necessários para
  validar a hipótese. Responda em formato executivo."*
- **Ferramenta 2 · Riscos e governança:** *"Avalie o caso de uso de IA
  descrito abaixo sob a ótica de riscos, ética, dados, segurança e governança.
  Classifique os riscos em baixo, médio e alto. Indique controles mínimos,
  ponto de intervenção humana, responsáveis, evidências de rastreabilidade
  e critérios para interromper o piloto."*
- **Ferramenta 3 · Priorização e ROI:** *"Compare os casos de uso abaixo
  usando os critérios: impacto, viabilidade, dados, risco e valor. Atribua
  notas de 1 a 5, explique cada nota, estime benefício, custo, ROI e payback
  quando houver dados suficientes. Ao final, recomende onde começar e quais
  premissas precisam ser validadas no piloto."*
- **Ferramenta 4 · Plano executivo:** *"Com base neste business case
  preliminar, produza uma recomendação executiva de até uma página contendo:
  problema, solução de IA, benefícios esperados, investimento, ROI estimado,
  riscos, governança, cronograma do piloto, responsáveis, indicadores e
  decisão solicitada ao comitê."*

---

## 10. Como a Aula 3 muda o PDF final

Antes da Aula 3, o PDF tinha 6 seções: contexto, diagnóstico, mapa, casos,
governança, recomendação (+ apêndice pedagógico). Com a Aula 3, o PDF ganha
uma seção nova antes da recomendação:

**Seção 5 — Business Cases preliminares** — 1 subseção por caso com business
case preenchido. Cada subseção traz:

- Tabela com 9 blocos (problema, linha de base, caso de uso, dados, investimento,
  benefício bruto/ano, cenário provável com BL e ROI, payback, decisão solicitada)
- Tabela cenários (conservador/provável/otimista) com BL, ROI% e payback
- Se a decisão "Aprovar piloto" está marcada mas não passa nos cortes, o PDF
  destaca as pendências abertas — o comitê vê a inconsistência

Se nenhum caso tem business case preenchido, a seção 5 simplesmente não aparece
no PDF — não polui a entrega quando o consultor rodou só as Aulas 1-2.
