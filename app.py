import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- 1. CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira instrução) ---
st.set_page_config(
    page_title="Gestão Omega & Raphson", 
    layout="wide", 
    page_icon="🏗️"
)

# --- 2. INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"
if 'user_logado' not in st.session_state:
    st.session_state['user_logado'] = ""

# --- 3. CSS PARA DESIGN PROFISSIONAL ---
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
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; text-align: center; margin-bottom: 0px; }
    .boas-vindas { color: #64748b; text-align: center; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px; }
    .stForm { border-radius: 15px; background-color: white; padding: 20px; box-shadow: 0px 4px 12px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

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

# --- 4. TELA DE LOGIN ---
if not st.session_state['autenticado']:
    st.write("<br>", unsafe_allow_html=True)
    
    # Centralização da Logo Unificada
    col_e, col_logo, col_d = st.columns([1, 2, 1])
    with col_logo:
        try:
            # Tenta carregar a imagem que você gerou
            img_composta = Image.open("logo_composta.png")
            st.image(img_composta, use_container_width=True)
        except:
            st.info("📌 Carregando Identidade Visual...")

    # Títulos e Mensagem de Boas-Vindas
    st.markdown("<h1>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p class='boas-vindas'>Bem-vindo ao portal administrativo. Identifique-se para continuar.</p>", unsafe_allow_html=True)

    # Card de Login
    col_c1, col_c2, col_c3 = st.columns([1, 1.5, 1])
    with col_c2:
        tab_login, tab_reset = st.tabs(["🔐 Acesso", "🔑 Esqueci a Senha"])
        
        with tab_login:
            with st.form("login_form_final"):
                u_input = st.text_input("Usuário ou E-mail")
                s_input = st.text_input("Senha", type="password")
                if st.form_submit_button("ACESSAR PAINEL", use_container_width=True):
                    realizar_login(u_input, s_input)
        
        with tab_reset:
            st.write("### Recuperação de Acesso")
            st.info("Por favor, contate o suporte técnico da Raphson Engenharia para redefinir sua senha.")
    st.stop()

# --- 5. INTERFACE INTERNA (APÓS LOGIN) ---
with st.sidebar:
    try:
        st.image("logo_composta.png", use_container_width=True)
    except:
        st.subheader("Omega & Raphson")
        
    st.write(f"👤 **Usuário:** {st.session_state['user_logado']}")
    if st.button("🚪 Sair"):
        st.session_state['autenticado'] = False
        st.rerun()
    st.divider()
    modulo = st.selectbox("Navegação:", ["🏠 Dashboard", "📅 Escala", "👤 Gestão"])

# Renderização básica dos módulos
if modulo == "🏠 Dashboard":
    st.title("Painel Geral de Operações")
    st.write("Bem-vindo ao centro de controle.")
elif modulo == "📅 Escala":
    st.title("Escala de Trabalho")
    st.info("Módulo de escala em desenvolvimento.")
elif modulo == "👤 Gestão":
    st.title("Gestão de Usuários")
    st.write("Área administrativa.")
