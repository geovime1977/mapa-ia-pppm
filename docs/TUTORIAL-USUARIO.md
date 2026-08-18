# Mapa IA em PPPM — Guia do aluno

App do curso do Prof. Bezerra (BSBr). Você usa como ferramenta de aula para
diagnosticar sua maturidade em IA aplicada a projetos, programas e portfólio (PPPM),
desenhar o Mapa Inicial e priorizar casos de uso com governança.

## O que este app faz

Em 6 abas você monta seu **Mapa Executivo de IA em PPPM**:

1. **Contexto** — quem é você, empresa, porte, cargo
2. **Diagnóstico** — pontua de 0 a 6 as 5 dimensões da Aula 1; recebe seu nível (0-3) e o gargalo prioritário
3. **Mapa Inicial** — responde os 5 blocos da Aula 1 (Contexto, Dor, Dados, Riscos, Valor) sobre um caso real seu
4. **Casos de Uso** — cadastra pilotos de IA, pontua nos 5 critérios da Aula 2 e vê o ranking com faixa (Fazer agora / Preparar / Não priorizar) e quadrante Impacto × Viabilidade
5. **Governança** — define nível HITL por caso, marca blocos de segurança e rastreabilidade
6. **Exportar PDF** — baixa o Mapa consolidado

Tudo fica no seu navegador (session_state). Nada é enviado ao servidor.

## Como instalar

1. Peça o pacote ao Geovane ou clone do GitHub `geovime1977/mapa-ia-pppm`
2. Instale Python 3.11+
3. No terminal, dentro da pasta do projeto:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

## Como usar

```bash
.venv/bin/streamlit run app.py --server.port 8513
```

Abre no navegador em `http://localhost:8513`. Percorra as abas na ordem.

**Dica:** no fim, use "Exportar JSON" na barra lateral para salvar seu progresso.
Da próxima vez, "Importar JSON" reconstrói tudo.

## Regra que trava o piloto: sem dono, não vai

Um caso de uso só é considerado **pronto para executar** se você declarar
explicitamente o **dono humano da decisão**. Score alto sem dono = bloqueado.
Isso é o "corte obrigatório" da Aula 2 (slide 30).

## Se der erro

- **Porta 8513 ocupada:** troque com `--server.port 8514`
- **PDF não gera:** cheque se preencheu ao menos Contexto e Diagnóstico
- **JSON importado não carrega:** confirme que foi exportado por este app
