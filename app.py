"""Interface enxuta (Streamlit) — TASK-02.3.

Executar a partir da raiz do repositório:   streamlit run src/app.py
Nenhuma peça é aprovada aqui: as conformes ficam "aguardando revisão humana".
"""
import json
from pathlib import Path

import streamlit as st

from nextgen import viewmodel as vm
from nextgen.config import forbidden_terms_from_env, load_env
from nextgen.generator import GenerationError, gerar
from nextgen.llm import LLMError
from nextgen.manual import load_manual
from nextgen.models import STATUS_BLOQUEADA

DATA = Path(__file__).resolve().parent / "data"

st.set_page_config(page_title="NextGen — criação com governança", layout="wide")
load_env()
manual = load_manual(DATA / "manual_marca_sintetico.json")
exemplo = json.loads((DATA / "briefing_exemplo.json").read_text(encoding="utf-8"))

# ---------------- barra lateral ----------------
st.sidebar.title("NextGen")
modo = st.sidebar.radio("Modo de geração", vm.MODOS)
if modo != vm.MODO_REAL:
    st.sidebar.info("Modo simulado: as peças são fictícias e servem só para demonstrar o fluxo e a governança.")
st.sidebar.markdown("---")
st.sidebar.caption(f"Manual de marca: v{manual.versao} (sintético)")
st.sidebar.caption("Regras de governança: " + ", ".join(r["id"] for r in manual.regras))

# ---------------- cabeçalho ----------------
st.title("Criação de peças em escala, com governança")
st.write("Preencha o briefing. O sistema gera uma variação por formato, confere cada uma "
         "com o manual de marca e **nunca aprova sozinho**: o que passa vai para revisão humana.")

# ---------------- briefing ----------------
with st.form("briefing"):
    objetivo = st.text_area("Objetivo da peça", value=exemplo["objetivo"], height=80)
    publico = st.text_input("Público", value=exemplo["publico"])
    formatos = st.multiselect(
        "Formatos", options=manual.formatos_validos, default=exemplo["formatos"],
        format_func=lambda f: f"{f} — {manual.formatos[f]['descricao']}")
    tom = st.text_input("Tom", value=exemplo["tom"])
    produto = st.text_input("Produto (opcional)", value=exemplo.get("produto", ""))
    restricoes = st.text_input("Restrições (opcional)", value=exemplo.get("restricoes", ""))
    enviar = st.form_submit_button("Gerar variações")

if enviar:
    briefing, problemas = vm.montar_briefing(
        {"objetivo": objetivo, "publico": publico, "formatos": formatos, "tom": tom,
         "produto": produto, "restricoes": restricoes}, manual)
    if problemas:
        st.session_state["resultado"] = None
        for p in problemas:
            st.error(f"Briefing inválido: {p}")
    else:
        try:
            llm = vm.criar_llm(modo)
            with st.spinner("Gerando e conferindo as peças..."):
                st.session_state["resultado"] = gerar(briefing, manual, llm, forbidden_terms_from_env())
        except LLMError as e:
            st.session_state["resultado"] = None
            st.error(f"Não foi possível usar o modelo: {e}")
        except GenerationError as e:
            st.session_state["resultado"] = None
            st.error(f"A geração falhou: {e}")

# ---------------- resultado ----------------
res = st.session_state.get("resultado")
if res is not None:
    r = vm.resumo(res)
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Peças geradas", r["total"])
    c2.metric("Aguardando revisão humana", r["em_revisao"])
    c3.metric("Bloqueadas", r["bloqueadas"])
    c4.metric("Tempo total (s)", r["tempo_segundos"])

    colunas = st.columns(len(res.pecas))
    for coluna, peca in zip(colunas, res.pecas):
        v = peca.variacao
        with coluna:
            st.subheader(v.formato)
            if peca.status == STATUS_BLOQUEADA:
                st.error(vm.ROTULO_STATUS[peca.status])
            else:
                st.info(vm.ROTULO_STATUS[peca.status])
            st.markdown(f"**{v.titulo}**")
            st.write(v.texto)
            st.markdown(f"Botão/CTA: **{v.cta}**")
            st.caption("Caracteres usados")
            st.table(vm.contadores(peca, manual))
            with st.expander("Conformidade com o manual de marca", expanded=(peca.status == STATUS_BLOQUEADA)):
                st.table(vm.linhas_regras(peca))

    st.caption("Peças bloqueadas não seguem adiante. Peças conformes ainda precisam de decisão humana "
               "(registro de aprovação: tarefa futura, a critério do Product Owner).")
