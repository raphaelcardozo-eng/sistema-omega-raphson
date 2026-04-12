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
    # Adicionado todos os setores planejados
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
        st.metric(label="Manutenções Hoje", value="2", delta="Pendentes")

    st.divider()
    st.info("Utilize o menu lateral para navegar entre os departamentos.")

# --- 4. MÓDULO DE MANUTENÇÃO ---
elif modulo == "🛠️ Manutenção":
    st.subheader("🛠️ Controle de Manutenção")
    if CSV_URL:
        try:
            df = pd.read_csv(CSV_URL)
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Erro ao carregar banco de dados.")

# --- 5. GESTÃO DE USUÁRIOS (NOVO) ---
elif modulo == "👤 Gestão de Usuários":
    st.subheader("👤 Cadastro de Novos Usuários")
    st.write("Adicione membros da equipe para acesso ao sistema.")
    
    with st.form("form_usuarios", clear_on_submit=True):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail corporativo")
        with col_u2:
            setor = st.selectbox("Departamento", ["Engenharia", "Operacional", "Financeiro", "Diretoria"])
            nivel = st.radio("Nível de Acesso", ["Visualização", "Editor", "Administrador"], horizontal=True)
        
        btn_user = st.form_submit_button("Cadastrar Usuário")
        
        if btn_user:
            if nome and email:
                st.success(f"Solicitação de cadastro para {nome} enviada com sucesso!")
            else:
                st.warning("Por favor, preencha o nome e o e-mail.")

# --- 6. ESCALAS / FINANCEIRO / RELATÓRIOS (ESTRUTURA PRONTA) ---
elif modulo == "📅 Escalas de Trabalho":
    st.subheader("📅 Gestão de Escalas")
    st.info("Módulo em integração com o calendário de campo.")

elif modulo
