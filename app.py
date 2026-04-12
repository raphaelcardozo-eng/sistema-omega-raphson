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
if 'user_logado' not in st.session_state:
    st.session_state['user_logado'] = ""

def realizar_login(u, s):
    # Base temporária de usuários
    usuarios_validos = {
        "admin": {"senha": "1234", "nivel": "Admin"},
        "editor": {"senha": "1234", "nivel": "Editor"},
        "raphaelcardozo@raphsonengenharia.com.br": {"senha": "1234", "nivel": "Admin"}
    }
    
    u_clean = u.strip().lower()
    if u_clean in usuarios_validos and s == usuarios_validos[u_clean]["senha"]:
        st.session_state['autenticado'] = True
        st.session_state['nivel'] = usuarios_validos[u_clean]["nivel"]
        st.session_state['user_logado'] = u_clean
        st.rerun()
    else:
        st.error("Usuário ou senha incorretos.")

def realizar_logout():
    st.session_state['autenticado'] = False
    st.rerun()

# --- 2. TELA DE ENTRADA ---
if not st.session_state['autenticado']:
    # Responsividade das Logos
    col_l1, col_l2, col_l3, col_l4 = st.columns([1, 2, 2, 1])
    
    with col_l2:
        try:
            logo_raphson = Image.open("LOGO RAPHSON FUNDO TRANSPARENTE.png")
            st.image(logo_raphson, use_container_width=True)
        except:
            st.write("Logo Raphson")
            
    with col_l3:
        try:
            logo_omega = Image.open("omega inc.png")
            st.image(logo_omega, use_container_width=True)
        except:
            st.write("Logo Omega")

    st.markdown("<h1 style='text-align: center;'>Sistema Integrado Omega & Raphson</h1>", unsafe_allow_html=True)
    
    t_login, t_reset = st.tabs(["🔐 Acesso", "🔑 Esqueci a Senha"])
    
    with t_login:
        with st.form("login_form"):
            u_input = st.text_input("Usuário (E-mail)")
            s_input = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar", use_container_width=True):
                realizar_login(u_input, s_input)
                
    with t_reset:
        st.subheader("Recuperação de Acesso")
        email_rec = st.text_input("Digite seu e-mail cadastrado")
        if st.button("Enviar link de redefinição", use_container_width=True):
            st.success(f"Instruções enviadas para {email_rec}")
    st.stop()

# --- 3. BARRA LATERAL (PÓS-LOGIN) ---
with st.sidebar:
    # Exibe logos menores no menu lateral
    c_s1, c_s2 = st.columns(2)
    with c_s1:
        st.image("LOGO RAPHSON FUNDO TRANSPARENTE.png", use_container_width=True)
    with c_s2:
        st.image("omega inc.png", use_container_width=True)
        
    st.write(f"👤 **Logado:** {st.session_state['user_logado']}")
    if st.button("🚪 Sair", use_container_width=True):
        realizar_logout()
    
    st.divider()
    modulo = st.selectbox("Navegação:", ["🏠 Dashboard", "📅 Escala de Trabalho", "👤 Gestão e Cadastros", "🛠️ Manutenção", "🤝 Comercial"])

# --- 4. DASHBOARD ---
if modulo == "🏠 Dashboard":
    st.title("Painel de Gestão Integrada")
    st.info("Bem-vindo ao sistema unificado.")

# --- 5. ESCALA DE TRABALHO ---
elif modulo == "📅 Escala de Trabalho":
    st.title("📅 Calendário de Escalas")
    hoje = datetime.now()
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    
    cols_h = st.columns(7)
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    for i, d in enumerate(dias): cols_h[i].write(f"**{d}**")
        
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia != 0:
                if cols[i].button(str(dia), key=f"d_{dia}", use_container_width=True):
                    st.toast(f"Dia {dia} selecionado.")

# --- 6. GESTÃO E CADASTROS ---
elif modulo == "👤 Gestão e Cadastros":
    if st.session_state['nivel'] in ["Admin", "Editor"]:
        st.title("👤 Administração")
        tab_u, tab_s, tab_i = st.tabs(["👥 Usuários", "🏢 Stands", "📦 Inventário"])
        
        with tab_u:
            st.write("### Base de Usuários")
            st.table(pd.DataFrame({
                "Nome": ["Raphael Cardozo", "Técnico Silva"],
                "E-mail": ["raphaelcardozo@raphsonengenharia.com.br", "silva@omega.com"],
                "Nível": ["Admin", "Editor"]
            }))
    else:
        st.error("Acesso restrito.")
