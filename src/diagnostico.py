"""Diagnóstico de maturidade — Aula 1.

Cada aluno pontua 5 dimensões (0-6). Total 0-30 mapeia em 4 níveis (0-3).
Gargalo = dimensão de menor score."""

from __future__ import annotations

from src import data_loader


def total_maturidade(diagnostico: dict) -> int:
    return sum(int(diagnostico.get(d["id"], 0) or 0) for d in data_loader.dimensoes()["dimensoes"])


def nivel_por_total(total: int) -> dict:
    for n in data_loader.niveis()["niveis_maturidade"]:
        lo, hi = n["faixa_total"]
        if lo <= total <= hi:
            return n
    return data_loader.niveis()["niveis_maturidade"][-1]


def identificar_gargalo(diagnostico: dict) -> dict:
    """Retorna a dimensão com menor nota. Empate quebra pela ordem do JSON."""
    dims = data_loader.dimensoes()["dimensoes"]
    minimo = min(int(diagnostico.get(d["id"], 0) or 0) for d in dims)
    for d in dims:
        if int(diagnostico.get(d["id"], 0) or 0) == minimo:
            return d
    return dims[0]


def leitura_executiva(diagnostico: dict) -> str:
    total = total_maturidade(diagnostico)
    nivel = nivel_por_total(total)
    gargalo = identificar_gargalo(diagnostico)
    return (
        f"Total {total}/30 · Nível {nivel['numero']} — {nivel['rotulo']}. "
        f"{nivel['descricao']} Gargalo prioritário: **{gargalo['rotulo']}** "
        f"({int(diagnostico.get(gargalo['id'], 0) or 0)}/6)."
    )
