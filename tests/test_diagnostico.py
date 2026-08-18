"""Testes de diagnostico.py — total, níveis, gargalo, leitura executiva."""

from src import diagnostico


def _diag(**notas):
    base = {
        "estrategia_valor": 0,
        "dados_processos": 0,
        "casos_uso": 0,
        "governanca_hitl": 0,
        "beneficios_roi": 0,
    }
    base.update(notas)
    return base


def test_total_zero():
    assert diagnostico.total_maturidade(_diag()) == 0


def test_total_maximo():
    assert diagnostico.total_maturidade(_diag(
        estrategia_valor=6, dados_processos=6, casos_uso=6, governanca_hitl=6, beneficios_roi=6
    )) == 30


def test_nivel_inexistente():
    assert diagnostico.nivel_por_total(0)["numero"] == 0
    assert diagnostico.nivel_por_total(5)["numero"] == 0


def test_nivel_reativo():
    assert diagnostico.nivel_por_total(6)["numero"] == 1
    assert diagnostico.nivel_por_total(12)["numero"] == 1


def test_nivel_experimental():
    assert diagnostico.nivel_por_total(13)["numero"] == 2
    assert diagnostico.nivel_por_total(20)["numero"] == 2


def test_nivel_estruturado():
    assert diagnostico.nivel_por_total(21)["numero"] == 3
    assert diagnostico.nivel_por_total(30)["numero"] == 3


def test_nivel_acima_max_ainda_encontra():
    # Robustez: total > 30 (não deveria acontecer) mapeia para Estruturado.
    assert diagnostico.nivel_por_total(999)["numero"] == 3


def test_gargalo_menor_nota():
    d = _diag(estrategia_valor=5, dados_processos=1, casos_uso=4, governanca_hitl=3, beneficios_roi=4)
    assert diagnostico.identificar_gargalo(d)["id"] == "dados_processos"


def test_gargalo_empate_pega_primeiro_do_json():
    # Empate: estrategia_valor vem antes de dados_processos no JSON.
    d = _diag(estrategia_valor=1, dados_processos=1, casos_uso=5, governanca_hitl=5, beneficios_roi=5)
    assert diagnostico.identificar_gargalo(d)["id"] == "estrategia_valor"


def test_leitura_executiva_tem_total_e_nivel():
    d = _diag(estrategia_valor=3, dados_processos=2, casos_uso=3, governanca_hitl=2, beneficios_roi=2)
    texto = diagnostico.leitura_executiva(d)
    assert "12/30" in texto
    assert "Reativo" in texto
