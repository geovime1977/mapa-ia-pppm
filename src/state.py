"""Estado da sessão Streamlit. Aluno mantém tudo em session_state; nada persistente
no servidor. Portabilidade via JSON (import_export.py)."""

from __future__ import annotations

import uuid

import streamlit as st

from src import data_loader


def _diagnostico_zerado() -> dict:
    return {d["id"]: 0 for d in data_loader.dimensoes()["dimensoes"]}


def _mapa_zerado() -> dict:
    return {b["id"]: "" for b in data_loader.dimensoes()["blocos_mapa"]}


_SCHEMA = {
    "contexto": {
        "nome": "",
        "empresa": "",
        "porte": "",
        "cargo": "",
        "n_projetos": 0,
        "pmo_ativo": False,
    },
    "diagnostico": None,  # preenchido em init_state() com _diagnostico_zerado()
    "mapa": None,         # idem
    "casos_uso": [],      # list[dict] — ver priorizacao.novo_caso()
    "governanca": {},     # dict[caso_id, dict] — ver governanca.estado_zerado()
    "contexto_salvo": False,
    "mapa_salvo": False,
}


def init_state() -> None:
    for chave, default in _SCHEMA.items():
        if chave not in st.session_state:
            if chave == "diagnostico":
                st.session_state[chave] = _diagnostico_zerado()
            elif chave == "mapa":
                st.session_state[chave] = _mapa_zerado()
            elif isinstance(default, (dict, list)):
                st.session_state[chave] = type(default)()
                if isinstance(default, dict):
                    st.session_state[chave].update(default)
                else:
                    st.session_state[chave].extend(default)
            else:
                st.session_state[chave] = default
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = uuid.uuid4().hex[:12]


def reset_state() -> None:
    for chave in _SCHEMA:
        st.session_state.pop(chave, None)
    init_state()


def get_all_data() -> dict:
    """Snapshot do estado — usado por PDF e export JSON."""
    return {
        "contexto": dict(st.session_state.get("contexto") or {}),
        "diagnostico": dict(st.session_state.get("diagnostico") or {}),
        "mapa": dict(st.session_state.get("mapa") or {}),
        "casos_uso": list(st.session_state.get("casos_uso") or []),
        "governanca": dict(st.session_state.get("governanca") or {}),
    }
