"""Governança e HITL — Aula 2 · slides 32-36.

Princípio de ouro: quanto maior o impacto da decisão, maior a validação humana.
Cada caso rastreia entrada, processamento, saída, validação e registro."""

from __future__ import annotations

from typing import Any

from src import data_loader


def estado_zerado(caso_id: str) -> dict[str, Any]:
    """Estrutura de governança vazia para um caso."""
    rast = data_loader.governanca()["rastreabilidade"]
    seg = data_loader.governanca()["blocos_seguranca"]
    return {
        "caso_id": caso_id,
        "rastreabilidade": {r["id"]: "" for r in rast},
        "seguranca": {s["id"]: False for s in seg},
        "riscos_marcados": [],
        "aprovador": "",
        "decisao_registrada": False,
    }


def nivel_hitl_por_impacto(nota_impacto: int) -> dict:
    """Mapeia nota de impacto (1-5) em nível HITL (leve / estruturada / executiva)."""
    n = max(1, min(5, int(nota_impacto or 1)))
    for nivel in data_loader.governanca()["niveis_hitl"]:
        if int(nivel["score_impacto_min"]) <= n <= int(nivel["score_impacto_max"]):
            return nivel
    return data_loader.governanca()["niveis_hitl"][-1]


def workflow_validacao() -> list[str]:
    """4 passos do workflow (Aula 2 · slide 36)."""
    return list(data_loader.governanca()["workflow_validacao"])


def cobertura_seguranca(estado: dict) -> float:
    """% de blocos de segurança marcados como cobertos (0.0 a 1.0)."""
    seg = estado.get("seguranca") or {}
    if not seg:
        return 0.0
    return sum(1 for v in seg.values() if v) / len(seg)


def cobertura_rastreabilidade(estado: dict) -> float:
    """% de campos de rastreabilidade preenchidos."""
    rast = estado.get("rastreabilidade") or {}
    if not rast:
        return 0.0
    return sum(1 for v in rast.values() if str(v).strip()) / len(rast)


def pronto_para_producao(caso: dict, estado: dict) -> tuple[bool, list[str]]:
    """Checagem final antes de rodar em produção. Retorna (ok, pendências)."""
    pendencias: list[str] = []
    if not (caso.get("dono") or "").strip():
        pendencias.append("Sem dono humano declarado.")
    if cobertura_seguranca(estado) < 1.0:
        pendencias.append("Blocos de segurança incompletos.")
    if cobertura_rastreabilidade(estado) < 1.0:
        pendencias.append("Rastreabilidade incompleta (entrada/processamento/saída/validação/registro).")
    if not (estado.get("aprovador") or "").strip():
        pendencias.append("Aprovador HITL não indicado.")
    if not estado.get("decisao_registrada"):
        pendencias.append("Decisão ainda não registrada.")
    return (len(pendencias) == 0, pendencias)


def resumo(caso: dict, estado: dict) -> dict:
    """Snapshot pronto para renderizar no dashboard e PDF."""
    nota_imp = int((caso.get("notas") or {}).get("impacto", 3) or 3)
    nivel = nivel_hitl_por_impacto(nota_imp)
    ok, pend = pronto_para_producao(caso, estado)
    return {
        "caso_id": caso.get("id"),
        "rotulo": caso.get("rotulo", ""),
        "nivel_hitl": nivel["id"],
        "aprovador_sugerido": nivel["aprovador"],
        "descricao_hitl": nivel["descricao"],
        "cobertura_seguranca": round(cobertura_seguranca(estado), 2),
        "cobertura_rastreabilidade": round(cobertura_rastreabilidade(estado), 2),
        "pronto_producao": ok,
        "pendencias": pend,
    }
