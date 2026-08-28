"""Testes do gerador determinístico de recomendação executiva."""

from __future__ import annotations

from src import priorizacao, recomendacao


def _caso(rotulo: str, notas: dict, dono: str = "PMO", dor: str = "dor exemplo", cid: str | None = None) -> dict:
    c = priorizacao.novo_caso(rotulo)
    if cid:
        c["id"] = cid
    c["dono"] = dono
    c["dor"] = dor
    c["notas"].update(notas)
    return c


def test_sugestao_com_1_caso_pronto_gera_bloco_e_fechamento():
    caso = _caso("Piloto RA", {"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 4, "valor": 5})
    texto = recomendacao.gerar_sugestao_recomendacao(
        [caso], governanca={}, contexto={"empresa": "Acme"},
    )
    assert "Recomendo priorizar 1 caso" in texto
    assert "Caso 1: Piloto RA" in texto
    assert "score ponderado" in texto
    assert "HITL" in texto
    assert "90 dias" in texto


def test_sugestao_ignora_casos_sem_dono():
    com_dono = _caso("Com dono", {"impacto": 5, "viabilidade": 5, "dados": 5, "risco": 5, "valor": 5})
    sem_dono = _caso("Sem dono", {"impacto": 5, "viabilidade": 5, "dados": 5, "risco": 5, "valor": 5}, dono="")
    texto = recomendacao.gerar_sugestao_recomendacao(
        [com_dono, sem_dono], governanca={}, contexto={},
    )
    assert "Com dono" in texto
    assert "Sem dono" not in texto
    assert "Recomendo priorizar 1 caso" in texto


def test_sugestao_com_zero_casos_prontos_retorna_mensagem_orientativa():
    texto = recomendacao.gerar_sugestao_recomendacao([], governanca={}, contexto={})
    assert "Ainda não há caso pronto" in texto
    assert "aba 4" in texto
    assert "aba 5" in texto


def test_sugestao_trunca_dor_longa_em_140_chars():
    dor_longa = "A" * 500
    caso = _caso(
        "Caso longo",
        {"impacto": 4, "viabilidade": 4, "dados": 4, "risco": 4, "valor": 4},
        dor=dor_longa,
    )
    texto = recomendacao.gerar_sugestao_recomendacao([caso], governanca={}, contexto={})
    assert "A" * 141 not in texto
    assert "A" * 140 + "…" in texto


def test_sugestao_usa_empresa_do_contexto_quando_preenchida():
    caso = _caso("X", {"impacto": 5, "viabilidade": 5, "dados": 5, "risco": 5, "valor": 5})
    texto = recomendacao.gerar_sugestao_recomendacao(
        [caso], governanca={}, contexto={"empresa": "Metalúrgica Sigma"},
    )
    assert "para Metalúrgica Sigma" in texto


def test_sugestao_sem_empresa_omite_para_x():
    caso = _caso("X", {"impacto": 5, "viabilidade": 5, "dados": 5, "risco": 5, "valor": 5})
    texto = recomendacao.gerar_sugestao_recomendacao(
        [caso], governanca={}, contexto={"empresa": ""},
    )
    assert " para " not in texto.split(",")[0]
