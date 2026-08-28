"""Gerador determinístico de recomendação executiva.

Filtra casos com dono humano declarado E score ponderado >= 3.0, ordena por
score desc, pega o top 3 e monta um texto abertura + bloco por caso + fechamento
seguindo o vocabulário oficial das Aulas 1 e 2 (Prof. Bezerra)."""

from __future__ import annotations

from src import priorizacao

_LIMITE_DOR = 140
_TOP_N = 3
_SCORE_MINIMO = 3.0

_MENSAGEM_VAZIA = (
    "Ainda não há caso pronto para virar recomendação executiva. "
    "Registre pelo menos 1 caso com dono humano declarado, score ponderado ≥ 3.0 "
    "e governança em preenchimento. Comece pela aba 4 (Casos de uso) e pela aba 5 (Governança)."
)


def _dor_curta(caso: dict) -> str:
    texto = (caso.get("dor") or "").strip()
    if not texto:
        return "não informada"
    if len(texto) > _LIMITE_DOR:
        return texto[:_LIMITE_DOR] + "…"
    return texto


def _metrica_sugerida(caso: dict, governanca: dict) -> str:
    estado = (governanca or {}).get(caso.get("id")) or {}
    rast = estado.get("rastreabilidade") or {}
    registro = str(rast.get("registro") or "").strip()
    if registro:
        return registro
    aprovador = str(estado.get("aprovador") or "").strip()
    if aprovador:
        return f"acompanhamento com {aprovador}"
    return "definir métrica na aba Governança"


def _frase_diagnostico(diagnostico: dict | None) -> tuple[str, str]:
    if not diagnostico:
        return "conforme informado", "a definir"
    nivel_rotulo = str(diagnostico.get("nivel_rotulo") or "").strip()
    nivel_numero = diagnostico.get("nivel_numero")
    total = diagnostico.get("total")
    if nivel_numero is not None and nivel_rotulo and total is not None:
        diag_frase = f"Nível {nivel_numero} — {nivel_rotulo} (total {total}/30)"
    elif nivel_rotulo:
        diag_frase = nivel_rotulo
    else:
        diag_frase = "conforme informado"
    gargalo = str(diagnostico.get("gargalo") or "").strip() or "a definir"
    return diag_frase, gargalo


def _casos_prontos(casos_uso: list[dict]) -> list[dict]:
    prontos = []
    for caso in casos_uso or []:
        if not (caso.get("dono") or "").strip():
            continue
        if priorizacao.score_caso(caso) < _SCORE_MINIMO:
            continue
        prontos.append(caso)
    prontos.sort(key=lambda c: priorizacao.score_caso(c), reverse=True)
    return prontos[:_TOP_N]


def gerar_sugestao_recomendacao(
    casos_uso: list[dict],
    governanca: dict,
    contexto: dict,
    diagnostico: dict | None = None,
) -> str:
    prontos = _casos_prontos(casos_uso)
    if not prontos:
        return _MENSAGEM_VAZIA

    empresa = str((contexto or {}).get("empresa") or "").strip()
    escopo_frase = f" para {empresa}" if empresa else ""
    diag_frase, gargalo = _frase_diagnostico(diagnostico)

    abertura = (
        f"Recomendo priorizar {len(prontos)} caso(s) de uso de IA em PPPM{escopo_frase}, "
        f"com base no diagnóstico de maturidade {diag_frase} e no gargalo prioritário em {gargalo}. "
        "Os casos abaixo foram selecionados por combinarem score executivo ≥ 3.0, dono humano "
        "da decisão declarado e enquadramento na matriz Impacto × Viabilidade."
    )

    blocos: list[str] = []
    for i, caso in enumerate(prontos, start=1):
        score = priorizacao.score_caso(caso)
        faixa = priorizacao.faixa_ranking(score)["rotulo"]
        bloco = (
            f"Caso {i}: {caso.get('rotulo') or '(sem rótulo)'} (id {caso.get('id')}) — "
            f"score ponderado {score:.2f}, faixa {faixa}. "
            f"Responsável: {caso.get('dono')}. "
            f"Dor endereçada: {_dor_curta(caso)}. "
            f"Métrica de acompanhamento sugerida: {_metrica_sugerida(caso, governanca)}."
        )
        blocos.append(bloco)

    fechamento = (
        "Como próximo passo, recomendo iniciar pelo caso de maior score, respeitando o "
        "princípio de ouro da governança: quanto maior o impacto da decisão, maior deve ser "
        "a validação humana. A implementação deverá ocorrer com HITL em cada etapa crítica, "
        "rastreabilidade completa (entrada · processamento · saída · validação · registro) e "
        "decisão executiva registrada em ata ou sistema equivalente. Reavaliar o portfólio de "
        "casos a cada 90 dias para incorporar novas dores e novos dados."
    )

    return "\n\n".join([abertura, *blocos, fechamento])


__all__ = ["gerar_sugestao_recomendacao"]
