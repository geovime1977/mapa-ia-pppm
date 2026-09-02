"""Gerador de PDF do Mapa Executivo. reportlab platypus.

Layout: capa · contexto · diagnóstico (barras + gargalo) · mapa 5 blocos ·
casos ranqueados (tabela) · governança (por caso pronto)."""

from __future__ import annotations

import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src import business_case as business_case_mod
from src import data_loader, diagnostico, governanca, priorizacao, recomendacao


def _estilos() -> dict:
    base = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle("Titulo", parent=base["Title"], fontSize=22, spaceAfter=14),
        "h1": ParagraphStyle("H1", parent=base["Heading1"], fontSize=15, spaceAfter=8, textColor=colors.HexColor("#1e3a8a")),
        "h2": ParagraphStyle("H2", parent=base["Heading2"], fontSize=12, spaceAfter=6),
        "corpo": ParagraphStyle("Corpo", parent=base["BodyText"], fontSize=10, spaceAfter=4, leading=13),
        "small": ParagraphStyle("Small", parent=base["BodyText"], fontSize=8, textColor=colors.grey),
    }


def _capa(story: list, ctx: dict, est: dict) -> None:
    nome = (ctx.get("nome") or "Aluno").strip() or "Aluno"
    empresa = (ctx.get("empresa") or "-").strip() or "-"
    porte = (ctx.get("porte") or "-").strip() or "-"
    story.append(Paragraph("Mapa Executivo — IA em PPPM", est["titulo"]))
    story.append(Paragraph(f"Aluno: <b>{nome}</b>", est["corpo"]))
    story.append(Paragraph(f"Empresa: <b>{empresa}</b> · Porte: <b>{porte}</b>", est["corpo"]))
    story.append(Paragraph(f"Gerado em {datetime.now():%d/%m/%Y %H:%M}", est["small"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Baseado nas Aulas 1 e 2 · Prof. Bezerra (BSBr)", est["small"]))
    story.append(Spacer(1, 0.6 * cm))


def _secao_diagnostico(story: list, diag: dict, est: dict) -> None:
    story.append(Paragraph("1. Diagnóstico de maturidade", est["h1"]))
    total = diagnostico.total_maturidade(diag)
    nivel = diagnostico.nivel_por_total(total)
    gargalo = diagnostico.identificar_gargalo(diag)
    story.append(Paragraph(diagnostico.leitura_executiva(diag), est["corpo"]))
    story.append(Spacer(1, 0.2 * cm))

    linhas = [["Dimensão", "Nota (0-6)"]]
    for d in data_loader.dimensoes()["dimensoes"]:
        linhas.append([d["rotulo"], str(int(diag.get(d["id"], 0) or 0))])
    linhas.append(["TOTAL", f"{total}/30 — Nível {nivel['numero']} ({nivel['rotulo']})"])
    tabela = Table(linhas, colWidths=[10 * cm, 6 * cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#e5e7eb")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(f"<b>Gargalo prioritário:</b> {gargalo['rotulo']} — {gargalo['descricao']}", est["corpo"]))


def _secao_mapa(story: list, mapa: dict, est: dict) -> None:
    story.append(PageBreak())
    story.append(Paragraph("2. Mapa Inicial (5 blocos)", est["h1"]))
    for b in data_loader.dimensoes()["blocos_mapa"]:
        story.append(Paragraph(f"<b>{b['rotulo']}</b> — {b['pergunta']}", est["h2"]))
        resposta = (mapa.get(b["id"]) or "").strip() or "<i>não preenchido</i>"
        story.append(Paragraph(resposta, est["corpo"]))
        story.append(Spacer(1, 0.15 * cm))


def _secao_casos(story: list, casos: list, est: dict) -> None:
    story.append(PageBreak())
    story.append(Paragraph("3. Casos de uso priorizados", est["h1"]))
    if not casos:
        story.append(Paragraph("Nenhum caso cadastrado.", est["corpo"]))
        return
    ordenados = priorizacao.ranking(casos)
    celula = ParagraphStyle("Celula", parent=est["corpo"], fontSize=8, leading=10, spaceAfter=0)
    celula_head = ParagraphStyle("CelulaHead", parent=celula, textColor=colors.white, fontName="Helvetica-Bold")

    linhas: list = [[Paragraph(h, celula_head) for h in ["Rótulo", "Score", "Faixa", "Quadrante", "Dono", "Pronto"]]]
    for c in ordenados:
        r = priorizacao.resumo(c)
        linhas.append([
            Paragraph(r["rotulo"] or "(sem rótulo)", celula),
            Paragraph(f"{r['score']:.2f}", celula),
            Paragraph(r["faixa"], celula),
            Paragraph(r["quadrante"], celula),
            Paragraph(r["dono"] or "—", celula),
            Paragraph("Sim" if r["pronto"] else "Não", celula),
        ])
    tabela = Table(linhas, colWidths=[5.0 * cm, 1.3 * cm, 2.6 * cm, 3.0 * cm, 3.6 * cm, 1.5 * cm], repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 0.3 * cm))
    bloqueados = [c for c in ordenados if not priorizacao.pronto_para_executar(c)[0]]
    if bloqueados:
        story.append(Paragraph(
            f"<b>{len(bloqueados)} caso(s) bloqueado(s)</b> pelo corte obrigatório (sem dono humano declarado).",
            est["corpo"],
        ))


def _secao_governanca(story: list, casos: list, gov: dict, est: dict) -> None:
    story.append(PageBreak())
    story.append(Paragraph("4. Governança e HITL", est["h1"]))
    story.append(Paragraph(
        f"<b>Princípio de ouro:</b> {data_loader.governanca()['principio_de_ouro']}",
        est["corpo"],
    ))
    story.append(Spacer(1, 0.2 * cm))
    if not casos:
        story.append(Paragraph("Sem casos para avaliar governança.", est["corpo"]))
        return
    for c in casos:
        estado = gov.get(c["id"]) or governanca.estado_zerado(c["id"])
        r = governanca.resumo(c, estado)
        story.append(Paragraph(f"<b>{r['rotulo'] or c['id']}</b> — nível <b>{r['nivel_hitl']}</b> ({r['aprovador_sugerido']})", est["h2"]))
        story.append(Paragraph(
            f"Segurança: {int(r['cobertura_seguranca']*100)}% · "
            f"Rastreabilidade: {int(r['cobertura_rastreabilidade']*100)}% · "
            f"Pronto p/ produção: {'Sim' if r['pronto_producao'] else 'Não'}",
            est["corpo"],
        ))
        if r["pendencias"]:
            story.append(Paragraph("Pendências: " + "; ".join(r["pendencias"]), est["corpo"]))
        story.append(Spacer(1, 0.15 * cm))


def _fmt_moeda(v: float) -> str:
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "R$ 0,00"


def _secao_business_cases(story: list, casos: list, bcs: dict, est: dict) -> None:
    """5. Business Cases preliminares — 1 subseção por caso com BC preenchido (Aula 3)."""
    cfg = business_case_mod.config()
    casos_com_bc = [c for c in casos if bcs.get(c["id"])]
    if not casos_com_bc:
        return
    story.append(PageBreak())
    story.append(Paragraph("5. Business Cases preliminares (Aula 3)", est["h1"]))
    story.append(Paragraph(f"<i>{cfg['principio']}</i>", est["corpo"]))
    story.append(Spacer(1, 0.2 * cm))

    for c in casos_com_bc:
        bc = bcs[c["id"]]
        r = business_case_mod.resumo(bc, c)
        story.append(Paragraph(f"<b>{r['rotulo']}</b>", est["h2"]))

        linhas = [
            ["Contexto e dor", (bc.get("contexto") or "—")[:400]],
            ["Caso de uso de IA", (bc.get("caso_uso") or "—")[:400]],
            ["Dados necessários", (bc.get("dados") or "—")[:400]],
            ["Investimento total", _fmt_moeda(r["investimento"])],
            ["Benefício bruto anual", _fmt_moeda(r["beneficio_bruto_anual"])],
            [
                f"Cenário base ({bc.get('janela_meses', 12)} meses)",
                f"BL: {_fmt_moeda(r['beneficio_liquido_base'])} · "
                f"ROI: {r['roi_base']}%" if r['roi_base'] is not None else f"BL: {_fmt_moeda(r['beneficio_liquido_base'])} · ROI: —",
            ],
            [
                "Payback (cenário base)",
                f"{r['payback_base']} meses" if r["payback_base"] is not None else "—",
            ],
            ["Decisão solicitada", r["decisao_rotulo"] or "— (não preenchida)"],
        ]
        tabela = Table(linhas, colWidths=[4.5 * cm, 12.0 * cm])
        tabela.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e5e7eb")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(tabela)
        story.append(Spacer(1, 0.15 * cm))

        cenarios = r["cenarios"]
        story.append(Paragraph("<b>Cenários (pessimista / base / otimista):</b>", est["corpo"]))
        cen_linhas = [["Cenário", "Benefício líquido", "ROI %", "Payback"]]
        for nome in ("pessimista", "base", "otimista"):
            info = cenarios.get(nome, {})
            cen_linhas.append([
                nome.capitalize(),
                _fmt_moeda(info.get("beneficio_liquido") or 0),
                f"{info['roi_percentual']}%" if info.get("roi_percentual") is not None else "—",
                f"{info['payback_meses']} m" if info.get("payback_meses") is not None else "—",
            ])
        cen_tab = Table(cen_linhas, colWidths=[3.5 * cm, 5.0 * cm, 3.5 * cm, 4.5 * cm])
        cen_tab.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ]))
        story.append(cen_tab)

        if not r["pode_aprovar"] and r["decisao"] == "aprovar_piloto":
            story.append(Spacer(1, 0.1 * cm))
            story.append(Paragraph(
                "<b>Atenção:</b> decisão 'Aprovar piloto' marcada mas não passa nos cortes: "
                + " · ".join(r["pendencias_aprovacao"]),
                est["corpo"],
            ))
        story.append(Spacer(1, 0.3 * cm))


def _secao_recomendacao(story: list, texto: str, estado: dict, est: dict) -> None:
    """6. Recomendação executiva — texto editável do aluno ou sugestão on-the-fly."""
    story.append(PageBreak())
    story.append(Paragraph("6. Recomendação executiva", est["h1"]))
    conteudo = (texto or "").strip()
    if not conteudo:
        conteudo = recomendacao.gerar_sugestao_recomendacao(
            estado.get("casos_uso") or [],
            estado.get("governanca") or {},
            estado.get("contexto") or {},
            _diag_para_recomendacao(estado.get("diagnostico") or {}),
        )
        story.append(Paragraph(
            "<i>Texto sugerido automaticamente — o aluno pode editar na aba 6.</i>",
            est["small"],
        ))
        story.append(Spacer(1, 0.15 * cm))
    for paragrafo in conteudo.split("\n\n"):
        p = paragrafo.strip()
        if not p:
            continue
        story.append(Paragraph(p, est["corpo"]))
        story.append(Spacer(1, 0.15 * cm))


def _diag_para_recomendacao(diag: dict) -> dict | None:
    """Empacota diagnóstico bruto no formato consumido por recomendacao."""
    if not diag:
        return None
    total = diagnostico.total_maturidade(diag)
    nivel = diagnostico.nivel_por_total(total)
    gargalo = diagnostico.identificar_gargalo(diag)
    return {
        "total": total,
        "nivel_numero": nivel["numero"],
        "nivel_rotulo": nivel["rotulo"],
        "gargalo": gargalo["rotulo"],
    }


def _secao_referencias(story: list, est: dict) -> None:
    """Apêndice pedagógico: 5 erros a evitar + 4 casos-exemplo da Empresa Alfa."""
    ex = data_loader.exemplos()
    story.append(PageBreak())
    story.append(Paragraph("7. Referências pedagógicas (Aula 2)", est["h1"]))

    story.append(Paragraph("6.1 · Cinco erros a evitar", est["h2"]))
    for erro in ex["cinco_erros"]:
        story.append(Paragraph(f"<b>{erro['titulo']}</b> — {erro['descricao']}", est["corpo"]))
        story.append(Paragraph(f"↳ {erro['correcao']}", est["small"]))
        story.append(Spacer(1, 0.1 * cm))

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("6.2 · Casos-exemplo da Empresa Alfa", est["h2"]))
    for alfa in ex["casos_alfa"]:
        story.append(Paragraph(f"<b>{alfa['rotulo']}</b>", est["corpo"]))
        story.append(Paragraph(
            f"Dor: {alfa['dor']}<br/>Dados: {alfa['dados']}<br/>"
            f"Decisão: {alfa['decisao']}<br/>Valor: {alfa['valor']}",
            est["corpo"],
        ))
        story.append(Spacer(1, 0.15 * cm))


def gerar_pdf(estado: dict) -> bytes:
    """Retorna os bytes do PDF."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=1.8 * cm, bottomMargin=1.8 * cm,
        title="Mapa Executivo IA em PPPM",
    )
    est = _estilos()
    story: list = []
    _capa(story, estado.get("contexto") or {}, est)
    _secao_diagnostico(story, estado.get("diagnostico") or {}, est)
    _secao_mapa(story, estado.get("mapa") or {}, est)
    _secao_casos(story, estado.get("casos_uso") or [], est)
    _secao_governanca(story, estado.get("casos_uso") or [], estado.get("governanca") or {}, est)
    _secao_business_cases(story, estado.get("casos_uso") or [], estado.get("business_cases") or {}, est)
    _secao_recomendacao(story, estado.get("recomendacao_texto") or "", estado, est)
    _secao_referencias(story, est)
    doc.build(story)
    return buffer.getvalue()
