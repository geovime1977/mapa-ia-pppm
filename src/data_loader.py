"""Loaders JSON dos dados estáticos das aulas. Zero I/O de rede."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def _ler(nome: str) -> dict | list:
    with open(_DATA_DIR / nome, encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def niveis() -> dict:
    return _ler("niveis.json")


@lru_cache(maxsize=1)
def dimensoes() -> dict:
    return _ler("dimensoes.json")


@lru_cache(maxsize=1)
def criterios() -> dict:
    return _ler("criterios_priorizacao.json")


@lru_cache(maxsize=1)
def exemplos() -> dict:
    return _ler("exemplos_aulas.json")


@lru_cache(maxsize=1)
def governanca() -> dict:
    return _ler("governanca.json")


@lru_cache(maxsize=1)
def exemplos_prontos() -> list[dict]:
    """Metadados + conteúdo dos JSONs de aluno em data/exemplos/."""
    indice = _ler("exemplos/_index.json")["exemplos"]
    resultado: list[dict] = []
    for item in indice:
        payload = _ler(f"exemplos/{item['arquivo']}")
        resultado.append({**item, "payload": payload})
    return resultado
