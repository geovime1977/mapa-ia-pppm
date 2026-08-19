"""Inicializa a worksheet de telemetria (headers + freeze).

Pré-requisitos:
1. Criar a Google Sheet manualmente na sua conta pessoal
2. Compartilhar a planilha com o client_email do service account (editor)
3. Preencher .streamlit/secrets.toml (ver docs/TELEMETRIA.md)
4. Rodar: .venv/bin/python scripts/init_telemetria.py

Idempotente: se os headers já existem, não sobrescreve.
"""

from __future__ import annotations

import sys
from pathlib import Path

import gspread
import toml
from google.oauth2.service_account import Credentials

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.telemetria import HEADERS

SECRETS = Path(__file__).resolve().parent.parent / ".streamlit" / "secrets.toml"


def main() -> int:
    if not SECRETS.exists():
        print(f"secrets.toml não encontrado em {SECRETS}", file=sys.stderr)
        return 1
    cfg = toml.loads(SECRETS.read_text(encoding="utf-8"))
    sa = cfg.get("gcp_service_account")
    tel = cfg.get("telemetria")
    if not sa or not tel:
        print("Faltam seções [gcp_service_account] ou [telemetria] em secrets.toml", file=sys.stderr)
        return 1
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(sa, scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(tel["sheet_id"])
    worksheet_name = tel.get("worksheet", "exports")

    try:
        ws = sh.worksheet(worksheet_name)
        print(f"Worksheet '{worksheet_name}' já existe.")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(worksheet_name, rows=1000, cols=len(HEADERS))
        print(f"Worksheet '{worksheet_name}' criada.")

    primeira = ws.row_values(1)
    if primeira == HEADERS:
        print("Headers já corretos, nada a fazer.")
        return 0
    if primeira:
        print(f"Aviso: linha 1 diferente do esperado ({primeira[:3]}...). Sobrescrevendo.")
    ws.update("A1", [HEADERS])
    ws.freeze(rows=1)
    print(f"Headers gravados: {len(HEADERS)} colunas. Freeze aplicado.")
    print(f"URL: https://docs.google.com/spreadsheets/d/{tel['sheet_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
