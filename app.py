import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- CSS PARA ESTILIZAÇÃO DA TELA DE LOGIN ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    div[data-testid="stExpander"] {
        border: none !important;
        box-shadow: none !important;
    }
    .welcome-text {
        text-align: center;
        color: #1E3A8A;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        margin-bottom: 20px;
    }
    .login-container {
        max-width: 500px;
        margin: auto;
        padding: 30px;
        background: white;
        border-radius: 15px;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. CONTROLE DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"

def realizar_login(u, s):
    usuarios_validos = {
        "admin": "1234",
        "raphaelcardozo@raphsonengenharia.com.br": "1234"
    }
    u_clean = u.strip().lower()
    if u_clean in usuarios_validos and s == usuarios_validos[u_clean]:
        st.session_state['autenticado'] = True
        st.session_state['nivel'] = "Admin"
        st.rerun()
    else:
        st.error("⚠️ Credenciais incorretas. Tente novamente.")

# --- 2. TELA DE LOGIN ESTILIZADA ---
if not st.session_state['autenticado']:
    # Espaçamento Superior
    st.write("<br>", unsafe_allow_html=True)
    
    # Logos Centralizadas e Responsivas
    col_l1, col_l2, col_l3, col_l4 = st.columns([1, 1.5, 1.5, 1])
    
    with col_l2:
        try:
            st.image("LOGO RAPHSON FUNDO TRANSPARENTE.png", use_container_width=True)
        except: st.write("Logo Raphson")
            
    with col_l3:
        try:
            st.image("omega inc.png", use_container_width=True)
        except: st.write("Logo Omega")

    # Título e Boas-Vindas
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px; color: #64748b;'>Bem-vindo ao portal administrativo. Identifique-se para continuar.</p>", unsafe_allow_html=True)

    # Container de Login
    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
    
    with col_c2:
        tab_login, tab_reset = st.tabs(["🔐 Entrar no Sistema", "🔑 Redefinir Acesso"])
        
        with tab_login:
            with st.form("login_moderno"):
                u_input = st.text_input("Usuário ou E-mail")
                s_input = st.text_input("Sua Senha", type="password")
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ACESSAR PAINEL", use_container_width=True):
                    realizar_login(u_input, s_input)
                    
        with tab_reset:
            st.write("### Recuperar Senha")
            email_rec = st.text_input("Digite seu e-mail cadastrado")
            if st.button("ENVIAR CÓDIGO", use_container_width=True):
                st.info("Se o e-mail estiver cadastrado, você receberá um link de redefinição.")
    
    st.stop()

# --- 3. SISTEMA APÓS LOGIN (MANTIDO) ---
with st.sidebar:
    st.success(f"Logado como: {st.session_state['nivel']}")
    if st.button("🚪 Sair"):
        st.session_state['autenticado'] = False
        st.rerun()
    st.divider()
    modulo = st.selectbox("Menu:", ["🏠 Dashboard", "📅 Escala", "👤 Gestão"])

if modulo == "🏠 Dashboard":
    st.title("Painel Geral")
    st.write("Sistema Operacional.")
