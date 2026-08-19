"""mapa-ia-pppm — App Streamlit multi-aba.

Operacionaliza Aula 1 (diagnóstico de maturidade + Mapa Inicial 5 blocos) e
Aula 2 (5 erros, 7 domínios, priorização, governança HITL) do Prof. Bezerra.
100% em session_state; nada persistente no servidor."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

_EXEMPLOS_DIR = Path(__file__).parent / "data" / "exemplos"


def _listar_exemplos_prontos() -> list[dict]:
    """Lê data/exemplos/_index.json e retorna metadados + payload de cada exemplo.
    Definida no app.py (não em data_loader) para evitar problemas de hot-reload
    parcial no Streamlit Cloud."""
    indice_path = _EXEMPLOS_DIR / "_index.json"
    if not indice_path.exists():
        return []
    with open(indice_path, encoding="utf-8") as f:
        indice = json.load(f)["exemplos"]
    resultado: list[dict] = []
    for item in indice:
        arq = _EXEMPLOS_DIR / item["arquivo"]
        if not arq.exists():
            continue
        with open(arq, encoding="utf-8") as f:
            item = {**item, "payload": json.load(f)}
        resultado.append(item)
    return resultado

from src import (
    data_loader,
    diagnostico,
    governanca,
    import_export,
    pdf as pdf_gen,
    priorizacao,
    state,
)


st.set_page_config(
    page_title="Mapa IA em PPPM",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


state.init_state()


# =============================================================================
# SIDEBAR — importar/exportar/resetar
# =============================================================================
with st.sidebar:
    st.title("🗺️ Mapa IA em PPPM")
    st.caption("Aulas 1 e 2 · Prof. Bezerra (BSBr)")
    st.divider()

    st.subheader("Portabilidade")
    upload = st.file_uploader("Importar JSON", type=["json"], key="upload_json")
    if upload is not None:
        try:
            dados = import_export.importar(upload.getvalue())
            for k, v in dados.items():
                st.session_state[k] = v
            st.success("Mapa importado.")
        except Exception as exc:
            st.error(f"Falha na importação: {exc}")

    payload = import_export.exportar(state.get_all_data())
    st.download_button(
        "📥 Exportar JSON",
        data=payload.encode("utf-8"),
        file_name="mapa-ia-pppm.json",
        mime="application/json",
        use_container_width=True,
    )

    st.divider()
    st.subheader("Exemplos prontos")
    st.caption("Carrega um cenário completo com 1 clique. Sobrescreve o mapa atual.")
    for ex in _listar_exemplos_prontos():
        if st.button(ex["botao"], key=f"ex_{ex['id']}", use_container_width=True, help=ex["descricao"]):
            dados = import_export.importar(json.dumps(ex["payload"]))
            for k, v in dados.items():
                st.session_state[k] = v
            st.success(f"Exemplo '{ex['botao']}' carregado.")
            st.rerun()

    st.divider()
    if st.button("🔄 Resetar tudo", type="secondary", use_container_width=True):
        state.reset_state()
        st.rerun()


# =============================================================================
# ABAS
# =============================================================================
abas = st.tabs([
    "1. Contexto",
    "2. Diagnóstico",
    "3. Mapa Inicial",
    "4. Casos de Uso",
    "5. Governança",
    "6. Exportar PDF",
])


# ---------------------------------------------------------------------------- #
# 1. CONTEXTO
# ---------------------------------------------------------------------------- #
with abas[0]:
    st.header("1. Contexto do aluno")
    st.caption("Identifica você e sua organização. Isso vai para a capa do PDF.")
    ctx = st.session_state["contexto"]
    col1, col2 = st.columns(2)
    with col1:
        ctx["nome"] = st.text_input("Seu nome", value=ctx.get("nome", ""))
        ctx["empresa"] = st.text_input("Empresa / órgão", value=ctx.get("empresa", ""))
        ctx["cargo"] = st.text_input("Cargo / papel", value=ctx.get("cargo", ""))
    with col2:
        ctx["porte"] = st.selectbox(
            "Porte",
            ["", "MEI", "PME", "Média", "Grande", "Órgão público"],
            index=["", "MEI", "PME", "Média", "Grande", "Órgão público"].index(ctx.get("porte", "") or ""),
        )
        ctx["n_projetos"] = st.number_input("Nº de projetos ativos", min_value=0, value=int(ctx.get("n_projetos", 0) or 0))
        ctx["pmo_ativo"] = st.checkbox("Já existe PMO ativo", value=bool(ctx.get("pmo_ativo", False)))
    if st.button("Salvar contexto", type="primary"):
        st.session_state["contexto_salvo"] = True
        st.success("Contexto salvo na sessão.")


# ---------------------------------------------------------------------------- #
# 2. DIAGNÓSTICO
# ---------------------------------------------------------------------------- #
with abas[1]:
    st.header("2. Diagnóstico de maturidade")
    st.caption("Pontue de 0 a 6 cada dimensão. Total 0-30 → Nível 0-3.")
    diag = st.session_state["diagnostico"]
    for d in data_loader.dimensoes()["dimensoes"]:
        diag[d["id"]] = st.slider(
            f"**{d['rotulo']}** — {d['descricao']}",
            0, 6, int(diag.get(d["id"], 0) or 0),
            key=f"diag_{d['id']}",
            help=d["referencia"],
        )

    st.divider()
    total = diagnostico.total_maturidade(diag)
    nivel = diagnostico.nivel_por_total(total)
    gargalo = diagnostico.identificar_gargalo(diag)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total", f"{total}/30")
    c2.metric("Nível", f"{nivel['numero']} — {nivel['rotulo']}")
    c3.metric("Gargalo", gargalo["rotulo"])
    st.info(diagnostico.leitura_executiva(diag))


# ---------------------------------------------------------------------------- #
# 3. MAPA INICIAL
# ---------------------------------------------------------------------------- #
with abas[2]:
    st.header("3. Mapa Inicial (5 blocos)")
    st.caption("Aula 1 · slide 33 — responda sobre um projeto, processo ou área concreta.")
    mapa = st.session_state["mapa"]
    for b in data_loader.dimensoes()["blocos_mapa"]:
        mapa[b["id"]] = st.text_area(
            f"**{b['rotulo']}** — {b['pergunta']}",
            value=mapa.get(b["id"], ""),
            key=f"mapa_{b['id']}",
            height=90,
        )
    if st.button("Salvar mapa", type="primary"):
        st.session_state["mapa_salvo"] = True
        st.success("Mapa salvo na sessão.")


# ---------------------------------------------------------------------------- #
# 4. CASOS DE USO
# ---------------------------------------------------------------------------- #
with abas[3]:
    st.header("4. Casos de uso e priorização")
    st.caption("Aula 2 · slide 30 — nota 1-5 nos 5 critérios; corte obrigatório: sem dono, não vai.")

    exemplos = data_loader.exemplos()

    with st.expander("💡 5 erros a evitar antes de cadastrar seu caso (Aula 2 · slides 8-12)"):
        for erro in exemplos["cinco_erros"]:
            st.markdown(f"**{erro['titulo']}** — {erro['descricao']}")
            st.caption(f"↳ {erro['correcao']}  ·  _{erro['referencia']}_")

    with st.expander("📚 4 casos-exemplo da Empresa Alfa (Aula 2 · slide 37)"):
        st.caption("Use como inspiração — copie um rótulo e adapte para o seu contexto.")
        for alfa in exemplos["casos_alfa"]:
            st.markdown(f"**{alfa['rotulo']}**")
            st.markdown(
                f"- Dor: {alfa['dor']}\n"
                f"- Dados: {alfa['dados']}\n"
                f"- Decisão: {alfa['decisao']}\n"
                f"- Valor: {alfa['valor']}"
            )
            st.divider()

    with st.expander("🎯 Carregar caso-exemplo pronto para editar"):
        st.caption("Adiciona 1 caso já pontuado como ponto de partida. Cada botão cobre um quadrante da matriz Impacto × Viabilidade. Depois é só ajustar textos e notas ao seu contexto.")
        _templates = [
            {
                "rotulo": "Relatório executivo automático de portfólio",
                "descricao": "Pipeline que consome status reports do Jira, atas de comitê e plano de riscos, gera resumo executivo semanal em Markdown/PDF e publica para o board.",
                "dor": "Consolidação semanal do portfólio consome 2 dias do PMO e chega ao comitê com atraso; hoje é feita à mão em PowerPoint.",
                "dono": "Diretor de PMO",
                "notas": {"impacto": 5, "viabilidade": 5, "dados": 4, "risco": 4, "valor": 5},
                "botao": "🚀 Fazer agora · Comece aqui (4.65)",
            },
            {
                "rotulo": "Análise preditiva de atrasos em dependências",
                "descricao": "Modelo que aprende do histórico de cronogramas para prever atrasos em dependências críticas antes do impacto no projeto.",
                "dor": "Atrasos em dependências críticas só aparecem depois de já terem estourado o cronograma.",
                "dono": "Coordenação de projetos",
                "notas": {"impacto": 5, "viabilidade": 2, "dados": 3, "risco": 3, "valor": 4},
                "botao": "🔍 Preparar · Investigue (3.55)",
            },
            {
                "rotulo": "Chatbot interno de metodologia",
                "descricao": "Assistente que responde dúvidas de PMs iniciantes sobre metodologia interna (templates, ritos, papéis) consultando a base PMBOK + manual corporativo.",
                "dor": "PMs iniciantes esperam dias por resposta de metodologia; sênior gasta tempo respondendo pergunta repetida.",
                "dono": "PMO corporativo",
                "notas": {"impacto": 2, "viabilidade": 5, "dados": 3, "risco": 3, "valor": 2},
                "botao": "⚠️ Não priorizar · Baixa prioridade (2.95)",
            },
            {
                "rotulo": "Geração automática de EAP a partir de contrato",
                "descricao": "Extrai escopo do contrato assinado e propõe uma EAP inicial em formato de árvore para o PM revisar.",
                "dor": "EAP inicial de projeto novo consome 3 dias do PM em copiar-colar.",
                "dono": "",  # DE PROPÓSITO: dispara o corte obrigatório da Aula 2 · slide 30
                "notas": {"impacto": 2, "viabilidade": 2, "dados": 2, "risco": 2, "valor": 2},
                "botao": "⛔ Evite agora · Bloqueado sem dono (2.00)",
            },
        ]
        # 2 linhas × 2 colunas
        for linha in (_templates[:2], _templates[2:]):
            cols = st.columns(2)
            for tpl, col in zip(linha, cols):
                with col:
                    if st.button(tpl["botao"], key=f"tpl_{tpl['rotulo'][:12]}", use_container_width=True):
                        novo = priorizacao.novo_caso(tpl["rotulo"])
                        novo["descricao"] = tpl["descricao"]
                        novo["dor"] = tpl["dor"]
                        novo["dono"] = tpl["dono"]
                        novo["notas"].update(tpl["notas"])
                        st.session_state["casos_uso"].append(novo)
                        st.success(f"Caso '{tpl['rotulo']}' carregado. Role para baixo para editar.")
                        st.rerun()

    # Streamlit proíbe escrever em session_state[key] depois do widget existir;
    # usamos uma flag processada ANTES do widget na próxima execução.
    if st.session_state.pop("_limpar_novo_rotulo", False):
        st.session_state["novo_rotulo"] = ""

    with st.expander("➕ Adicionar novo caso"):
        novo_rotulo = st.text_input("Rótulo do caso", key="novo_rotulo")
        if st.button("Criar caso"):
            if novo_rotulo.strip():
                st.session_state["casos_uso"].append(priorizacao.novo_caso(novo_rotulo.strip()))
                st.session_state["_limpar_novo_rotulo"] = True
                st.rerun()
            else:
                st.warning("Dê um rótulo curto ao caso.")

    if not st.session_state["casos_uso"]:
        st.info("Nenhum caso cadastrado ainda. Comece criando um acima.")
    else:
        for i, caso in enumerate(list(st.session_state["casos_uso"])):
            with st.expander(f"{caso.get('rotulo') or '(sem rótulo)'} — id {caso['id']}", expanded=False):
                caso["rotulo"] = st.text_input("Rótulo", value=caso.get("rotulo", ""), key=f"rot_{caso['id']}")
                caso["descricao"] = st.text_area("Descrição", value=caso.get("descricao", ""), key=f"desc_{caso['id']}", height=70)
                caso["dor"] = st.text_area("Dor real que resolve", value=caso.get("dor", ""), key=f"dor_{caso['id']}", height=60)
                caso["dono"] = st.text_input("Dono humano da decisão (obrigatório)", value=caso.get("dono", ""), key=f"dono_{caso['id']}")

                st.markdown("**Notas 1-5 nos critérios:**")
                cols = st.columns(5)
                for j, crit in enumerate(data_loader.criterios()["criterios"]):
                    with cols[j]:
                        caso["notas"][crit["id"]] = st.slider(
                            crit["rotulo"], 1, 5,
                            int(caso["notas"].get(crit["id"], 3) or 3),
                            key=f"nota_{caso['id']}_{crit['id']}",
                            help=crit["descricao"],
                        )

                r = priorizacao.resumo(caso)
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Score", f"{r['score']:.2f}")
                c2.markdown(f"**Faixa**<br><span style='color:{r['faixa_cor']}'>■</span> {r['faixa']}", unsafe_allow_html=True)
                c3.markdown(f"**Quadrante**<br><span style='color:{r['quadrante_cor']}'>■</span> {r['quadrante']}", unsafe_allow_html=True)
                c4.markdown(f"**Pronto?**<br>{'✅ Sim' if r['pronto'] else '⛔ Não'}", unsafe_allow_html=True)
                if not r["pronto"]:
                    st.warning(r["motivo_bloqueio"])

                if st.button("🗑️ Remover caso", key=f"rm_{caso['id']}"):
                    st.session_state["casos_uso"] = [c for c in st.session_state["casos_uso"] if c["id"] != caso["id"]]
                    st.session_state["governanca"].pop(caso["id"], None)
                    st.rerun()

        st.divider()
        st.subheader("Ranking consolidado")
        ordenados = priorizacao.ranking(st.session_state["casos_uso"])
        tabela = [priorizacao.resumo(c) for c in ordenados]
        st.dataframe(
            tabela,
            column_config={
                "id": None,
                "faixa_cor": None,
                "quadrante_cor": None,
                "motivo_bloqueio": None,
                "rotulo": "Caso",
                "score": "Score",
                "faixa": "Faixa",
                "quadrante": "Quadrante",
                "dono": "Dono",
                "pronto": "Pronto",
            },
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------------------------- #
# 5. GOVERNANÇA
# ---------------------------------------------------------------------------- #
with abas[4]:
    st.header("5. Governança e HITL")
    st.caption(f"Princípio de ouro: {data_loader.governanca()['principio_de_ouro']}")

    if not st.session_state["casos_uso"]:
        st.info("Cadastre casos na aba 4 antes de configurar governança.")
    else:
        for caso in st.session_state["casos_uso"]:
            estado = st.session_state["governanca"].setdefault(caso["id"], governanca.estado_zerado(caso["id"]))
            nivel = governanca.nivel_hitl_por_impacto(int(caso["notas"].get("impacto", 3) or 3))
            with st.expander(f"{caso.get('rotulo') or caso['id']} — HITL: **{nivel['id']}** ({nivel['aprovador']})", expanded=False):
                st.caption(nivel["descricao"])

                st.markdown("**Blocos de segurança cobertos:**")
                cols = st.columns(2)
                blocos = data_loader.governanca()["blocos_seguranca"]
                for i, b in enumerate(blocos):
                    with cols[i % 2]:
                        estado["seguranca"][b["id"]] = st.checkbox(
                            f"{b['titulo']} — {b['regra']}",
                            value=bool(estado["seguranca"].get(b["id"], False)),
                            key=f"seg_{caso['id']}_{b['id']}",
                        )

                st.markdown("**Rastreabilidade (Entrada · Processamento · Saída · Validação · Registro):**")
                for r in data_loader.governanca()["rastreabilidade"]:
                    estado["rastreabilidade"][r["id"]] = st.text_input(
                        f"{r['titulo']} — {r['descricao']}",
                        value=estado["rastreabilidade"].get(r["id"], ""),
                        key=f"rast_{caso['id']}_{r['id']}",
                    )

                estado["aprovador"] = st.text_input(
                    "Aprovador HITL (nome/papel)",
                    value=estado.get("aprovador", ""),
                    key=f"aprov_{caso['id']}",
                )
                estado["decisao_registrada"] = st.checkbox(
                    "Decisão executiva registrada (ata / e-mail / sistema)",
                    value=bool(estado.get("decisao_registrada", False)),
                    key=f"regdec_{caso['id']}",
                )

                r = governanca.resumo(caso, estado)
                c1, c2, c3 = st.columns(3)
                c1.metric("Segurança", f"{int(r['cobertura_seguranca']*100)}%")
                c2.metric("Rastreabilidade", f"{int(r['cobertura_rastreabilidade']*100)}%")
                c3.metric("Pronto p/ produção", "Sim" if r["pronto_producao"] else "Não")
                if r["pendencias"]:
                    st.warning("Pendências: " + "; ".join(r["pendencias"]))


# ---------------------------------------------------------------------------- #
# 6. EXPORTAR PDF
# ---------------------------------------------------------------------------- #
with abas[5]:
    st.header("6. Exportar Mapa Executivo (PDF)")
    st.caption("Gera o PDF consolidado com contexto, diagnóstico, mapa, casos ranqueados e governança.")

    if st.button("📄 Gerar PDF", type="primary"):
        try:
            bytes_pdf = pdf_gen.gerar_pdf(state.get_all_data())
            st.success("PDF gerado.")
            st.download_button(
                "⬇️ Baixar PDF",
                data=bytes_pdf,
                file_name="mapa-ia-pppm.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as exc:
            st.error(f"Falha ao gerar PDF: {exc}")

    st.divider()
    with st.expander("Ver dados brutos (JSON)"):
        st.code(import_export.exportar(state.get_all_data()), language="json")
