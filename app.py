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

# --- 2. CSS PARA DESIGN AVANÇADO ---
st.markdown("""
    <style>
    /* Estilo do Fundo */
    .main { background-color: #f8fafc; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Centralização e Design do Formulário de Login */
    .stForm { 
        border-radius: 15px; 
        background-color: white; 
        padding: 30px; 
        box-shadow: 0px 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #f1f5f9;
    }
    
    /* Títulos */
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; text-align: center; }
    p { color: #64748b; text-align: center; font-size: 1.1rem; }
    
    /* Rodapé da Sidebar (Usuário e Sair) */
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        width: 260px;
        padding: 15px;
        background-color: #f8fafc;
        border-top: 1px solid #e2e8f0;
        font-size: 0.8rem;
    }
    
    /* Botão Sair Estilizado */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. INICIALIZAÇÃO DO ESTADO DE SESSÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'user_logado' not in st.session_state:
    st.session_state['user_logado'] = ""

# --- FUNÇÃO DE LOGIN ---
def realizar_login(u, s):
    # Base de acesso autorizada
    usuarios_validos = {
        "admin": "1234",
        "raphaelcardozo@raphsonengenharia.com.br": "1234"
    }
    u_clean = u.strip().lower()
    if u_clean in usuarios_validos and s == usuarios_validos[u_clean]:
        st.session_state['autenticado'] = True
        st.session_state['user_logado'] = u_clean
        st.rerun()
    else:
        st.error("⚠️ Credenciais incorretas.")

# --- 4. TELA DE ENTRADA (PAINEL DE LOGIN) ---
if not st.session_state['autenticado']:
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Exibição da NOVA Logo Final Centralizada
    col_e, col_logo, col_d = st.columns([1, 2, 1])
    with col_logo:
        try:
            # Carrega a imagem composta que você gerou
            img_final = Image.open("logo_final.png")
            st.image(img_final, use_container_width=True)
        except:
            st.warning("⚠️ Arquivo 'logo_final.png' não encontrado no repositório.")

    # Títulos e Mensagem
    st.markdown("<h1>Gestão Integrada Omega Inc & Raphson Engenharia</h1>", unsafe_allow_html=True)
    st.markdown("<p>Bem-vindo ao portal administrativo. Identifique-se para continuar.</p>", unsafe_allow_html=True)

    # Card de Login centralizado
    col_c1, col_c2, col_c3 = st.columns([1, 1.2, 1])
    with col_c2:
        with st.form("login_moderno"):
            u_input = st.text_input("Usuário ou E-mail")
            s_input = st.text_input("Senha", type="password")
            st.write("<br>", unsafe_allow_html=True)
            if st.form_submit_button("ACESSAR PAINEL", use_container_width=True):
                realizar_login(u_input, s_input)
    st.stop()

# --- 5. INTERFACE INTERNA (APÓS LOGIN) ---
with st.sidebar:
    # Exibição da Logo Final na barra lateral
    try:
        st.image("logo_final.png", use_container_width=True)
    except:
        st.title("🏗️ Omega & Raphson")
    
    st.divider()
    
    # Menu Principal com todos os setores
    st.markdown("### 🧭 Menu")
    modulo = st.selectbox(
        "Selecione o Setor:",
        ["🏠 Dashboard", "📅 Escala de Trabalho", "👤 Gestão de Usuários", "🛠️ Manutenção", "🤝 Comercial"],
        label_visibility="collapsed"
    )
    
    # Rodapé da Sidebar (Canto Inferior Esquerdo)
    st.markdown("---")
    st.caption("👤 USUÁRIO LOGADO:")
    st.write(f"**{st.session_state['user_logado']}**")
    
    if st.button("🚪 Sair do Sistema", use_container_width=True):
        st.session_state['autenticado'] = False
        st.rerun()

# --- 6. RENDERIZAÇÃO DOS SETORES ---
if modulo == "🏠 Dashboard":
    st.title("Painel Geral de Operações")
    st.write("Acesso confirmado. Bem-vindo ao sistema!")

elif modulo == "📅 Escala de Trabalho":
    st.title("Escala de Trabalho")

elif modulo == "👤 Gestão de Usuários":
    st.title("Gestão de Usuários")

elif modulo == "🛠️ Manutenção":
    st.title("Manutenção de Stands")

elif modulo == "🤝 Comercial":
    st.title("Módulo Comercial")
