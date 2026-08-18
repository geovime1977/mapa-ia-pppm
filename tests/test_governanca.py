"""Testes de governanca.py — estado zerado, nível HITL, coberturas, prontidão."""

from src import governanca, priorizacao


def _caso(impacto=3, dono="PMO"):
    c = priorizacao.novo_caso("Piloto")
    c["dono"] = dono
    c["notas"]["impacto"] = impacto
    return c


def test_estado_zerado_tem_todas_chaves():
    e = governanca.estado_zerado("abc")
    assert e["caso_id"] == "abc"
    assert set(e["rastreabilidade"].keys()) >= {"entrada", "processamento", "saida", "validacao", "registro"}
    assert set(e["seguranca"].keys()) >= {"dados_sensiveis", "acessos", "ambiente_seguro", "controle_uso"}
    assert e["aprovador"] == ""
    assert e["decisao_registrada"] is False


def test_hitl_leve_ate_impacto_2():
    assert governanca.nivel_hitl_por_impacto(1)["id"] == "leve"
    assert governanca.nivel_hitl_por_impacto(2)["id"] == "leve"


def test_hitl_estruturada_impacto_3_4():
    assert governanca.nivel_hitl_por_impacto(3)["id"] == "estruturada"
    assert governanca.nivel_hitl_por_impacto(4)["id"] == "estruturada"


def test_hitl_executiva_impacto_5():
    assert governanca.nivel_hitl_por_impacto(5)["id"] == "executiva"


def test_hitl_clampa_valores_invalidos():
    assert governanca.nivel_hitl_por_impacto(0)["id"] == "leve"
    assert governanca.nivel_hitl_por_impacto(99)["id"] == "executiva"


def test_cobertura_seguranca_vazia():
    assert governanca.cobertura_seguranca(governanca.estado_zerado("x")) == 0.0


def test_cobertura_seguranca_total():
    e = governanca.estado_zerado("x")
    for k in e["seguranca"]:
        e["seguranca"][k] = True
    assert governanca.cobertura_seguranca(e) == 1.0


def test_cobertura_rastreabilidade_parcial():
    e = governanca.estado_zerado("x")
    e["rastreabilidade"]["entrada"] = "Jira export"
    cob = governanca.cobertura_rastreabilidade(e)
    assert 0 < cob < 1


def test_pronto_producao_bloqueia_sem_dono():
    c = priorizacao.novo_caso("X")  # sem dono
    e = governanca.estado_zerado(c["id"])
    ok, pend = governanca.pronto_para_producao(c, e)
    assert ok is False
    assert any("dono" in p.lower() for p in pend)


def test_pronto_producao_libera_tudo_ok():
    c = _caso()
    e = governanca.estado_zerado(c["id"])
    for k in e["seguranca"]:
        e["seguranca"][k] = True
    for k in e["rastreabilidade"]:
        e["rastreabilidade"][k] = "ok"
    e["aprovador"] = "Sponsor"
    e["decisao_registrada"] = True
    ok, pend = governanca.pronto_para_producao(c, e)
    assert ok is True
    assert pend == []
