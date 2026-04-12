import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- CONFIGURAÇÃO DA PÁGINA (Sempre a primeira linha de código) ---
st.set_page_config(
    page_title="Gestão Omega & Raphson", 
    layout="wide", 
    page_icon="🏗️"
)

# --- CSS PARA DESIGN PROFISSIONAL E RESPONSIVO ---
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 45px; 
        background-color: #ffffff; 
        border-radius: 8px; 
        padding: 0px 20px;
    }
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; text-align: center; }
    p { color: #64748b; text-align: center; }
    .stForm { border-radius: 15px; background-color: white; padding: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. INICIALIZAÇÃO DO ESTADO DE SESSÃO (Evita o erro de NameError) ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"
if 'user_logado' not in st.session_state:
    st.session_state['user_logado'] = ""

# --- FUNÇÃO DE LOGIN ---
def realizar_login(u, s):
    usuarios_validos = {
        "admin": {"senha": "1234", "nivel": "Admin"},
        "raphaelcardozo@raphsonengenharia.com.br": {"senha": "1234", "nivel": "Admin"}
    }
    u_clean = u.strip().lower()
    if u_clean in usuarios_validos and s == usuarios_validos[u_clean]["senha"]:
        st.session_state['autenticado'] = True
        st.session_state['nivel'] = usuarios_validos[u_clean]["nivel"]
        st.session_state['user_logado'] = u_clean
        st.rerun()
    else:
        st.error("⚠️ Credenciais inválidas.")

# --- 2. TELA DE LOGIN (COM A NOVA LOGO UNIFICADA) ---
if not st.session_state['autenticado']:
    st.write("<br>", unsafe_allow_html=True)
    
    # Centralização da Logo Única (Substituindo as duas anteriores)
    col_e, col_logo, col_d = st.columns([1, 2, 1])
    with col_logo:
        try:
            # Certifique-se de que o nome no GitHub seja logo_composta.png
            img_composta = Image.open("logo_composta.png")
            st.image(img_composta, use_container_width=True)
        except:
            st.info("📌 Identidade Visual: Gestão Integrada Omega & Raphson")

    st.markdown("<h1>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size
