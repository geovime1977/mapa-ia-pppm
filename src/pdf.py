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

from src import data_loader, diagnostico, governanca, priorizacao


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
    linhas = [["Rótulo", "Score", "Faixa", "Quadrante", "Dono", "Pronto"]]
    for c in ordenados:
        r = priorizacao.resumo(c)
        linhas.append([
            r["rotulo"] or "(sem rótulo)",
            f"{r['score']:.2f}",
            r["faixa"],
            r["quadrante"],
            r["dono"] or "—",
            "Sim" if r["pronto"] else "Não",
        ])
    tabela = Table(linhas, colWidths=[4.5 * cm, 1.5 * cm, 3 * cm, 3.5 * cm, 3 * cm, 1.5 * cm])
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
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
    doc.build(story)
    return buffer.getvalue()
