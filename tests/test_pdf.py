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


def test_pdf_com_recomendacao_editada_inclui_texto():
    marcador = "TextoAutoralComMarcadorSingularXYZ42"
    estado = {
        "contexto": {"nome": "X", "empresa": "Y", "porte": "PME"},
        "diagnostico": {},
        "mapa": {},
        "casos_uso": [],
        "governanca": {},
        "recomendacao_texto": f"{marcador}\n\nSegundo parágrafo autoral do aluno.",
    }
    com_reco = pdf.gerar_pdf(estado)
    assert com_reco.startswith(b"%PDF-")
    try:
        import io as _io

        import pypdf
        leitor = pypdf.PdfReader(_io.BytesIO(com_reco))
        texto = "".join(pagina.extract_text() or "" for pagina in leitor.pages)
        assert marcador in texto
    except ImportError:
        baseline = pdf.gerar_pdf({**estado, "recomendacao_texto": ""})
        assert len(com_reco) != len(baseline)
