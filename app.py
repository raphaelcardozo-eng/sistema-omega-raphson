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

# --- 2. TELA DE LOGIN ---
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
        nova_s = st.text_input("Nova Senha", type="password")
        confirma_s = st.text_input("Confirme a Nova Senha", type="password")
        if st.button("Redefinir Senha"):
            if nova_s == confirma_s and nova_s != "":
                st.success("Senha alterada com sucesso! Faça login para acessar.")
            else:
                st.error("As senhas não coincidem.")
    st.stop()

# --- 3. BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    try:
        image = Image.open("logo_empresas.png")
        st.image(image, use_container_width=True)
    except:
        st.title("🏢 OMEGA & RAPHSON")
    
    st.write(f"👤 **Nível:** {st.session_state['nivel']}")
    if st.button("🚪 Sair"):
        logout()
    
    st.divider()
    modulo = st.selectbox("Navegação:", [
        "🏠 Dashboard", 
        "📅 Escala de Trabalho", 
        "👤 Gestão e Cadastros", 
        "🛠️ Manutenção", 
        "🤝 Comercial"
    ])

# --- 4. DASHBOARD ---
if modulo == "🏠 Dashboard":
    st.title("Painel de Gestão Integrada")
    c1, c2, c3 = st.columns(3)
    c1.metric("Stands Ativos", "3", "Jazz, Live, Principal")
    c2.metric("Status Global", "Operacional")
    c3.metric("Alertas", "0")

# --- 5. ESCALA DE TRABALHO (CALENDÁRIO DINÂMICO) ---
elif modulo == "📅 Escala de Trabalho":
    st.title("📅 Escala Mensal")
    hoje = datetime.now()
    ano, mes = hoje.year, hoje.month
    
    st.subheader(f"Competência: {calendar.month_name[mes]} / {ano}")
    
    cal = calendar.monthcalendar(ano, mes)
    dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    cols_h = st.columns(7)
    for i, d in enumerate(dias_semana):
        cols_h[i].write(f"**{d}**")
        
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write(" ")
            else:
                if cols[i].button(str(dia), key=f"dia_{dia}", use_container_width=True):
                    st.info(f"Escala do dia {dia}/{mes}: Sem registros.")

    if st.session_state['nivel'] in ["Admin", "Editor"]:
        st.divider()
        st.subheader("🛠️ Gestão da Escala")
        with st.form("gestao_escala"):
            c_e1, c_e2 = st.columns(2)
            c_e1.date_input("Data")
            c_e1.selectbox("Usuário", ["Raphael Cardozo", "Técnico Silva"])
            c_e2.selectbox("Stand", ["Jazz", "Live", "Principal"])
            if st.form_submit_button("Confirmar Escala"):
                st.success("Escala registrada!")

# --- 6. GESTÃO E CADASTROS (ABAS SEGREGADAS) ---
elif modulo == "👤 Gestão e Cadastros":
    if st.session_state['nivel'] in ["Admin", "Editor"]:
        st.title("👤 Central de Cadastros")
        tab_u, tab_s, tab_i = st.tabs(["👥 Usuários", "Store/Stands", "📦 Inventário"])
        
        with tab_u:
            st.write("### Usuários Ativos")
            df_users = pd.DataFrame({
                "Nome": ["Raphael Cardozo", "Técnico Silva"],
                "Alçada": ["Admin", "Editor"],
                "Setor": ["Diretoria", "Manutenção"]
            })
            st.table(df_users)
            
            with st.expander("➕ Novo Cadastro / Exclusão"):
                with st.form("cad_user"):
                    st.text_input("Nome")
                    st.text_input("E-mail")
                    st.selectbox("Nível", ["Leitor", "Editor", "Admin"])
                    st.password_input("Senha")
                    if st.form_submit_button("Salvar"):
                        st.success("Usuário processado!")
                
                st.divider()
                st.write("### Excluir Usuário")
                email_del = st.text_input("E-mail para excluir")
                if st.button("Confirmar Exclusão"):
                    st.warning(f"Usuário {email_del} removido.")

        with tab_s:
            st.subheader("Gestão de Stands")
            st.write("Lista: Jazz, Live, Principal.")

        with tab_i:
            st.subheader("Controle de Inventário")
            st.info("Espaço para materiais e ferramentas.")
    else:
        st.error("Acesso restrito a Administradores e Editores.")

# --- OUTROS SETORES ---
elif modulo == "🛠️ Manutenção":
    st.title("🛠️ Manutenção")

elif modulo == "🤝 Comercial":
    st.title("🤝 Comercial")
