"""Priorização de casos de uso — Aula 2.

Cada caso recebe notas 1-5 nos 5 critérios (impacto, viabilidade, dados, risco,
valor). Score final = média ponderada. Corte obrigatório: sem dono humano
declarado, o caso NÃO está pronto independente do score."""

from __future__ import annotations

import uuid
from typing import Any

from src import data_loader


def novo_caso(rotulo: str = "") -> dict[str, Any]:
    """Fábrica de caso zerado. Notas 1-5, default 3 (neutro)."""
    return {
        "id": uuid.uuid4().hex[:8],
        "rotulo": rotulo,
        "descricao": "",
        "dor": "",
        "dono": "",
        "notas": {c["id"]: 3 for c in data_loader.criterios()["criterios"]},
    }


def score_caso(caso: dict) -> float:
    """Média ponderada 1-5 usando os pesos declarados em criterios_priorizacao.json."""
    total = 0.0
    for crit in data_loader.criterios()["criterios"]:
        nota = float(caso.get("notas", {}).get(crit["id"], 0) or 0)
        total += nota * float(crit["peso"])
    return round(total, 2)


def faixa_ranking(score: float) -> dict:
    """Devolve o dict de faixa (fazer_agora / preparar / nao_priorizar)."""
    faixas = data_loader.criterios()["faixas_ranking"]
    for faixa in faixas:
        if score >= float(faixa["score_min"]):
            return faixa
    return faixas[-1]


def pronto_para_executar(caso: dict) -> tuple[bool, str]:
    """Corte obrigatório: sem dono humano declarado, não está pronto.
    Aula 2 · slide 30. Retorna (ok, motivo)."""
    dono = (caso.get("dono") or "").strip()
    if not dono:
        return False, data_loader.criterios()["corte_obrigatorio"]["regra"]
    return True, "Dono humano declarado."


def quadrante(caso: dict) -> dict:
    """Localiza o caso na matriz Impacto × Viabilidade (Aula 2 · slide 29).
    Corte: nota >= 4 é 'alto'."""
    notas = caso.get("notas", {})
    impacto_alto = int(notas.get("impacto", 0) or 0) >= 4
    viab_alta = int(notas.get("viabilidade", 0) or 0) >= 4
    if impacto_alto and viab_alta:
        nome = "Comece aqui"
    elif impacto_alto and not viab_alta:
        nome = "Investigue"
    elif not impacto_alto and viab_alta:
        nome = "Baixa prioridade"
    else:
        nome = "Evite agora"
    for q in data_loader.criterios()["matriz_impacto_viabilidade"]["quadrantes"]:
        if q["nome"] == nome:
            return q
    return {"nome": nome, "cor": "#a3a3a3"}


def ranking(casos: list[dict]) -> list[dict]:
    """Ordena por score desc; empate quebra pelo rótulo."""
    def _chave(c: dict) -> tuple[float, str]:
        return (-score_caso(c), c.get("rotulo", ""))
    return sorted(casos, key=_chave)


def resumo(caso: dict) -> dict:
    """Snapshot pronto para renderizar em tabela ou PDF."""
    s = score_caso(caso)
    ok, motivo = pronto_para_executar(caso)
    q = quadrante(caso)
    f = faixa_ranking(s)
    return {
        "id": caso["id"],
        "rotulo": caso.get("rotulo", ""),
        "dono": caso.get("dono", ""),
        "score": s,
        "faixa": f["rotulo"],
        "faixa_cor": f["cor"],
        "quadrante": q["nome"],
        "quadrante_cor": q["cor"],
        "pronto": ok,
        "motivo_bloqueio": "" if ok else motivo,
    }
