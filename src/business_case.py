"""Business Case — Aula 3 (Prof. Bezerra · BSBr).

Cada caso da Aula 2 pode ganhar 1 Business Case preliminar aqui: 8 blocos +
benefício em 3 camadas + custo em 5 camadas + riscos + ROI + decisão.

Corte novo introduzido pela Aula 3:
  - Decisão 'Aprovar piloto' exige benefício líquido positivo no cenário base
    E dono humano declarado (herdado da Aula 2)
    E controle textual em todo risco marcado como alto.

Nada de método PO aqui — só a matemática do slide 14 (ROI) e slide 15 (exemplo)."""

from __future__ import annotations

from typing import Any

from src import data_loader, priorizacao


# ---------------------------------------------------------------------------- #
# Loader
# ---------------------------------------------------------------------------- #
def config() -> dict:
    """Definições da Aula 3 (JSON carregado uma vez)."""
    from functools import lru_cache

    @lru_cache(maxsize=1)
    def _load() -> dict:
        import json
        from pathlib import Path
        p = Path(__file__).resolve().parent.parent / "data" / "business_case.json"
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return _load()


# ---------------------------------------------------------------------------- #
# Estado
# ---------------------------------------------------------------------------- #
def estado_zerado(caso_id: str) -> dict[str, Any]:
    """Business case vazio para 1 caso da Aula 2."""
    cfg = config()
    beneficios: dict[str, dict[str, Any]] = {}
    for camada in cfg["camadas_beneficio"]:
        beneficios[camada["id"]] = {campo["id"]: ("" if campo["tipo"] == "texto" else 0.0) for campo in camada["campos"]}
    custos: dict[str, dict[str, Any]] = {}
    for camada in cfg["camadas_custo"]:
        custos[camada["id"]] = {"valor": 0.0, "premissa": ""}
    riscos: dict[str, dict[str, Any]] = {}
    for r in cfg["riscos_catalogo"]:
        riscos[r["id"]] = {"nivel": "baixo", "controle": ""}
    return {
        "caso_id": caso_id,
        "contexto": "",
        "caso_uso": "",
        "dados": "",
        "beneficios": beneficios,
        "custos": custos,
        "riscos": riscos,
        "janela_meses": 12,
        "cenario": "base",
        "decisao": "",
        "decisao_justificativa": "",
    }


# ---------------------------------------------------------------------------- #
# Cálculo financeiro
# ---------------------------------------------------------------------------- #
def _num(v: Any) -> float:
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def beneficio_anual_bruto(bc: dict) -> float:
    """Soma financeiro + valor monetizado das horas economizadas (operacional).
    Estratégico não entra na conta — é qualitativo por definição da Aula 3."""
    fin = bc.get("beneficios", {}).get("financeiro", {})
    fin_total = _num(fin.get("economia_anual")) + _num(fin.get("receita_adicional_anual")) + _num(fin.get("custo_evitado_anual"))
    op = bc.get("beneficios", {}).get("operacional", {})
    horas_ano = _num(op.get("horas_economizadas_mes")) * 12.0
    op_total = horas_ano * _num(op.get("pessoas_impactadas")) * _num(op.get("custo_hora"))
    return round(fin_total + op_total, 2)


def investimento_total(bc: dict) -> float:
    """Soma das 5 camadas de custo (Aula 3 · slide 12)."""
    total = 0.0
    for camada in bc.get("custos", {}).values():
        total += _num(camada.get("valor"))
    return round(total, 2)


def beneficio_ajustado(bc: dict, janela_meses: int | None = None, cenario: str | None = None) -> float:
    """Benefício bruto anualizado × (janela/12) × multiplicador do cenário."""
    cfg = config()
    janela = int(janela_meses if janela_meses is not None else bc.get("janela_meses", 12))
    cen = str(cenario if cenario is not None else bc.get("cenario", "base"))
    mult = float(cfg["cenarios_multiplicador"].get(cen, 1.0))
    bruto_anual = beneficio_anual_bruto(bc)
    return round(bruto_anual * (janela / 12.0) * mult, 2)


def beneficio_liquido(bc: dict, janela_meses: int | None = None, cenario: str | None = None) -> float:
    return round(beneficio_ajustado(bc, janela_meses, cenario) - investimento_total(bc), 2)


def roi_percentual(bc: dict, janela_meses: int | None = None, cenario: str | None = None) -> float | None:
    """ROI = (benefícios líquidos ÷ investimento) × 100. None se investimento == 0."""
    inv = investimento_total(bc)
    if inv <= 0:
        return None
    bl = beneficio_liquido(bc, janela_meses, cenario)
    return round((bl / inv) * 100.0, 1)


def payback_meses(bc: dict, cenario: str | None = None) -> float | None:
    """Payback = investimento ÷ benefício mensal ajustado. None se benefício mensal <= 0."""
    cfg = config()
    cen = str(cenario if cenario is not None else bc.get("cenario", "base"))
    mult = float(cfg["cenarios_multiplicador"].get(cen, 1.0))
    bruto_mensal = (beneficio_anual_bruto(bc) / 12.0) * mult
    inv = investimento_total(bc)
    if bruto_mensal <= 0 or inv <= 0:
        return None
    return round(inv / bruto_mensal, 1)


def cenarios_completos(bc: dict) -> dict[str, dict]:
    """Devolve o trio pessimista/base/otimista com BL e ROI por cenário."""
    cfg = config()
    out: dict[str, dict] = {}
    janela = int(bc.get("janela_meses", 12))
    for cen in cfg["cenarios_multiplicador"]:
        out[cen] = {
            "beneficio_ajustado": beneficio_ajustado(bc, janela, cen),
            "beneficio_liquido": beneficio_liquido(bc, janela, cen),
            "roi_percentual": roi_percentual(bc, janela, cen),
            "payback_meses": payback_meses(bc, cen),
        }
    return out


# ---------------------------------------------------------------------------- #
# Validação e decisão
# ---------------------------------------------------------------------------- #
def _decisao_por_id(decisao_id: str) -> dict | None:
    for d in config()["decisoes_possiveis"]:
        if d["id"] == decisao_id:
            return d
    return None


def riscos_altos_sem_controle(bc: dict) -> list[str]:
    """Retorna rótulos de riscos marcados como 'alto' sem controle textual preenchido."""
    catalogo = {r["id"]: r["rotulo"] for r in config()["riscos_catalogo"]}
    faltando: list[str] = []
    for rid, dados in bc.get("riscos", {}).items():
        if str(dados.get("nivel", "")).lower() == "alto" and not str(dados.get("controle", "")).strip():
            faltando.append(catalogo.get(rid, rid))
    return faltando


def pode_aprovar(bc: dict, caso: dict) -> tuple[bool, list[str]]:
    """Checa os 3 cortes para 'Aprovar piloto'. Devolve (ok, pendências)."""
    pendencias: list[str] = []
    if beneficio_liquido(bc, cenario="base") <= 0:
        pendencias.append(config()["cortes_bloqueio"]["aprovar_exige_bl_positivo"])
    ok_dono, motivo = priorizacao.pronto_para_executar(caso)
    if not ok_dono:
        pendencias.append(config()["cortes_bloqueio"]["aprovar_exige_dono"])
    faltando = riscos_altos_sem_controle(bc)
    if faltando:
        pendencias.append(
            config()["cortes_bloqueio"]["aprovar_exige_controle"]
            + " Sem controle: " + ", ".join(faltando) + "."
        )
    return (not pendencias), pendencias


def decisoes_disponiveis(bc: dict, caso: dict) -> list[dict]:
    """Filtra decisoes_possiveis: se 'aprovar' não passa nos cortes, marca como bloqueada."""
    ok_aprovar, _ = pode_aprovar(bc, caso)
    saida: list[dict] = []
    for d in config()["decisoes_possiveis"]:
        item = dict(d)
        if d.get("exige_bl_positivo") and not ok_aprovar:
            item["disponivel"] = False
        else:
            item["disponivel"] = True
        saida.append(item)
    return saida


# ---------------------------------------------------------------------------- #
# Resumo pronto para UI e PDF
# ---------------------------------------------------------------------------- #
def resumo(bc: dict, caso: dict) -> dict:
    """Snapshot com números + status de aprovação."""
    ok_aprovar, pendencias = pode_aprovar(bc, caso)
    return {
        "caso_id": bc.get("caso_id"),
        "rotulo": caso.get("rotulo") or "(sem rótulo)",
        "beneficio_bruto_anual": beneficio_anual_bruto(bc),
        "investimento": investimento_total(bc),
        "beneficio_liquido_base": beneficio_liquido(bc, cenario="base"),
        "roi_base": roi_percentual(bc, cenario="base"),
        "payback_base": payback_meses(bc, cenario="base"),
        "cenarios": cenarios_completos(bc),
        "decisao": bc.get("decisao") or "",
        "decisao_rotulo": (_decisao_por_id(bc.get("decisao") or "") or {}).get("rotulo", ""),
        "pode_aprovar": ok_aprovar,
        "pendencias_aprovacao": pendencias,
    }
