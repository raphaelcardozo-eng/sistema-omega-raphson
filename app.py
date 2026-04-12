import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestão Omega & Raphson", layout="wide", page_icon="🏗️")

# --- CSS PARA DESIGN ATRAENTE ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 45px; 
        background-color: #ffffff; 
        border-radius: 8px; 
        padding: 0px 20px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; }
    p { color: #64748b; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. CONTROLE DE ACESSO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"

def realizar_login(u, s):
    # Base de acesso conforme solicitado
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
        st.error("⚠️ Credenciais inválidas.")

# --- 2. TELA DE LOGIN PERSONALIZADA ---
if not st.session_state['autenticado']:
    st.write("<br>", unsafe_allow_html=True)
    
    # Logos Centralizadas (Usando os nomes exatos do seu GitHub)
    col_l1, col_l2, col_l3, col_l4 = st.columns([1, 1.5, 1.5, 1])
    
    with col_l2:
        try:
            img1 = Image.open("LOGO RAPHSON FUNDO TRANSPARENTE.png")
            st.image(img1, use_container_width=True)
        except: st.write("Logo Raphson")
            
    with col_l3:
        try:
            img2 = Image.open("omega inc.png")
            st.image(img2, use_container_width=True)
        except: st.write("Logo Omega")

    # Títulos Atualizados
    st.markdown("<h1 style='text-align: center;'>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Bem-vindo ao sistema de controle operacional. Por favor, realize o login.</p>", unsafe_allow_html=True)

    # Card de Login
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        tab_acesso, tab_ajuda = st.tabs(["🔐 Acesso Restrito", "❓ Esqueci a Senha"])
        
        with tab_acesso:
            with st.form("form_login_final"):
                user = st.text_input("E-mail ou Usuário")
                senha = st.text_input("Senha", type="password")
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ENTRAR NO PAINEL", use_container_width=True):
                    realizar_login(user, senha)
        
        with tab_ajuda:
            st.info("Para recuperar seu acesso, entre em contato com o suporte da Raphson Engenharia.")

    st.stop()

# --- 3. PAINEL INTERNO (PÓS-LOGIN) ---
with st.sidebar:
    # Pequena logo no topo da sidebar
    st.image("LOGO RAPHSON FUNDO TRANSPARENTE.png", width=150)
    st.write(f"👤 **Acesso:** {st.session_state['nivel']}")
    if st.button("🚪 Sair do Sistema"):
        st.session_state['autenticado'] = False
        st.rerun()
    st.divider()
    modulo = st.selectbox("Selecione o Setor:", ["🏠 Início", "📅 Escala de Trabalho", "👤 Gestão de Usuários"])

# Lógica das telas (simplificada para demonstração)
if modulo == "🏠 Início":
    st.title("Painel Geral da Operação")
    st.metric("Status do Sistema", "Online", delta="Conectado")

elif modulo == "📅 Escala de Trabalho":
    st.title("Calendário de Escala")
    # O calendário dinâmico que montamos antes vai aqui
    st.info("Visualização instantânea da escala diária disponível para Admin.")

elif modulo == "👤 Gestão de Usuários":
    if st.session_state['nivel'] == "Admin":
        st.title("Administração de Usuários")
        st.write("Segregação: Stands, Usuários, Inventário.")
    else:
        st.error("Acesso negado para sua alçada.")
