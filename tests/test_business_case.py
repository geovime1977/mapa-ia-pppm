"""Testes de business_case.py — ROI, payback, cenários, cortes de aprovação."""

from __future__ import annotations

import pytest

from src import business_case as bc_mod
from src import priorizacao


def _caso_com_dono(rotulo="Piloto"):
    c = priorizacao.novo_caso(rotulo)
    c["dono"] = "PMO"
    return c


def _bc_com_valores(caso):
    """BC do exemplo calculado da Aula 3 · slide 15 — retrabalho R$ 600k → -25%.
    Benefício estimado R$ 150k, investimento R$ 60k → ROI 150%, payback 4,8 meses."""
    bc = bc_mod.estado_zerado(caso["id"])
    bc["beneficios"]["financeiro"]["economia_anual"] = 150_000.0
    bc["custos"]["tecnologia"]["valor"] = 30_000.0
    bc["custos"]["mudanca"]["valor"] = 30_000.0
    bc["janela_meses"] = 12
    bc["cenario"] = "base"
    return bc


# ---------------------------------------------------------------------------- #
# Estrutura básica
# ---------------------------------------------------------------------------- #
def test_estado_zerado_tem_estrutura_esperada():
    bc = bc_mod.estado_zerado("abc12345")
    assert bc["caso_id"] == "abc12345"
    assert set(bc["beneficios"].keys()) == {"financeiro", "operacional", "estrategico"}
    assert set(bc["custos"].keys()) == {"tecnologia", "dados", "pessoas", "mudanca", "governanca"}
    assert bc["janela_meses"] == 12
    assert bc["cenario"] == "base"
    assert bc["decisao"] == ""


def test_config_carrega_json():
    cfg = bc_mod.config()
    assert cfg["cenarios_multiplicador"]["base"] == 1.0
    assert len(cfg["prompts_ferramenta"]) == 4
    assert len(cfg["estudos_simulados"]) == 3


# ---------------------------------------------------------------------------- #
# Cálculo financeiro
# ---------------------------------------------------------------------------- #
def test_beneficio_bruto_anual_soma_financeiro_e_operacional():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    bc["beneficios"]["financeiro"]["economia_anual"] = 100_000
    bc["beneficios"]["operacional"]["horas_economizadas_mes"] = 10
    bc["beneficios"]["operacional"]["pessoas_impactadas"] = 5
    bc["beneficios"]["operacional"]["custo_hora"] = 120
    # financeiro: 100_000 + operacional: 10*12*5*120 = 72_000 → total 172_000
    assert bc_mod.beneficio_anual_bruto(bc) == pytest.approx(172_000.0)


def test_investimento_total_soma_5_camadas():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    for camada in ["tecnologia", "dados", "pessoas", "mudanca", "governanca"]:
        bc["custos"][camada]["valor"] = 10_000
    assert bc_mod.investimento_total(bc) == pytest.approx(50_000.0)


def test_exemplo_calculado_aula3_slide15():
    """Aula 3 · slide 15: R$150k benefício, R$60k invest → BL 90k, ROI 150%, payback 4,8m."""
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    assert bc_mod.investimento_total(bc) == pytest.approx(60_000.0)
    assert bc_mod.beneficio_anual_bruto(bc) == pytest.approx(150_000.0)
    assert bc_mod.beneficio_liquido(bc) == pytest.approx(90_000.0)
    assert bc_mod.roi_percentual(bc) == pytest.approx(150.0)
    assert bc_mod.payback_meses(bc) == pytest.approx(4.8, abs=0.1)


def test_cenarios_pessimista_reduz_beneficio_pela_metade():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    ben_base = bc_mod.beneficio_ajustado(bc, cenario="base")
    ben_pess = bc_mod.beneficio_ajustado(bc, cenario="pessimista")
    assert ben_pess == pytest.approx(ben_base * 0.5)


def test_cenarios_otimista_ampia_beneficio():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    ben_base = bc_mod.beneficio_ajustado(bc, cenario="base")
    ben_otm = bc_mod.beneficio_ajustado(bc, cenario="otimista")
    assert ben_otm == pytest.approx(ben_base * 1.3)


def test_roi_none_quando_investimento_zero():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    bc["beneficios"]["financeiro"]["economia_anual"] = 100_000
    assert bc_mod.roi_percentual(bc) is None


def test_payback_none_quando_beneficio_zero():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    bc["custos"]["tecnologia"]["valor"] = 10_000
    assert bc_mod.payback_meses(bc) is None


def test_cenarios_completos_traz_trio():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    trio = bc_mod.cenarios_completos(bc)
    assert set(trio.keys()) == {"pessimista", "base", "otimista"}
    assert trio["base"]["roi_percentual"] == pytest.approx(150.0)
    assert trio["pessimista"]["beneficio_liquido"] < trio["base"]["beneficio_liquido"]
    assert trio["otimista"]["beneficio_liquido"] > trio["base"]["beneficio_liquido"]


# ---------------------------------------------------------------------------- #
# Cortes de aprovação (regra dura da Aula 3)
# ---------------------------------------------------------------------------- #
def test_corte_aprovar_bloqueia_sem_beneficio_liquido_positivo():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    bc["custos"]["tecnologia"]["valor"] = 10_000  # invest > 0, benefício = 0 → BL negativo
    ok, pendencias = bc_mod.pode_aprovar(bc, caso)
    assert ok is False
    assert any("benefício líquido" in p.lower() for p in pendencias)


def test_corte_aprovar_bloqueia_sem_dono_humano():
    caso = priorizacao.novo_caso("sem dono")  # sem preencher caso["dono"]
    bc = _bc_com_valores(caso)
    ok, pendencias = bc_mod.pode_aprovar(bc, caso)
    assert ok is False
    assert any("dono" in p.lower() for p in pendencias)


def test_corte_aprovar_bloqueia_risco_alto_sem_controle():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    bc["riscos"]["dados_sensiveis"]["nivel"] = "alto"
    bc["riscos"]["dados_sensiveis"]["controle"] = ""
    ok, pendencias = bc_mod.pode_aprovar(bc, caso)
    assert ok is False
    assert any("controle" in p.lower() for p in pendencias)


def test_corte_aprovar_libera_com_tudo_ok():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    ok, pendencias = bc_mod.pode_aprovar(bc, caso)
    assert ok is True
    assert pendencias == []


def test_risco_alto_com_controle_nao_bloqueia():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    bc["riscos"]["dados_sensiveis"]["nivel"] = "alto"
    bc["riscos"]["dados_sensiveis"]["controle"] = "Anonimização + acesso restrito ao PMO."
    ok, _ = bc_mod.pode_aprovar(bc, caso)
    assert ok is True


# ---------------------------------------------------------------------------- #
# Decisões disponíveis
# ---------------------------------------------------------------------------- #
def test_decisoes_disponiveis_marca_aprovar_como_bloqueada_quando_bl_negativo():
    caso = _caso_com_dono()
    bc = bc_mod.estado_zerado(caso["id"])
    bc["custos"]["tecnologia"]["valor"] = 10_000
    decisoes = bc_mod.decisoes_disponiveis(bc, caso)
    aprovar = next(d for d in decisoes if d["id"] == "aprovar_piloto")
    assert aprovar["disponivel"] is False
    ajustar = next(d for d in decisoes if d["id"] == "ajustar")
    assert ajustar["disponivel"] is True


def test_decisoes_disponiveis_libera_aprovar_com_bc_ok():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    decisoes = bc_mod.decisoes_disponiveis(bc, caso)
    aprovar = next(d for d in decisoes if d["id"] == "aprovar_piloto")
    assert aprovar["disponivel"] is True


# ---------------------------------------------------------------------------- #
# Resumo (contrato para UI e PDF)
# ---------------------------------------------------------------------------- #
def test_resumo_traz_todos_os_campos_esperados():
    caso = _caso_com_dono()
    bc = _bc_com_valores(caso)
    r = bc_mod.resumo(bc, caso)
    esperado = {
        "caso_id", "rotulo", "beneficio_bruto_anual", "investimento",
        "beneficio_liquido_base", "roi_base", "payback_base",
        "cenarios", "decisao", "decisao_rotulo",
        "pode_aprovar", "pendencias_aprovacao",
    }
    assert esperado.issubset(r.keys())
    assert r["pode_aprovar"] is True
    assert r["roi_base"] == pytest.approx(150.0)
