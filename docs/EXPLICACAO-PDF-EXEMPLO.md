# Explicação do PDF de exemplo — mapa-ia-pppm

Documento que descreve cada seção do PDF gerado por `output/mapa-exemplo.pdf`,
peça por peça, para o aluno entender o que está lendo e o que teria acontecido
se tivesse preenchido diferente.

---

## Capa

- **Aluno / Empresa / Porte** — vêm da aba 1 (Contexto). São só rótulos que
  identificam o Mapa. Não afetam nenhum cálculo.
- **Data de geração** — timestamp do momento em que o botão "Gerar PDF" foi
  clicado.
- **Rodapé** — referência à Aula 1 e 2 do Prof. Bezerra (BSBr). Cabeçalho
  fixo do produto pedagógico.

---

## 1. Diagnóstico de maturidade

**De onde vem:** aba 2 (Diagnóstico). O aluno pontuou de 0 a 6 cada uma das 5
dimensões da Aula 1 (slide 27):

| Dimensão | Pergunta central |
|---|---|
| Estratégia e valor | IA está alinhada à estratégia? |
| Dados e processos | Há dados limpos e processo sólido? |
| Casos de uso | Há casos concretos com dor e dono? |
| Governança e HITL | Existe validação humana e rastreabilidade? |
| Benefícios e ROI | O valor é medido e comunicado? |

**Leitura executiva no topo:** frase única que combina total, nível e gargalo.
É o TL;DR do diagnóstico.

**Tabela:** as 5 notas + o total 0-30 + o nível derivado (0-3):

| Faixa | Nível | Nome |
|---|---|---|
| 0-5 | 0 | Inexistente |
| 6-12 | 1 | Reativo |
| 13-20 | 2 | Experimental |
| 21-30 | 3 | Estruturado |

**Gargalo prioritário:** dimensão com **menor nota**. Empate quebra pela
ordem do JSON (estratégia primeiro, depois dados, casos, governança, ROI).
É onde o aluno deveria investir primeiro para subir de nível.

*No exemplo:* total 14/30 → Nível 2 (Experimental); gargalo em "Dados e
processos" com nota 2.

---

## 2. Mapa Inicial (5 blocos)

**De onde vem:** aba 3 (Mapa Inicial). O aluno responde 5 perguntas da Aula 1
(slide 33) sobre um projeto ou processo real seu:

| Bloco | Pergunta |
|---|---|
| Contexto | Qual projeto, processo ou área será analisado? |
| Dor | Qual problema real precisa ser resolvido? |
| Dados | Que informações existem para apoiar a decisão? |
| Riscos | O que exige validação humana, ética ou segurança? |
| Valor | Que benefício executivo pode ser gerado? |

Bloco não preenchido aparece como *"não preenchido"* em itálico. Sem
cálculo, é o entregável textual da Aula 1 (slide 35).

---

## 3. Casos de uso priorizados

**De onde vem:** aba 4 (Casos de Uso). Cada caso recebeu notas 1-5 em 5
critérios com pesos fixos:

| Critério | Peso |
|---|---|
| Impacto no resultado | 0.30 |
| Viabilidade técnica | 0.20 |
| Dados disponíveis | 0.20 |
| Risco / segurança (alto = risco baixo) | 0.15 |
| Valor potencial | 0.15 |

**Cálculo:** `score = Σ (nota × peso)` — resultado entre 1.0 e 5.0.

**Faixa:**
- `>= 4.0` → **Fazer agora** (verde)
- `>= 3.0` → **Preparar** (âmbar)
- `< 3.0` → **Não priorizar** (vermelho)

**Quadrante Impacto × Viabilidade** (Aula 2 slide 29):
- Impacto ≥ 4 e Viabilidade ≥ 4 → **Comece aqui**
- Impacto ≥ 4 e Viabilidade < 4 → **Investigue**
- Impacto < 4 e Viabilidade ≥ 4 → **Baixa prioridade**
- Impacto < 4 e Viabilidade < 4 → **Evite agora**

**Pronto (Sim/Não):** só depende do campo **Dono humano da decisão**. Sem
dono declarado, é **Não** — independente do score.

**Ordenação:** score decrescente; empate pelo rótulo alfabético.

### Por que aparece "Caso bloqueado"?

Abaixo da tabela aparece a frase *"N caso(s) bloqueado(s) pelo corte
obrigatório (sem dono humano declarado)"* quando pelo menos um caso está
sem dono.

**Isso não é bug.** É a **regra dura** da Aula 2, slide 30: um caso pode ter
score altíssimo, mas se ninguém foi nomeado como responsável pela decisão,
ele **não vai para produção**. O app implementa o corte como regra do jogo.

*No PDF de exemplo:* o terceiro caso ("Chatbot interno de metodologia")
está sem dono **de propósito**, para demonstrar visualmente o corte
funcionando. Basta preencher o campo Dono na aba 4 para desbloquear.

---

## 4. Governança e HITL

**De onde vem:** aba 5 (Governança). Para cada caso, o aluno definiu:

- Quais **blocos de segurança** estão cobertos (dados sensíveis, acessos,
  ambiente seguro, controle de uso)
- Quais campos de **rastreabilidade** estão preenchidos (entrada,
  processamento, saída, validação, registro — Aula 2 slide 34)
- Quem é o **aprovador HITL** (nome ou papel)
- Se a **decisão foi registrada** em ata/e-mail/sistema

**Nível HITL** (derivado automaticamente da nota de impacto do caso):
- Impacto 1-2 → **Leve** (PM ou analista)
- Impacto 3-4 → **Estruturada** (Especialista + PM)
- Impacto 5   → **Executiva** (Sponsor / comitê)

**Princípio de ouro:** quanto maior o impacto da decisão, maior a
validação humana (Aula 2 slide 33).

**Métricas mostradas por caso:**
- Cobertura de Segurança (% dos 4 blocos marcados)
- Cobertura de Rastreabilidade (% dos 5 campos preenchidos)
- Pronto para produção (Sim se: tem dono + segurança 100% + rastreabilidade
  100% + aprovador declarado + decisão registrada)

**Pendências** listadas ao lado quando algo falta.

---

## 5. Referências pedagógicas (Aula 2)

Apêndice fixo que **não depende dos dados do aluno**. Aparece igual em todo
PDF gerado. Serve como material de bolso offline.

### 5.1 Cinco erros a evitar (Aula 2 slides 8-12)
1. **Começar pela ferramenta** — "Qual IA?" é a pergunta errada; a certa é
   "Qual dor?"
2. **Escolher pelo fascínio técnico** — casos chamativos nem sempre são
   estratégicos
3. **Ignorar dados e processos** — sem dados confiáveis, IA recomenda com
   baixa precisão
4. **Confundir automação com decisão** — IA recomenda, humano decide
5. **Não medir valor nem risco** — sem métricas o piloto vira opinião

### 5.2 Casos-exemplo da Empresa Alfa (slide 37)
Quatro casos canônicos de referência: relatório executivo automático,
análise preditiva de atrasos, priorização de portfólio, chatbot interno de
metodologia. Cada um listado com Dor / Dados / Decisão / Valor para o
aluno usar como inspiração ao cadastrar casos próprios.

---

## Como regenerar

Depois de alterar qualquer campo em qualquer aba, basta ir na aba 6
(Exportar PDF) e clicar **Gerar PDF**. A regeneração é instantânea e não
depende de rede.

Para reproduzir o PDF de exemplo exatamente como está:
```bash
.venv/bin/python /tmp/gerar_exemplo_mapa.py
```
Saída em `output/mapa-exemplo.pdf`.
