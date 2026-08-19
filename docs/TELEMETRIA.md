# Telemetria — Guia de Setup

Como conectar a coleta anônima ao Google Sheets do professor.

## 1. Criar service account no Google Cloud

1. Acessar https://console.cloud.google.com/iam-admin/serviceaccounts
2. Selecionar (ou criar) projeto → **Criar conta de serviço**
3. Nome sugerido: `mapa-ia-pppm-telemetria`
4. Pular concessão de papéis (não precisa)
5. Aba **Chaves** → **Adicionar chave** → **JSON** → baixar arquivo

## 2. Habilitar as APIs no projeto

- https://console.cloud.google.com/apis/library/sheets.googleapis.com → **Ativar**
- https://console.cloud.google.com/apis/library/drive.googleapis.com → **Ativar**

## 3. Criar a planilha

1. https://sheets.new na conta pessoal do professor
2. Nomear: `mapa-ia-pppm — telemetria`
3. **Compartilhar** com o `client_email` do JSON (permissão: Editor)
4. Copiar o `sheet_id` da URL (`docs.google.com/spreadsheets/d/{ESTE_ID}/edit`)

## 4. Configurar secrets

Criar `.streamlit/secrets.toml` na raiz do projeto:

```toml
[gcp_service_account]
type = "service_account"
project_id = "<do JSON>"
private_key_id = "<do JSON>"
private_key = """<do JSON — cole com aspas triplas para preservar quebras de linha>"""
client_email = "<do JSON>"
client_id = "<do JSON>"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "<do JSON>"
universe_domain = "googleapis.com"

[telemetria]
sheet_id = "<ID da planilha>"
worksheet = "exports"
```

**Nunca commitar** este arquivo. Já está no `.gitignore` (padrão Streamlit).

## 5. Inicializar a worksheet

```bash
.venv/bin/pip install toml  # só para o script
.venv/bin/python scripts/init_telemetria.py
```

Cria a aba `exports` com headers e freeze na linha 1.

## 6. Deploy no Streamlit Cloud

- Settings do app → **Secrets** → colar o mesmo conteúdo do `secrets.toml`
- Nenhum código muda; o app lê `st.secrets` transparentemente

## 7. Verificar

- Rodar o app local, gerar PDF ou exportar JSON
- Abrir a planilha — deve aparecer 1 linha nova
- Sessões subsequentes na mesma aba do navegador não geram nova linha (flag `_telemetria_enviada`)

## O que é coletado

| Campo | Origem | Anonimizado? |
|---|---|---|
| timestamp | servidor | — |
| session_id | uuid gerado no `init_state` | sim (não vinculável a pessoa) |
| trigger | `export_json` ou `gerar_pdf` | — |
| porte, n_projetos, pmo_ativo | contexto | — |
| diag_total, nivel, gargalo | derivado | — |
| n_casos, n_casos_prontos | derivado | — |
| payload_json | snapshot completo | **sim — sem nome/empresa/cargo/dono nominal** |

## O que NÃO é coletado

- Nome do aluno
- Nome da empresa
- Cargo/papel do aluno
- Nome do dono humano nos casos (só bool `tem_dono`)
- IP, user-agent, geolocalização

## Falha silenciosa

Se as credenciais estiverem ausentes, se o `gspread` não estiver instalado ou se a API falhar, o app **funciona normalmente** e o aluno não vê erro. Falhas caem em stderr do container Streamlit.

## Rollback

Remover a chamada `telemetria.enviar_uma_vez(...)` no `app.py` e o arquivo `src/telemetria.py`. Nenhum estado do aluno depende de telemetria.
