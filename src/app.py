"""Interface Streamlit — Cenários Fixos, Tema Escuro e Sem Troca de Produto."""
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from nextgen import viewmodel as vm
from nextgen.approval import ROTULOS as ROTULOS_APROV, aprovar, pode_aprovar, rejeitar
from nextgen.catalog import load_catalog
from nextgen.config import forbidden_terms_from_env, load_env
from nextgen.generator import GenerationError, gerar
from nextgen.llm import LLMError, MockLLM
from nextgen.manual import load_manual
from nextgen.metrics import estimar_ganho
from nextgen.models import Briefing, STATUS_APROVADA, STATUS_BLOQUEADA, STATUS_REPROVADA
from nextgen.templates import VARIANTES, render_peca

DATA = Path(__file__).resolve().parent / "data"

st.set_page_config(page_title="Creative AI", layout="wide")

# Apenas um respiro nas bordas, SEM forçar cores
st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }
</style>
""", unsafe_allow_html=True)

load_env()
manual = load_manual(DATA / "manual_marca_sintetico.json")
catalog = load_catalog(DATA / "products_demo.json")

# --- Sidebar ---
with st.sidebar:
    st.title("Painel de Controle")
    revisor = st.text_input("Seu nome (Revisor)", value="Aprovador Sênior")
    st.write("---")
    st.caption(f"Catálogo: **{len(catalog.todos())} produtos**")
    st.caption(f"Manual de Marca: **v{manual.versao}**")

# --- Header ---
st.title("Creative AI")
st.markdown("Produção de criativos em escala com governança determinística e aprovação humana.")

# --- Definição dos Cenários Fixos ---
CENARIOS = {
    "valido": {
        "nome": "1. Exemplo Válido",
        "desc": "Produto em oferta válida. Todas as regras passam.",
        "briefing": {"objetivo": "Divulgar linha de cuidado diário.", "publico": "Adultos", "formatos": ["feed_social", "story", "banner_web"], "tom": "acolhedor", "produto_id": "SKU-EX-001", "restricoes": ""},
        "mock": MockLLM("bom")
    },
    "vencido": {
        "nome": "2. Oferta Vencida (CDC)",
        "desc": "Hidratante com data de validade no passado.",
        "briefing": {"objetivo": "Divulgar hidratante facial.", "publico": "Adultos", "formatos": ["feed_social", "story"], "tom": "acolhedor", "produto_id": "SKU-EX-003", "restricoes": ""},
        "mock": MockLLM("bom")
    },
    "medicamento": {
        "nome": "3. Medicamento (ANVISA)",
        "desc": "Analgésico. Exige disclaimer legal.",
        "briefing": {"objetivo": "Divulgar analgésico.", "publico": "Adultos", "formatos": ["feed_social", "banner_web"], "tom": "acolhedor", "produto_id": "SKU-EX-004", "restricoes": ""},
        "mock": MockLLM("bom")
    },
    "inadequado": {
        "nome": "4. Peças Inadequadas",
        "desc": "Mock gera termos proibidos e estoura limite de texto.",
        "briefing": {"objetivo": "Testar falhas de segurança.", "publico": "Adultos", "formatos": ["feed_social", "story"], "tom": "agressivo", "produto_id": "SKU-EX-001", "restricoes": ""},
        "mock": MockLLM("ruim")
    }
}

if "cenario_ativo" not in st.session_state:
    st.session_state["cenario_ativo"] = "valido"

# --- Seleção de Cenário ---
st.markdown("### Selecione um cenário para testar:")
cols = st.columns(4)
for i, (key, c) in enumerate(CENARIOS.items()):
    if cols[i].button(c["nome"], use_container_width=True):
        st.session_state["cenario_ativo"] = key
        st.session_state["resultado"] = None
        st.rerun()

c_ativo = st.session_state["cenario_ativo"]
dados_cenario = CENARIOS[c_ativo]

st.info(f"**Cenário Selecionado:** {dados_cenario['desc']}")

# --- Formulário Editável (SEM PRODUTO BASE) ---
with st.form("form_briefing"):
    st.markdown("#### Briefing da Campanha")
    
    # O Objetivo e Tom ainda podem ser editados se o usuário quiser, mas o produto está travado nos bastidores
    objetivo = st.text_area("Objetivo", value=dados_cenario["briefing"]["objetivo"], height=80)
    
    c1, c2 = st.columns(2)
    publico = c1.text_input("Público", value=dados_cenario["briefing"]["publico"])
    tom = c2.text_input("Tom de Voz", value=dados_cenario["briefing"]["tom"])
    
    formatos = st.multiselect("Formatos Desejados", manual.formatos_validos, default=dados_cenario["briefing"]["formatos"])
    
    btn_gerar = st.form_submit_button("Gerar Peças com este Briefing", type="primary", use_container_width=True)

# --- Ação de Gerar ---
if btn_gerar:
    # Pega o produto_id direto do cenário, sem intervenção do usuário
    produto_id = dados_cenario["briefing"]["produto_id"]
    
    briefing, problemas = vm.montar_briefing(
        {"objetivo": objetivo, "publico": publico, "formatos": formatos, 
         "tom": tom, "produto_id": produto_id, "restricoes": dados_cenario["briefing"]["restricoes"]}, manual)
    
    if problemas:
        for p in problemas: st.error(p)
    else:
        try:
            with st.spinner("Processando e aplicando governança..."):
                st.session_state["resultado"] = gerar(briefing, manual, dados_cenario["mock"], forbidden_terms_from_env(), catalog=catalog)
        except Exception as e:
            st.error(f"Erro: {e}")

# --- Resultados ---
res = st.session_state.get("resultado")
if res:
    st.write("---")
    r = vm.resumo(res)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Peças Geradas", r["total"])
    m2.metric("Aguardando Revisão", r["em_revisao"])
    m3.metric("Bloqueadas", r["bloqueadas"], delta_color="inverse")
    m4.metric("Tempo de Execução", f"{r['tempo_segundos']}s")

    st.subheader("Criativos Gerados")
    for i, peca in enumerate(res.pecas):
        v = peca.variacao
        
        st.write("---")
        col_h, col_v = st.columns([4, 1])
        col_h.markdown(f"#### {v.formato.replace('_', ' ').title()}")
        variante = col_v.selectbox("Layout", list(range(1, VARIANTES[v.formato] + 1)), key=f"v_{i}", label_visibility="collapsed")
        
        if peca.status == STATUS_BLOQUEADA: st.error("BLOQUEADA PELA GOVERNANÇA")
        elif peca.status == STATUS_APROVADA: st.success("APROVADA")
        elif peca.status == STATUS_REPROVADA: st.warning("REPROVADA")
        else: st.info("AGUARDANDO REVISÃO HUMANA")
        
        prod = catalog.get(v.produto_id) if v.produto_id else None
        html = render_peca(peca, prod, manual, variante=variante)
        components.html(html, height=680 if v.formato=="story" else 520, scrolling=True)
        
        with st.expander("Ver Relatório de Governança"):
            st.table(vm.linhas_regras(peca))
            
        ok_apr, motivo = pode_aprovar(peca)
        c_btn1, c_btn2, c_btn3 = st.columns([2, 1, 1])
        com = c_btn1.text_input("Comentário (obrigatório p/ rejeitar)", key=f"c_{i}", label_visibility="collapsed", placeholder="Escreva um comentário se for rejeitar...")
        
        if c_btn2.button("Aprovar", key=f"ap_{i}", disabled=not ok_apr, use_container_width=True):
            ok, msg = aprovar(peca, revisor, com)
            if ok: st.rerun()
        
        if c_btn3.button("Rejeitar", key=f"rj_{i}", use_container_width=True):
            ok, msg = rejeitar(peca, revisor, com)
            if ok: st.rerun()
            
        if not ok_apr: st.caption(f"*{motivo}*")
        if peca.decisao: st.caption(f"Log: {peca.decisao['acao']} por {peca.decisao['responsavel']}")

    st.write("---")
    st.subheader("Métricas de Produtividade")
    c_met1, c_met2 = st.columns([1, 1])
    t_man = c_met1.number_input("Tempo manual estimado por peça (minutos)", value=20.0, step=1.0)
    ganho = estimar_ganho(t_man, r["total"], r["tempo_segundos"])
    if "erro" not in ganho:
        c_met2.metric("Redução de Esforço Estimada", f"{ganho['reducao_pct']}%")
        st.info(f"**Análise:** Produção manual de {ganho['num_pecas']} peças levaria **{ganho['tempo_manual_total_min']} min**. A IA levou **{ganho['tempo_assistido_min']} min**.")