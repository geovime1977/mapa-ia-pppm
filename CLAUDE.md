# Diretiva de Contexto Global

Sempre consulte as configurações, comandos e subagentes definidos em `~/.claude/` antes de executar tarefas complexas.

---

# CLAUDE.md — mapa-ia-pppm

## Sobre este projeto

- **O que faz:** app Streamlit multi-aba que operacionaliza Aulas 1 e 2 do curso de IA em PPPM do Prof. Bezerra (BSBr). O aluno faz diagnóstico de maturidade (5 dims), Mapa Inicial (5 blocos), cadastra casos de uso com priorização ponderada (5 critérios), define governança HITL e exporta um Mapa Executivo em PDF.
- **Stack:** Python 3.11+ · Streamlit 1.61 · ReportLab 5.0 · pytest 9.1
- **Como rodar:** `.venv/bin/streamlit run app.py --server.port 8512`
- **Status:** ativo

## Localização

- **Local:** `~/projetos/mapa-ia-pppm/`
- **Backup:** `onedrive-eixoestrategico10:repos/mapa-ia-pppm`
- **GitHub:** `geovime1977/mapa-ia-pppm` (privado)
- **Nota no vault:** `01 - Profissional/Projetos/mapa-ia-pppm.md`
- **Porta:** 8512 (fora da faixa 8501-8511 já ocupada pelos apps irmãos)

## Comandos principais

```bash
# Instalar
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt

# Rodar
.venv/bin/streamlit run app.py --server.port 8512

# Testar
.venv/bin/python -m pytest tests/ -v

# Backup
rclone copy . onedrive-eixoestrategico10:repos/mapa-ia-pppm \
  --exclude ".venv/**" --exclude "__pycache__/**" --exclude ".git/**"
```

## Contexto relevante

- Trilogia PPPM: `diag-ia-pppm` (8511) · **`mapa-ia-pppm` (8512)** · `consultor-ia-pppm` (8509)
- Nada é persistido no servidor — session_state Streamlit. Portabilidade via export JSON.
- Corte obrigatório da Aula 2: caso sem dono humano declarado é bloqueado independente do score.
- Todo conteúdo pedagógico vive em `data/*.json` — mudar o JSON muda o app sem tocar em código.
