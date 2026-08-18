"""Testes de pdf.py — smoke test do gerador. Só valida bytes válidos de PDF."""

from src import governanca, pdf, priorizacao


def test_gera_pdf_com_estado_vazio():
    estado = {"contexto": {}, "diagnostico": {}, "mapa": {}, "casos_uso": [], "governanca": {}}
    bytes_pdf = pdf.gerar_pdf(estado)
    assert bytes_pdf.startswith(b"%PDF-")
    assert len(bytes_pdf) > 500


def test_gera_pdf_com_estado_completo():
    caso = priorizacao.novo_caso("Relatório Executivo Automático")
    caso["dono"] = "PMO"
    for k in caso["notas"]:
        caso["notas"][k] = 4
    estado = {
        "contexto": {"nome": "Geovane", "empresa": "Eixo Estratégico", "porte": "PME"},
        "diagnostico": {
            "estrategia_valor": 3, "dados_processos": 2, "casos_uso": 3,
            "governanca_hitl": 2, "beneficios_roi": 2,
        },
        "mapa": {
            "contexto": "Portfólio de projetos de TI 2026",
            "dor": "Consolidação de status semanal atrasa e falha",
            "dados": "Jira, atas de comitê",
            "riscos": "Dados sensíveis de clientes internos",
            "valor": "Publicação D+1 aprovada pelo PMO",
        },
        "casos_uso": [caso],
        "governanca": {caso["id"]: governanca.estado_zerado(caso["id"])},
    }
    bytes_pdf = pdf.gerar_pdf(estado)
    assert bytes_pdf.startswith(b"%PDF-")
    assert len(bytes_pdf) > 2000
