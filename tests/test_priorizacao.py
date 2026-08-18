"""Testes de priorizacao.py — score, faixa, corte, quadrante, ranking."""

import pytest

from src import priorizacao


def _caso_pronto(**overrides):
    c = priorizacao.novo_caso("Piloto X")
    c["dono"] = "PMO"
    c.update(overrides)
    return c


def test_novo_caso_tem_id_e_notas_default_3():
    c = priorizacao.novo_caso("Caso A")
    assert c["rotulo"] == "Caso A"
    assert len(c["id"]) == 8
    assert all(v == 3 for v in c["notas"].values())


def test_score_com_notas_3_da_3():
    # 3 * (0.30+0.20+0.20+0.15+0.15) = 3.0
    c = _caso_pronto()
    assert priorizacao.score_caso(c) == pytest.approx(3.0)


def test_score_com_notas_5_da_5():
    c = _caso_pronto()
    for k in c["notas"]:
        c["notas"][k] = 5
    assert priorizacao.score_caso(c) == pytest.approx(5.0)


def test_faixa_fazer_agora():
    assert priorizacao.faixa_ranking(4.5)["id"] == "fazer_agora"
    assert priorizacao.faixa_ranking(4.0)["id"] == "fazer_agora"


def test_faixa_preparar():
    assert priorizacao.faixa_ranking(3.5)["id"] == "preparar"
    assert priorizacao.faixa_ranking(3.0)["id"] == "preparar"


def test_faixa_nao_priorizar():
    assert priorizacao.faixa_ranking(2.9)["id"] == "nao_priorizar"
    assert priorizacao.faixa_ranking(0.0)["id"] == "nao_priorizar"


def test_corte_sem_dono_bloqueia():
    c = priorizacao.novo_caso("Sem dono")
    ok, motivo = priorizacao.pronto_para_executar(c)
    assert ok is False
    assert "dono" in motivo.lower()


def test_corte_com_dono_libera():
    ok, _ = priorizacao.pronto_para_executar(_caso_pronto())
    assert ok is True


def test_quadrante_comece_aqui():
    c = _caso_pronto()
    c["notas"]["impacto"] = 5
    c["notas"]["viabilidade"] = 5
    assert priorizacao.quadrante(c)["nome"] == "Comece aqui"


def test_quadrante_investigue():
    c = _caso_pronto()
    c["notas"]["impacto"] = 5
    c["notas"]["viabilidade"] = 2
    assert priorizacao.quadrante(c)["nome"] == "Investigue"


def test_quadrante_evite_agora():
    c = _caso_pronto()
    c["notas"]["impacto"] = 1
    c["notas"]["viabilidade"] = 1
    assert priorizacao.quadrante(c)["nome"] == "Evite agora"


def test_ranking_ordem_desc():
    c1 = _caso_pronto(rotulo="A")
    c2 = _caso_pronto(rotulo="B")
    for k in c2["notas"]:
        c2["notas"][k] = 5
    ranking = priorizacao.ranking([c1, c2])
    assert ranking[0]["rotulo"] == "B"
    assert ranking[1]["rotulo"] == "A"


def test_resumo_marca_bloqueado_sem_dono():
    c = priorizacao.novo_caso("Sem dono")
    r = priorizacao.resumo(c)
    assert r["pronto"] is False
    assert r["motivo_bloqueio"] != ""
