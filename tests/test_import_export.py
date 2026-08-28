"""Testes de import_export.py — round-trip e tolerância a payloads sem envelope."""

import json

from src import import_export, priorizacao


def _estado_exemplo():
    caso = priorizacao.novo_caso("Piloto Alfa")
    caso["dono"] = "PMO"
    return {
        "contexto": {"nome": "Geovane", "empresa": "Eixo", "porte": "PME"},
        "diagnostico": {"estrategia_valor": 3, "dados_processos": 2},
        "mapa": {"contexto": "Portfólio 2026", "dor": "Atrasos"},
        "casos_uso": [caso],
        "governanca": {caso["id"]: {"aprovador": "Sponsor"}},
    }


def test_round_trip_preserva_dados():
    original = _estado_exemplo()
    conteudo = import_export.exportar(original)
    restaurado = import_export.importar(conteudo)
    assert restaurado["contexto"] == original["contexto"]
    assert restaurado["diagnostico"] == original["diagnostico"]
    assert restaurado["mapa"] == original["mapa"]
    assert restaurado["casos_uso"][0]["rotulo"] == "Piloto Alfa"
    assert restaurado["casos_uso"][0]["dono"] == "PMO"


def test_exportar_traz_envelope_com_versao():
    payload = json.loads(import_export.exportar(_estado_exemplo()))
    assert payload["app"] == "mapa-ia-pppm"
    assert "versao" in payload
    assert "gerado_em" in payload
    assert "dados" in payload


def test_importar_aceita_dados_sem_envelope():
    puro = {
        "contexto": {"nome": "Teste"},
        "diagnostico": {},
        "mapa": {},
        "casos_uso": [],
        "governanca": {},
    }
    restaurado = import_export.importar(json.dumps(puro))
    assert restaurado["contexto"] == {"nome": "Teste"}


def test_importar_aceita_bytes():
    conteudo = import_export.exportar(_estado_exemplo()).encode("utf-8")
    restaurado = import_export.importar(conteudo)
    assert restaurado["contexto"]["nome"] == "Geovane"


def test_recomendacao_texto_persiste_no_round_trip():
    original = _estado_exemplo()
    original["recomendacao_texto"] = "Recomendo priorizar o piloto Alfa."
    conteudo = import_export.exportar(original)
    restaurado = import_export.importar(conteudo)
    assert restaurado["recomendacao_texto"] == "Recomendo priorizar o piloto Alfa."


def test_importar_payload_v10_default_recomendacao_vazia():
    puro_v10 = {
        "app": "mapa-ia-pppm",
        "versao": "1.0",
        "dados": {
            "contexto": {"nome": "X"},
            "diagnostico": {},
            "mapa": {},
            "casos_uso": [],
            "governanca": {},
        },
    }
    restaurado = import_export.importar(json.dumps(puro_v10))
    assert restaurado["recomendacao_texto"] == ""
