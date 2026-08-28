"""Testes do glossário — carregamento e aplicação de tooltips <abbr>."""

from __future__ import annotations

from src import glossario


def test_carregar_glossario_traz_20_termos():
    g = glossario.carregar_glossario()
    assert g["versao"] == "1.0"
    assert len(g["termos"]) == 20


def test_aplicar_tooltips_substitui_hitl():
    resultado = glossario.aplicar_tooltips("Governança forte exige HITL em cada etapa.")
    assert "<abbr" in resultado
    assert "HITL" in resultado
    assert 'title="' in resultado


def test_aplicar_tooltips_respeita_case_insensitive():
    resultado = glossario.aplicar_tooltips("O piloto valida a hipótese.")
    assert "<abbr" in resultado
    assert ">piloto<" in resultado


def test_aplicar_tooltips_pula_dentro_de_tag_html():
    entrada = "<p>HITL já dentro de tag</p>"
    resultado = glossario.aplicar_tooltips(entrada)
    assert resultado == entrada


def test_aplicar_tooltips_substitui_no_maximo_uma_vez_por_termo():
    resultado = glossario.aplicar_tooltips("HITL primeiro. HITL depois. HITL terceiro.")
    assert resultado.count("<abbr") == 1


def test_aplicar_tooltips_prefere_alias_mais_longo():
    resultado = glossario.aplicar_tooltips("A validação humana registra decisão.")
    assert "<abbr" in resultado
    assert "validação humana</abbr>" in resultado
