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
        "📅 Escalas de Trabalho",
        "💰 Financeiro",
        "📊 Relatórios",
        "👤 Gestão de Usuários"
    ])

# --- 3. PÁGINA INICIAL (DASHBOARD) ---
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

    st.divider()
    st.markdown("### Informativos Recentes")
    st.info("Utilize o menu lateral para navegar entre os departamentos da Omega & Raphson.")

# --- 4. MÓDULO DE MANUTENÇÃO ---
elif modulo == "🛠️ Manutenção":
    st.subheader("🛠️ Controle de Manutenção")
    if CSV_URL:
        try:
            df = pd.read_csv(CSV_URL)
            st.dataframe(df, use_container_width=True)
            st.success("Dados carregados da Planilha Google.")
        except:
            st.error("Erro ao acessar a planilha. Verifique a publicação na web.")

# --- 5. GESTÃO DE USUÁRIOS ---
elif modulo == "👤 Gestão de Usuários":
    st.subheader("👤 Cadastro e Gestão de Usuários")
    
    with st.form("novo_usuario", clear_on_submit=True):
        st.write("Preencha os dados para solicitar acesso:")
        c1, c2 = st.columns(2)
        with c1:
            nome_novo = st.text_input("Nome Completo")
            email_novo = st.text_input("E-mail Corporativo")
        with c2:
            setor_novo = st.selectbox("Setor", ["Engenharia", "Manutenção", "Financeiro", "Diretoria"])
            acesso_novo = st.select_slider("Nível de Acesso", options=["Leitura", "Editor", "Admin"])
        
        enviar = st.form_submit_button("Registrar Usuário")
        if enviar:
            if nome_novo and email_novo:
                st.success(f"Usuário {nome_novo} pré-cadastrado! (Aguardando aprovação do Admin)")
            else:
                st.error("Por favor, preencha todos os campos obrigatórios.")

# --- 6. OUTROS SET
