import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Gestão Omega & Raphson", 
    layout="wide", 
    page_icon="🏗️"
)

# --- 2. CSS PARA POSICIONAMENTO (USUÁRIO NO RODAPÉ) ---
st.markdown("""
    <style>
    /* Estilização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
    }
    
    /* Container para empurrar o conteúdo para o rodapé */
    .sidebar-content {
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    /* Estilo do Usuário e Botão Sair no Rodapé */
    .footer-user {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: 220px;
        font-size: 0.8rem;
        color: #64748b;
        border-top: 1px solid #e2e8f0;
        padding-top: 10px;
    }

    /* Ajuste de títulos e formulários */
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; text-align: center; }
    .stForm { border-radius: 15px; background-color: white; padding: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'user_logado' not in st.session_state:
    st.session_state['user_logado'] = ""

# --- 4. TELA DE LOGIN ---
if not st.session_state['autenticado']:
    st.write("<br>", unsafe_allow_html=True)
    
    # Logo Unificada
    col_e, col_logo, col_d = st.columns([1, 2, 1])
    with col_logo:
        try:
            img_composta = Image.open("logo_composta.png")
            st.image(img_composta, use_container_width=True)
        except:
            st.info("📌 Gestão Integrada Omega Inc & Raphson Engenharia")

    st.markdown("<h1>Portal de Gestão Integrada</h1>", unsafe_allow_html=True)
    
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        with st.form("login_form"):
            u_input = st.text_input("Usuário ou E-mail").strip().lower()
            s_input = st.text_input("Senha", type="password")
            if st.form_submit_button("ACESSAR PAINEL", use_container_width=True):
                # Credenciais autorizadas
                if (u_input == "admin" or u_input == "raphaelcardozo@raphsonengenharia.com.br") and s_input == "1234":
                    st.session_state['autenticado'] = True
                    st.session_state['user_logado'] = u_input
                    st.rerun()
                else:
                    st.error("⚠️ Credenciais inválidas.")
    st.stop()

# --- 5. INTERFACE INTERNA (SIDEBAR E MENU) ---
with st.sidebar:
    # Topo da Sidebar: Logo ou Nome
    st.markdown("### 🏗️ Menu Principal")
    st.divider()
    
    # Seletor de Menu
