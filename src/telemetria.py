"""Telemetria anônima para benchmark do professor.

Envia uma linha por sessão para uma Google Sheet privada quando o aluno
finaliza (exporta JSON ou gera PDF). Falha silenciosa: se credencial ausente
ou API off, o aluno não vê erro nenhum.

LGPD: dados identificáveis (nome, empresa, cargo, dono nominal) são removidos
antes do envio. O que sobe: porte, contadores, notas, textos livres do mapa
e casos, cobertura de governança.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any

import streamlit as st

from src import diagnostico, governanca as gov_mod, priorizacao

_CAMPOS_IDENTIFICAVEIS_CONTEXTO = ("nome", "empresa", "cargo")

HEADERS = [
    "timestamp",
    "session_id",
    "trigger",
    "porte",
    "n_projetos",
    "pmo_ativo",
    "diag_total",
    "diag_nivel",
    "diag_gargalo",
    "n_casos",
    "n_casos_prontos",
    "payload_json",
]


def anonimizar(estado: dict) -> dict:
    """Remove qualquer campo identificável do snapshot antes de subir."""
    ctx = dict(estado.get("contexto") or {})
    for campo in _CAMPOS_IDENTIFICAVEIS_CONTEXTO:
        ctx.pop(campo, None)

    casos_anon = []
    for c in (estado.get("casos_uso") or []):
        casos_anon.append({
            "id": c.get("id"),
            "rotulo": c.get("rotulo", ""),
            "descricao": c.get("descricao", ""),
            "dor": c.get("dor", ""),
            "tem_dono": bool((c.get("dono") or "").strip()),
            "notas": dict(c.get("notas") or {}),
        })

    gov_anon = {}
    for cid, g in (estado.get("governanca") or {}).items():
        gov_anon[cid] = {
            "cobertura_seguranca": sum(1 for v in (g.get("seguranca") or {}).values() if v),
            "total_seguranca": len(g.get("seguranca") or {}),
            "cobertura_rastreabilidade": sum(1 for v in (g.get("rastreabilidade") or {}).values() if str(v).strip()),
            "total_rastreabilidade": len(g.get("rastreabilidade") or {}),
            "tem_aprovador": bool((g.get("aprovador") or "").strip()),
            "decisao_registrada": bool(g.get("decisao_registrada", False)),
        }

    return {
        "contexto": ctx,
        "diagnostico": dict(estado.get("diagnostico") or {}),
        "mapa": dict(estado.get("mapa") or {}),
        "casos_uso": casos_anon,
        "governanca": gov_anon,
    }


def _resumo_escalar(estado_anon: dict) -> dict:
    diag = estado_anon.get("diagnostico") or {}
    casos = estado_anon.get("casos_uso") or []
    total = diagnostico.total_maturidade(diag)
    nivel = diagnostico.nivel_por_total(total)
    gargalo = diagnostico.identificar_gargalo(diag)
    prontos = 0
    for c in casos:
        caso_check = {"dono": "x" if c.get("tem_dono") else ""}
        ok, _ = priorizacao.pronto_para_executar(caso_check)
        if ok:
            prontos += 1
    ctx = estado_anon.get("contexto") or {}
    return {
        "porte": ctx.get("porte", ""),
        "n_projetos": int(ctx.get("n_projetos", 0) or 0),
        "pmo_ativo": bool(ctx.get("pmo_ativo", False)),
        "diag_total": total,
        "diag_nivel": f"{nivel['numero']} — {nivel['rotulo']}",
        "diag_gargalo": gargalo["rotulo"],
        "n_casos": len(casos),
        "n_casos_prontos": prontos,
    }


def _worksheet():
    """Retorna a worksheet do Sheets. None se credenciais ausentes."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        return None
    try:
        cfg = st.secrets["gcp_service_account"]
        tel = st.secrets["telemetria"]
    except Exception:
        return None
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(dict(cfg), scopes=scopes)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(tel["sheet_id"])
    return sh.worksheet(tel.get("worksheet", "exports"))


def enviar(estado: dict, session_id: str, trigger: str) -> bool:
    """Envia snapshot anonimizado. Retorna True se enviado, False se skip/falha.
    Nunca levanta exceção — telemetria falhando não pode quebrar o app."""
    try:
        ws = _worksheet()
        if ws is None:
            return False
        anon = anonimizar(estado)
        resumo = _resumo_escalar(anon)
        linha: list[Any] = [
            datetime.now().isoformat(timespec="seconds"),
            session_id,
            trigger,
            resumo["porte"],
            resumo["n_projetos"],
            resumo["pmo_ativo"],
            resumo["diag_total"],
            resumo["diag_nivel"],
            resumo["diag_gargalo"],
            resumo["n_casos"],
            resumo["n_casos_prontos"],
            json.dumps(anon, ensure_ascii=False),
        ]
        ws.append_row(linha, value_input_option="USER_ENTERED")
        return True
    except Exception as exc:
        print(f"[telemetria] falha silenciosa: {exc}", file=sys.stderr)
        return False


def enviar_uma_vez(estado: dict, trigger: str) -> None:
    """Envia no máximo uma vez por sessão. Idempotente."""
    if st.session_state.get("_telemetria_enviada"):
        return
    session_id = st.session_state.get("session_id", "sem-id")
    if enviar(estado, session_id, trigger):
        st.session_state["_telemetria_enviada"] = True
