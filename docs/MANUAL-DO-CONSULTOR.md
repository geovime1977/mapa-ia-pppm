# Manual do Consultor — mapa-ia-pppm

Guia de uso completo do app https://mapa-ia-pppm.streamlit.app/ como ferramenta
de consultoria. Baseado nas Aulas 1 e 2 do curso de IA em PPPM do Prof. Bezerra
(BSBr).

Este manual responde às 6 perguntas mais comuns do consultor que começa a usar
o app com um cliente, e acrescenta outras que aparecem depois da segunda ou
terceira sessão.

---

## 1. Aba "Contexto" — o que preencher

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

Isso é o funil Fase 2 do modelo Eixo Estratégico: transformar discovery em
proposta assinada usando entrega tangível como âncora.

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
| 6. Exportar PDF | (saída) | Mapa Executivo em PDF | 1 min |
| **Total** | | | **~45 min** |

45min é o tempo típico de uma sessão de discovery com cliente. O app foi
desenhado para caber nessa janela.
