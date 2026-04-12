import streamlit as st
import pandas as pd
from PIL import Image

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- 1. CONFIGURAÇÃO DO LINK DA PLANILHA ---
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1GjNaksY3_N2AxVvMdVtr2L-0Zk2DXT3luZUwbdNFpeA/edit?gid=0#gid=0"

if "docs.google.com" in URL_PLANILHA:
    CSV_URL = URL_PLANILHA.split("/edit")[0] + "/export?format=csv"
else:
    CSV_URL = None

# --- 2. LOGO E SIDEBAR ---
with st.sidebar:
    try:
        image = Image.open("logo_empresas.png")
        st.image(image, use_container_width=True)
    except:
        st.title("🏢 OMEGA & RAPHSON")
    
    st.divider()
    modulo = st.selectbox("Escolha o Setor:", [
        "🏠 Início", 
        "🛠️ Manutenção", 
        "🤝 Comercial",
        "📅 Escalas de Trabalho",
        "💰 Financeiro",
        "📊 Relatórios",
        "👤 Gestão de Usuários"
    ])

# --- 3. PÁGINA INICIAL ---
if modulo == "🏠 Início":
    st.title("Painel de Gestão Integrada")
    st.subheader("Visão Geral da Operação")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Stands Ativos", value="3", delta="Jazz, Live, Principal")
    with col2:
        st.metric(label="Status da Operação", value="Normal", delta="0 Alertas")
    with col3:
        st.metric(label="Manutenções Hoje", value="Ver Planilha", delta_color="off")

# --- 4. GESTÃO DE USUÁRIOS (CADASTRO, SENHA E EXCLUSÃO) ---
elif modulo == "👤 Gestão de Usuários":
    st.subheader("👤 Cadastro e Gestão de Usuários")
    
    # Criamos 3 abas para organizar as funções
    tab1, tab2, tab3 = st.tabs(["🆕 Novo Cadastro", "🔑 Alterar Senha", "❌ Excluir Usuário"])
    
    with tab1:
        with st.form("novo_usuario", clear_on_submit=
