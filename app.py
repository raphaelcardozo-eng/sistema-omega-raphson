import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- 1. CONTROLE DE ACESSO (SESSION STATE) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"

def login(u, s):
    # Simulação de base de dados (Pode ser substituído pela sua planilha no futuro)
    if u == "admin" and s == "1234":
        st.session_state['autenticado'] = True
        st.session_state['nivel'] = "Admin"
    elif u == "editor" and s == "1234":
        st.session_state['autenticado'] = True
        st.session_state['nivel'] = "Editor"
    else:
        st.error("Credenciais inválidas.")

def logout():
    st.session_state['autenticado'] = False
    st.rerun()

# --- 2. TELA DE ENTRADA (LOGIN / ESQUECI SENHA) ---
if not st.session_state['autenticado']:
    st.title("🏗️ Sistema Integrado Omega & Raphson")
    t_login, t_reset = st.tabs(["🔐 Acesso", "🔑 Esqueci a Senha"])
    
    with t_login:
        with st.form("form_login"):
            u_input = st.text_input("Usuário")
            s_input = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar"):
                login(u_input, s_input)
                
    with t_reset:
        st.subheader("Recuperação de Acesso")
        email_rec = st.text_input("E-mail Cadastrado")
        if st.button("Solicitar Nova Senha"):
            st.info(f"As instruções de redefinição foram enviadas para {email_rec}")
    st.stop()

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    try:
        image = Image.open("logo_empresas.png")
        st.image(image, use_container_width=True)
    except:
        st.title("🏢 OMEGA & RAPHSON")
    
    st.write(f"✅ **Sessão:** {st.session_state['nivel']}")
    if st.button("🚪 Sair do Sistema"):
        logout()
    
    st.divider()
    modulo = st.selectbox("Navegação:", [
        "🏠 Dashboard Inicial", 
        "📅 Escala de Trabalho", 
        "👤 Gestão e Cadastros", 
        "🛠️ Manutenção", 
        "🤝 Comercial"
    ])

# --- 4. DASHBOARD INICIAL ---
if modulo == "🏠 Dashboard Inicial":
    st.title("Painel de Gestão Integrada")
    c1, c2, c3 = st.columns(3)
    c1.metric("Stands Ativos", "3", "Jazz, Live, Principal")
    c2.metric("Equipe em Campo", "8", "Técnicos")
    c3.metric("Status Global", "Operacional")

# --- 5. ESCALA DE TRABALHO (CALENDÁRIO DINÂMICO) ---
elif modulo == "📅 Escala de Trabalho":
    st.title("📅 Escala Mensal de Trabalho")
    hoje = datetime.now()
    ano, mes = hoje.year, hoje.month
    
    # Cabeçalho do Calendário
    st.subheader(f"Visualização: {calendar.month_name[mes]} / {ano}")
    
    # Criar a grade do calendário
    cal = calendar.monthcalendar(ano
