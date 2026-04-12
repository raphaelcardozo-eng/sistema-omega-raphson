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
    st.divider()
    st.info("Utilize o menu lateral para navegar entre os setores.")

# --- 4. GESTÃO DE USUÁRIOS ---
elif modulo == "👤 Gestão de Usuários":
    st.subheader("👤 Gestão de Usuários e Acessos")
    
    tab1, tab2, tab3 = st.tabs(["🆕 Novo Cadastro", "🔑 Alterar Senha", "❌ Excluir Usuário"])
    
    with tab1:
        with st.form("form_novo_usuario", clear_on_submit=True):
            st.write("### Registrar Novo Membro")
            c1, c2 = st.columns(2)
            with c1:
                nome_u = st.text_input("Nome Completo")
                email_u = st.text_input("E-mail Corporativo")
                senha_u = st.text_input("Definir Senha", type="password")
            with c2:
                # Setor Comercial incluído
                setor_u = st.selectbox("Setor", ["Diretoria", "Engenharia", "Manutenção", "Comercial", "Financeiro"])
                acesso_u = st.select_slider("Nível de Acesso", options=["Leitor", "Editor", "Admin"])
            
            if st.form_submit_button("Registrar"):
                if nome_u and email_u and senha_u:
                    st.success(f"Usuário {nome_u} pré-cadastrado com sucesso!")
                else:
                    st.error("Todos os campos são obrigatórios.")

    with tab2:
        with st.form("form_alterar_senha"):
            st.write("### Alteração de Senha")
            email_alt = st.text_input("Confirme o E-mail")
            nova_senha = st.text_input("Nova Senha", type="password")
            confirma_s = st.text_input("Repita a Nova Senha", type="password")
            
            if st.form_submit_button("Salvar Nova Senha"):
                if nova_senha == confirma_s and nova_senha:
                    st.success("Senha atualizada!")
                else:
                    st.error("As senhas não coincidem.")

    with tab3:
        with st.form("form_excluir"):
            st.write("### Excluir Conta")
            email_del = st.text_input("E-mail do usuário a remover")
            confirma_del = st.checkbox("Confirmo a exclusão permanente deste acesso.")
            
            if st.form_submit_button("Excluir Permanentemente"):
                if confirma_del and email_del:
                    st.success(f"Usuário {email_del} removido.")
                else:
                    st.warning("Marque a confirmação e digite o e-mail.")

# --- 5. DEMAIS SETORES ---
elif modulo == "🛠️ Manutenção":
    st.subheader("🛠️ Controle de Manutenção")
    if CSV_URL:
        try:
            df = pd.read_csv(CSV_URL)
            st.dataframe(df, use_container_width=True)
        except:
            st.error("Erro ao ler banco de dados.")

elif modulo == "🤝 Comercial":
    st.subheader("🤝 Gestão Comercial")
    st.info("Módulo Comercial carregado.")

elif modulo == "📅 Escalas de Trabalho":
    st.subheader("📅 Cronograma")

elif modulo == "💰 Financeiro":
    st.subheader("💰 Financeiro")
    st.warning("Área Restrita.")

elif modulo == "📊 Relatórios":
    st.subheader("📊 BI & Performance")
