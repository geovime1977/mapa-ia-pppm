"""Testes de anonimização — o que sobe para o Sheets NÃO pode ter dado identificável."""

from __future__ import annotations

from src.telemetria import anonimizar


def _estado_completo() -> dict:
    return {
        "contexto": {
            "nome": "Fulano da Silva",
            "empresa": "Acme Corp",
            "porte": "Média",
            "cargo": "Diretor de PMO",
            "n_projetos": 12,
            "pmo_ativo": True,
        },
        "diagnostico": {"dados": 3, "processos": 4, "pessoas": 2, "tecnologia": 3, "governanca": 2},
        "mapa": {"dor": "atraso em relatórios", "dado": "jira", "decisao": "quem prioriza",
                 "acao": "consolidar", "valor": "reduzir 2 dias"},
        "casos_uso": [
            {
                "id": "abc12345",
                "rotulo": "Relatório automático",
                "descricao": "pipeline de status",
                "dor": "consolidação manual",
                "dono": "Ciclana de Souza — Diretora",
                "notas": {"impacto": 5, "viabilidade": 4, "dados": 4, "risco": 3, "valor": 5},
            },
            {
                "id": "def67890",
                "rotulo": "Sem dono",
                "descricao": "x",
                "dor": "y",
                "dono": "",
                "notas": {"impacto": 3, "viabilidade": 3, "dados": 3, "risco": 3, "valor": 3},
            },
        ],
        "governanca": {
            "abc12345": {
                "caso_id": "abc12345",
                "seguranca": {"a": True, "b": False},
                "rastreabilidade": {"e": "jira", "p": "", "s": "email", "v": "PMO", "r": "ata"},
                "aprovador": "Ciclana",
                "decisao_registrada": True,
            }
        },
    }


def test_anonimizar_remove_nome_empresa_cargo():
    anon = anonimizar(_estado_completo())
    ctx = anon["contexto"]
    assert "nome" not in ctx
    assert "empresa" not in ctx
    assert "cargo" not in ctx
    assert ctx["porte"] == "Média"
    assert ctx["n_projetos"] == 12
    assert ctx["pmo_ativo"] is True


def test_anonimizar_remove_dono_nominal_dos_casos():
    anon = anonimizar(_estado_completo())
    casos = anon["casos_uso"]
    assert len(casos) == 2
    for c in casos:
        assert "dono" not in c
        assert "tem_dono" in c
    assert casos[0]["tem_dono"] is True
    assert casos[1]["tem_dono"] is False


def test_anonimizar_mantem_notas_e_texto_livre():
    anon = anonimizar(_estado_completo())
    assert anon["diagnostico"]["dados"] == 3
    assert anon["mapa"]["dor"] == "atraso em relatórios"
    assert anon["casos_uso"][0]["notas"]["impacto"] == 5
    assert anon["casos_uso"][0]["descricao"] == "pipeline de status"


def test_anonimizar_governanca_vira_stats():
    anon = anonimizar(_estado_completo())
    g = anon["governanca"]["abc12345"]
    assert g["cobertura_seguranca"] == 1
    assert g["total_seguranca"] == 2
    assert g["cobertura_rastreabilidade"] == 4
    assert g["total_rastreabilidade"] == 5
    assert g["tem_aprovador"] is True
    assert g["decisao_registrada"] is True
    assert "aprovador" not in g


def test_anonimizar_serializa_sem_pii():
    import json
    anon = anonimizar(_estado_completo())
    dumped = json.dumps(anon, ensure_ascii=False)
    assert "Fulano" not in dumped
    assert "Acme" not in dumped
    assert "Ciclana" not in dumped
    assert "Diretora" not in dumped
