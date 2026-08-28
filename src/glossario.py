"""Glossário PPPM/IA — tooltips via <abbr> HTML. Zero dependência externa."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

_DATA = Path(__file__).resolve().parent.parent / "data" / "glossario.json"


@lru_cache(maxsize=1)
def carregar_glossario() -> dict:
    with open(_DATA, encoding="utf-8") as f:
        return json.load(f)


def definicao_de(slug: str) -> str | None:
    termos = carregar_glossario().get("termos", {})
    termo = termos.get(slug)
    if not termo:
        return None
    return termo.get("definicao")


def _pares_alias_definicao() -> list[tuple[str, str, str]]:
    """Lista de (alias, termo_canonico, definicao) ordenada por alias mais longo primeiro."""
    pares: list[tuple[str, str, str]] = []
    for termo in carregar_glossario().get("termos", {}).values():
        canonico = termo["termo_canonico"]
        definicao = termo["definicao"]
        for alias in termo.get("aliases", []):
            pares.append((alias, canonico, definicao))
    pares.sort(key=lambda t: len(t[0]), reverse=True)
    return pares


def aplicar_tooltips(texto: str) -> str:
    """Envolve o PRIMEIRO match de cada termo canônico num <abbr title="definição">.

    Preserva capitalização do trecho original. Só age em texto que não contém
    tags HTML — se aparecer '<' na string, devolve original."""
    if not texto or "<" in texto:
        return texto
    resultado = texto
    canonicos_ja_usados: set[str] = set()
    for alias, canonico, definicao in _pares_alias_definicao():
        if canonico in canonicos_ja_usados:
            continue
        padrao = re.compile(r"\b" + re.escape(alias) + r"\b", re.IGNORECASE)
        titulo_html = definicao.replace('"', "&quot;")

        def _sub(match: re.Match, _titulo=titulo_html, _canonico=canonico) -> str:
            canonicos_ja_usados.add(_canonico)
            return f'<abbr title="{_titulo}">{match.group(0)}</abbr>'

        novo, n = padrao.subn(_sub, resultado, count=1)
        if n:
            resultado = novo
    return resultado
