# mapa-ia-pppm — Guia técnico

Segundo app da trilogia PPPM (Prof. Bezerra, BSBr). Operacionaliza Aula 1
(diagnóstico + Mapa Inicial) e Aula 2 (5 erros, 7 domínios, priorização,
governança HITL). Determinístico, zero LLM, zero I/O de rede.

## Arquitetura

```
mapa-ia-pppm/
├── app.py                 # Streamlit multi-aba (entry point)
├── data/                  # JSONs estáticos da aula (fonte da verdade)
│   ├── dimensoes.json          # 5 dims diagnóstico + 5 blocos mapa
│   ├── niveis.json             # 4 níveis de maturidade (0-3)
│   ├── criterios_priorizacao.json  # 5 critérios + faixas + quadrantes
│   ├── governanca.json         # blocos segurança, rastreabilidade, HITL
│   └── exemplos_aulas.json     # 5 erros, 7 domínios, casos Alfa
├── src/
│   ├── data_loader.py     # loaders JSON com lru_cache
│   ├── state.py           # session_state Streamlit
│   ├── diagnostico.py     # total, nível, gargalo, leitura executiva
│   ├── priorizacao.py     # CRUD casos, score, corte obrigatório, quadrante
│   ├── governanca.py      # estado zerado, HITL, coberturas, prontidão
│   ├── import_export.py   # dump/load JSON versionado
│   └── pdf.py             # ReportLab platypus → PDF consolidado
└── tests/                 # pytest — 39 casos, 100% verde
```

**Fluxo:** `data/*.json → data_loader → módulos de domínio → app.py`

Regra: nenhum arquivo em `src/` faz I/O de rede. Toda persistência é responsabilidade
do usuário (exportar JSON) — o servidor não guarda nada entre sessões.

## Stack

| Camada | Escolha |
|---|---|
| UI | Streamlit 1.61 |
| PDF | ReportLab 5.0 (platypus) |
| Dados | JSON no repo, `functools.lru_cache` no loader |
| Testes | pytest 9.1 |
| Python | 3.11+ (testado em 3.14) |

## Rodar localmente

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/streamlit run app.py --server.port 8512
```

Health check: `curl http://localhost:8512/_stcore/health` → `ok`.

## Rodar testes

```bash
.venv/bin/python -m pytest tests/ -v
```

## Convenções

- **Porta única do ecossistema:** 8512 (fora da faixa 8501-8511 já ocupada pelos apps irmãos do Geovane)
- **Nenhum comentário sobre "o quê" o código faz** — só sobre "por quê", quando não óbvio
- **Sem error handling defensivo** — só validação em fronteiras (upload JSON, entrada do usuário)
- **Referências à aula** ficam nos JSONs em `data/`, campo `referencia`

## Como estender

### Adicionar uma dimensão nova ao diagnóstico
1. Acrescente o item em `data/dimensoes.json` → `dimensoes[]` com `id`, `rotulo`, `descricao`, `referencia`
2. Ajuste o slider max em `app.py` se quiser mudar de 0-6
3. Ajuste as faixas em `data/niveis.json` se o total mudar
4. `.venv/bin/python -m pytest` — os testes de gargalo devem seguir passando

### Adicionar um critério de priorização
1. Novo item em `data/criterios_priorizacao.json` → `criterios[]` com `id`, `peso`
2. **Soma dos pesos precisa ser 1.0** — quebre outros pesos proporcionalmente
3. `test_score_com_notas_5_da_5` valida a soma implícita

### Trocar o layout do PDF
Toda a montagem está em `src/pdf.py`. Editar `_capa`, `_secao_diagnostico`,
`_secao_mapa`, `_secao_casos`, `_secao_governanca` de forma independente.
`test_gera_pdf_com_estado_completo` valida bytes válidos após mudanças.

## Deploy

Segue a rotina padrão do Geovane (ver `~/.claude/rules/projetos.md`):

```bash
# GitHub
gh repo create geovime1977/mapa-ia-pppm --private --source=. --push

# OneDrive
rclone copy ~/projetos/mapa-ia-pppm onedrive-eixoestrategico10:repos/mapa-ia-pppm \
  --exclude ".venv/**" --exclude "__pycache__/**" --exclude ".git/**"
```

## Trilogia PPPM (contexto)

| App | Porta | Escopo |
|---|---|---|
| diag-ia-pppm | 8511 | Diagnóstico 5D + Mapa 5 Blocos + 3 pilotos + PDF (Aula 1 completa) |
| **mapa-ia-pppm** | **8512** | **Diagnóstico + Mapa + Priorização + Governança HITL (Aulas 1+2)** |
| consultor-ia-pppm | 8509 | Consultor completo do curso (todas as aulas) |

Este app foca no aluno individual construindo seu Mapa Executivo em uma única sessão.
