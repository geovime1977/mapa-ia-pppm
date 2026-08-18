"""Portabilidade JSON do session_state — importar/exportar o Mapa completo do aluno."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

VERSAO = "1.0"


def exportar(estado: dict) -> str:
    """Serializa o estado como JSON UTF-8 indentado."""
    payload: dict[str, Any] = {
        "app": "mapa-ia-pppm",
        "versao": VERSAO,
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        "dados": {
            "contexto": estado.get("contexto") or {},
            "diagnostico": estado.get("diagnostico") or {},
            "mapa": estado.get("mapa") or {},
            "casos_uso": estado.get("casos_uso") or [],
            "governanca": estado.get("governanca") or {},
        },
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def importar(conteudo: str | bytes) -> dict:
    """Lê JSON e devolve o bloco 'dados' pronto para hidratar session_state.
    Aceita payloads sem envelope (dados diretos)."""
    if isinstance(conteudo, bytes):
        conteudo = conteudo.decode("utf-8")
    payload = json.loads(conteudo)
    if isinstance(payload, dict) and "dados" in payload:
        dados = payload["dados"]
    else:
        dados = payload
    return {
        "contexto": dict(dados.get("contexto") or {}),
        "diagnostico": dict(dados.get("diagnostico") or {}),
        "mapa": dict(dados.get("mapa") or {}),
        "casos_uso": list(dados.get("casos_uso") or []),
        "governanca": dict(dados.get("governanca") or {}),
    }
