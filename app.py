"""mapa-ia-pppm — App Streamlit multi-aba.

Operacionaliza Aula 1 (diagnóstico de maturidade + Mapa Inicial 5 blocos) e
Aula 2 (5 erros, 7 domínios, priorização, governança HITL) do Prof. Bezerra.
100% em session_state; nada persistente no servidor."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

_EXEMPLOS_DIR = Path(__file__).parent / "data" / "exemplos"


def _aplicar_dados_importados(dados: dict) -> None:
    """Aplica dados importados no session_state. Também sincroniza as keys dos
    widgets que fixam nome (Diagnóstico e Mapa) — sem isso o Streamlit ignora
    o novo value e mantém o antigo, que é o bug reportado na aula."""
    for k, v in dados.items():
        st.session_state[k] = v
    for k, v in (dados.get("diagnostico") or {}).items():
        st.session_state[f"diag_{k}"] = int(v or 0)
    for k, v in (dados.get("mapa") or {}).items():
        st.session_state[f"mapa_{k}"] = v or ""
    for caso in (dados.get("casos_uso") or []):
        cid = caso.get("id")
        if not cid:
            continue
        st.session_state[f"rot_{cid}"] = caso.get("rotulo", "")
        st.session_state[f"desc_{cid}"] = caso.get("descricao", "")
        st.session_state[f"dor_{cid}"] = caso.get("dor", "")
        st.session_state[f"dono_{cid}"] = caso.get("dono", "")
        for crit_id, nota in (caso.get("notas") or {}).items():
            st.session_state[f"nota_{cid}_{crit_id}"] = int(nota or 3)
    for cid, gov in (dados.get("governanca") or {}).items():
        for bid, v in (gov.get("seguranca") or {}).items():
            st.session_state[f"seg_{cid}_{bid}"] = bool(v)
        for rid, v in (gov.get("rastreabilidade") or {}).items():
            st.session_state[f"rast_{cid}_{rid}"] = v or ""
        st.session_state[f"aprov_{cid}"] = gov.get("aprovador", "")
        st.session_state[f"regdec_{cid}"] = bool(gov.get("decisao_registrada", False))
    for cid, bc in (dados.get("business_cases") or {}).items():
        st.session_state[f"bc_contexto_{cid}"] = bc.get("contexto", "") or ""
        st.session_state[f"bc_caso_uso_{cid}"] = bc.get("caso_uso", "") or ""
        st.session_state[f"bc_dados_{cid}"] = bc.get("dados", "") or ""
        st.session_state[f"bc_janela_{cid}"] = int(bc.get("janela_meses", 12) or 12)
        st.session_state[f"bc_cenario_{cid}"] = bc.get("cenario", "base") or "base"
        st.session_state[f"bc_decisao_{cid}"] = bc.get("decisao", "") or ""
        st.session_state[f"bc_decisao_just_{cid}"] = bc.get("decisao_justificativa", "") or ""
        for camada_id, campos in (bc.get("beneficios") or {}).items():
            for campo_id, valor in campos.items():
                st.session_state[f"bc_ben_{cid}_{camada_id}_{campo_id}"] = valor
        for camada_id, dados_camada in (bc.get("custos") or {}).items():
            st.session_state[f"bc_custo_val_{cid}_{camada_id}"] = float(dados_camada.get("valor", 0) or 0)
            st.session_state[f"bc_custo_prem_{cid}_{camada_id}"] = dados_camada.get("premissa", "") or ""
        for risco_id, r in (bc.get("riscos") or {}).items():
            st.session_state[f"bc_risco_nivel_{cid}_{risco_id}"] = r.get("nivel", "baixo") or "baixo"
            st.session_state[f"bc_risco_ctrl_{cid}_{risco_id}"] = r.get("controle", "") or ""
    if "recomendacao_texto" in dados:
        st.session_state["recomendacao_texto"] = dados["recomendacao_texto"] or ""


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
    business_case as business_case_mod,
    data_loader,
    diagnostico,
    glossario,
    governanca,
    import_export,
    pdf as pdf_gen,
    priorizacao,
    recomendacao,
    state,
    telemetria,
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
    st.caption("Aulas 1, 2 e 3 · Prof. Bezerra (BSBr)")
    st.divider()

    st.subheader("Portabilidade")
    upload = st.file_uploader("Importar JSON", type=["json"], key="upload_json")
    if upload is not None:
        try:
            dados = import_export.importar(upload.getvalue())
            _aplicar_dados_importados(dados)
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
        on_click=telemetria.enviar_uma_vez,
        args=(state.get_all_data(), "export_json"),
    )

    st.divider()
    st.subheader("Exemplos prontos")
    st.caption("Carrega um cenário completo com 1 clique. Sobrescreve o mapa atual.")
    for ex in _listar_exemplos_prontos():
        if st.button(ex["botao"], key=f"ex_{ex['id']}", use_container_width=True, help=ex["descricao"]):
            dados = import_export.importar(json.dumps(ex["payload"]))
            _aplicar_dados_importados(dados)
            st.success(f"Exemplo '{ex['botao']}' carregado.")
            st.rerun()

    st.divider()
    if st.button("🔄 Resetar tudo", type="secondary", use_container_width=True):
        state.reset_state()
        st.rerun()

    st.caption(
        "Seus dados ficam só na sua sessão do navegador. Estatísticas anonimizadas "
        "(notas, categorias, textos sem identificação pessoal) podem ser usadas para "
        "melhoria pedagógica. Não coletamos nome, empresa ou cargo."
    )


# =============================================================================
# ABAS
# =============================================================================
abas = st.tabs([
    "1. Contexto",
    "2. Diagnóstico",
    "3. Mapa Inicial",
    "4. Casos de Uso",
    "5. Governança",
    "6. Business Case",
    "7. Prompts Executivos",
    "8. Exportar PDF",
])


# ---------------------------------------------------------------------------- #
# 1. CONTEXTO
# ---------------------------------------------------------------------------- #
with abas[0]:
    st.header("1. Contexto do cliente")
    st.caption("Identifica o cliente e sua organização. Isso vai para a capa do PDF.")
    ctx = st.session_state["contexto"]
    col1, col2 = st.columns(2)
    with col1:
        ctx["nome"] = st.text_input("Nome do cliente", value=ctx.get("nome", ""))
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

    st.info(
        "Sem evidência clara para atribuir nota alta, use nota 2 como padrão conservador. "
        "Registre a evidência sempre que possível."
    )

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
                        tooltip = glossario.definicao_de(crit["id"]) or crit.get("descricao", "")
                        nota_atual = st.slider(
                            crit["rotulo"], 1, 5,
                            int(caso["notas"].get(crit["id"], 3) or 3),
                            key=f"nota_{caso['id']}_{crit['id']}",
                            help=tooltip,
                        )
                        caso["notas"][crit["id"]] = nota_atual
                        escala = crit.get("escala") or {}
                        st.caption(
                            f"1: {escala.get('1', '-')} · 3: {escala.get('3', '-')} · 5: {escala.get('5', '-')}"
                        )
                        st.caption(
                            f"Nota atual: {nota_atual} — {priorizacao.interpretar_nota(crit['id'], nota_atual)}"
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
    st.markdown(
        glossario.aplicar_tooltips(
            f"Princípio de ouro: {data_loader.governanca()['principio_de_ouro']}"
        ),
        unsafe_allow_html=True,
    )

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
# 6. BUSINESS CASE (Aula 3)
# ---------------------------------------------------------------------------- #
with abas[5]:
    st.header("6. Business Case preliminar")
    st.caption("Aula 3 · Prof. Bezerra — para cada caso da aba 4, monte a tese de valor que vai ao comitê.")

    _bc_cfg = business_case_mod.config()
    st.info(f"**Princípio:** {_bc_cfg['principio']}  \n**Pergunta executiva:** {_bc_cfg['pergunta_executiva']}")

    with st.expander("💡 3 estudos simulados da Aula 3 (slides 24-26)"):
        for est_bc in _bc_cfg["estudos_simulados"]:
            st.markdown(f"**{est_bc['rotulo']}**")
            st.markdown(
                f"- Problema: {est_bc['problema']}\n"
                f"- Solução IA: {est_bc['solucao_ia']}\n"
                f"- Benefício: {est_bc['beneficio']}\n"
                f"- Risco: {est_bc['risco']}  → **Controle:** {est_bc['controle']}\n"
                f"- Decisão solicitada: {est_bc['decisao_solicitada']}"
            )
            st.divider()

    if not st.session_state["casos_uso"]:
        st.warning("Cadastre casos na aba 4 antes de montar o business case.")
    else:
        for caso in st.session_state["casos_uso"]:
            cid = caso["id"]
            bc = st.session_state["business_cases"].setdefault(cid, business_case_mod.estado_zerado(cid))
            with st.expander(
                f"{caso.get('rotulo') or '(sem rótulo)'} — id {cid}",
                expanded=False,
            ):
                st.markdown("**Contexto e caso de uso**")
                bc["contexto"] = st.text_area(
                    "Contexto e dor (com métrica)",
                    value=bc.get("contexto", ""),
                    key=f"bc_contexto_{cid}",
                    height=70,
                    help='Bloco 1 · slide 9 — "32% dos projetos atrasaram mais de 20 dias no último semestre, gerando custo adicional estimado em R$ 480 mil."',
                )
                bc["caso_uso"] = st.text_area(
                    "Como a IA atuará (entrada → processamento → saída)",
                    value=bc.get("caso_uso", ""),
                    key=f"bc_caso_uso_{cid}",
                    height=70,
                    help="Bloco 2 · slide 10 — descreva sem cair no fascínio técnico.",
                )
                bc["dados"] = st.text_area(
                    "Dados necessários e como serão validados",
                    value=bc.get("dados", ""),
                    key=f"bc_dados_{cid}",
                    height=60,
                )

                st.markdown("---")
                st.markdown("**Benefícios (3 camadas · slide 11)**")
                for camada in _bc_cfg["camadas_beneficio"]:
                    st.markdown(f"*{camada['rotulo']}* — {camada['descricao']}")
                    cols = st.columns(len(camada["campos"]))
                    for i, campo in enumerate(camada["campos"]):
                        atual = bc["beneficios"][camada["id"]].get(campo["id"], "" if campo["tipo"] == "texto" else 0.0)
                        with cols[i]:
                            if campo["tipo"] == "texto":
                                bc["beneficios"][camada["id"]][campo["id"]] = st.text_input(
                                    campo["rotulo"],
                                    value=str(atual or ""),
                                    key=f"bc_ben_{cid}_{camada['id']}_{campo['id']}",
                                )
                            else:
                                bc["beneficios"][camada["id"]][campo["id"]] = st.number_input(
                                    campo["rotulo"],
                                    min_value=0.0,
                                    value=float(atual or 0),
                                    step=100.0 if campo["tipo"] == "moeda" else 1.0,
                                    key=f"bc_ben_{cid}_{camada['id']}_{campo['id']}",
                                )

                st.markdown("---")
                st.markdown("**Custos (5 camadas · slide 12) — custo real quase nunca é só licença**")
                cols_c = st.columns(len(_bc_cfg["camadas_custo"]))
                for i, camada in enumerate(_bc_cfg["camadas_custo"]):
                    with cols_c[i]:
                        bc["custos"][camada["id"]]["valor"] = st.number_input(
                            f"{camada['rotulo']} (R$)",
                            min_value=0.0,
                            value=float(bc["custos"][camada["id"]].get("valor", 0) or 0),
                            step=100.0,
                            key=f"bc_custo_val_{cid}_{camada['id']}",
                            help=camada["descricao"],
                        )
                        bc["custos"][camada["id"]]["premissa"] = st.text_input(
                            "Premissa",
                            value=bc["custos"][camada["id"]].get("premissa", ""),
                            key=f"bc_custo_prem_{cid}_{camada['id']}",
                            label_visibility="collapsed",
                            placeholder="Premissa (opcional)",
                        )

                st.markdown("---")
                st.markdown("**Riscos e controles (slide 13) — valor sem controle não escala**")
                for r in _bc_cfg["riscos_catalogo"]:
                    cols_r = st.columns([1, 3])
                    with cols_r[0]:
                        bc["riscos"][r["id"]]["nivel"] = st.selectbox(
                            r["rotulo"],
                            ["baixo", "medio", "alto"],
                            index=["baixo", "medio", "alto"].index(bc["riscos"][r["id"]].get("nivel", "baixo")),
                            key=f"bc_risco_nivel_{cid}_{r['id']}",
                        )
                    with cols_r[1]:
                        bc["riscos"][r["id"]]["controle"] = st.text_input(
                            "Controle",
                            value=bc["riscos"][r["id"]].get("controle", ""),
                            key=f"bc_risco_ctrl_{cid}_{r['id']}",
                            placeholder=f"Padrão sugerido: {r['controle_padrao']}",
                            label_visibility="collapsed",
                        )

                st.markdown("---")
                st.markdown("**ROI e cenários (slides 14-15)**")
                cols_j = st.columns(2)
                with cols_j[0]:
                    bc["janela_meses"] = st.selectbox(
                        "Janela de análise (meses)",
                        _bc_cfg["janelas_analise_meses"],
                        index=_bc_cfg["janelas_analise_meses"].index(int(bc.get("janela_meses", 12))),
                        key=f"bc_janela_{cid}",
                    )
                with cols_j[1]:
                    bc["cenario"] = st.selectbox(
                        "Cenário-alvo para a decisão",
                        ["pessimista", "base", "otimista"],
                        index=["pessimista", "base", "otimista"].index(bc.get("cenario", "base")),
                        key=f"bc_cenario_{cid}",
                    )

                r = business_case_mod.resumo(bc, caso)
                cA, cB, cC, cD = st.columns(4)
                cA.metric("Investimento", f"R$ {r['investimento']:,.0f}".replace(",", "."))
                cB.metric("Benefício bruto/ano", f"R$ {r['beneficio_bruto_anual']:,.0f}".replace(",", "."))
                cC.metric(
                    f"ROI base ({bc['janela_meses']}m)",
                    f"{r['roi_base']}%" if r["roi_base"] is not None else "—",
                )
                cD.metric(
                    "Payback",
                    f"{r['payback_base']} meses" if r["payback_base"] is not None else "—",
                )

                st.markdown("**Cenários (pessimista / base / otimista)**")
                cen_rows = []
                for nome, info in r["cenarios"].items():
                    cen_rows.append({
                        "Cenário": nome,
                        "Benefício líquido (R$)": info["beneficio_liquido"],
                        "ROI %": info["roi_percentual"] if info["roi_percentual"] is not None else "—",
                        "Payback (m)": info["payback_meses"] if info["payback_meses"] is not None else "—",
                    })
                st.dataframe(cen_rows, use_container_width=True, hide_index=True)

                st.markdown("---")
                st.markdown("**Decisão solicitada ao comitê**")
                decisoes = business_case_mod.decisoes_disponiveis(bc, caso)
                opcoes_ids = [""] + [d["id"] for d in decisoes]
                def _label(did: str) -> str:
                    if not did:
                        return "— selecionar —"
                    for d in decisoes:
                        if d["id"] == did:
                            marca = "" if d["disponivel"] else "  ⛔ bloqueada"
                            return f"{d['rotulo']}{marca}"
                    return did
                idx_atual = opcoes_ids.index(bc.get("decisao", "")) if bc.get("decisao", "") in opcoes_ids else 0
                bc["decisao"] = st.selectbox(
                    "Decisão",
                    opcoes_ids,
                    index=idx_atual,
                    format_func=_label,
                    key=f"bc_decisao_{cid}",
                )
                bc["decisao_justificativa"] = st.text_area(
                    "Justificativa curta da decisão (vai para o PDF)",
                    value=bc.get("decisao_justificativa", ""),
                    key=f"bc_decisao_just_{cid}",
                    height=60,
                )

                ok_aprovar, pendencias = business_case_mod.pode_aprovar(bc, caso)
                if bc["decisao"] == "aprovar_piloto" and not ok_aprovar:
                    st.error(
                        "Decisão 'Aprovar piloto' não pode ser registrada. Pendências:\n\n- "
                        + "\n- ".join(pendencias)
                    )
                elif bc["decisao"] and bc["decisao"] != "aprovar_piloto":
                    d_desc = next((d["descricao"] for d in decisoes if d["id"] == bc["decisao"]), "")
                    st.info(f"Decisão registrada: {d_desc}")
                elif ok_aprovar:
                    st.success("Business case passa nos 3 cortes — 'Aprovar piloto' está liberado.")


# ---------------------------------------------------------------------------- #
# 7. PROMPTS EXECUTIVOS (Aula 3)
# ---------------------------------------------------------------------------- #
with abas[6]:
    st.header("7. Prompts executivos")
    st.caption("Aula 3 · slides 20-23 — 4 prompts prontos para usar no ChatGPT/Claude durante a consultoria.")

    _bc_cfg_p = business_case_mod.config()
    for prompt in _bc_cfg_p["prompts_ferramenta"]:
        with st.expander(f"**{prompt['rotulo']}** — {prompt['quando_usar']}", expanded=False):
            st.caption(f"*Entrada recomendada:* {prompt['entrada_recomendada']}  \n*Referência:* {prompt['referencia']}")
            st.code(prompt["texto"], language="text")


# ---------------------------------------------------------------------------- #
# 8. EXPORTAR PDF
# ---------------------------------------------------------------------------- #
with abas[7]:
    st.header("8. Exportar Mapa Executivo (PDF)")
    st.caption("Gera o PDF consolidado com contexto, diagnóstico, mapa, casos ranqueados e governança.")

    st.subheader("Recomendação executiva")
    st.caption("Texto que abrirá o PDF. Comece pela sugestão automática e edite livremente.")
    diag_atual = st.session_state.get("diagnostico") or {}
    diag_para_reco = None
    if diag_atual:
        total_atual = diagnostico.total_maturidade(diag_atual)
        nivel_atual = diagnostico.nivel_por_total(total_atual)
        gargalo_atual = diagnostico.identificar_gargalo(diag_atual)
        diag_para_reco = {
            "total": total_atual,
            "nivel_numero": nivel_atual["numero"],
            "nivel_rotulo": nivel_atual["rotulo"],
            "gargalo": gargalo_atual["rotulo"],
        }
    sugestao = recomendacao.gerar_sugestao_recomendacao(
        st.session_state.get("casos_uso") or [],
        st.session_state.get("governanca") or {},
        st.session_state.get("contexto") or {},
        diag_para_reco,
    )
    with st.expander("Ver sugestão automática", expanded=True):
        st.markdown(glossario.aplicar_tooltips(sugestao), unsafe_allow_html=True)
        if st.button("Usar esta sugestão como base", help="Substitui o texto atual pelo sugerido"):
            st.session_state["recomendacao_texto"] = sugestao
            st.rerun()
    st.text_area(
        "Recomendação (editável)",
        key="recomendacao_texto",
        height=260,
        help="Este texto entra na abertura do PDF, antes das seções analíticas.",
    )

    st.divider()

    if st.button("📄 Gerar PDF", type="primary"):
        try:
            bytes_pdf = pdf_gen.gerar_pdf(state.get_all_data())
            telemetria.enviar_uma_vez(state.get_all_data(), "gerar_pdf")
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
