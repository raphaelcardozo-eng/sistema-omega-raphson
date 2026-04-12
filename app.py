import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime
import calendar

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sistema Integrado Omega & Raphson", 
    layout="wide", 
    page_icon="🏗️"
)

# --- 2. CSS PARA DESIGN AVANÇADO ---
st.markdown("""
    <style>
    /* Estilo do Fundo e Sidebar */
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
    h1 { color: #1e293b; font-family: 'Inter', sans-serif; font-weight: 800; }
    
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
if 'nivel' not in st.session_state:
    st.session_state['nivel'] = "Leitor"

# --- 4. TELA DE LOGIN ---
if not st.session_state['autenticado']:
    st.write("<br><br>", unsafe_allow_html=True)
    
    # Exibição da Logo Composta (Unificada)
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        try:
            img = Image.open("logo_composta.png")
            st.image(img, use_container_width=True)
        except:
            st.title("🏗️ Omega Inc & Raphson Engenharia")

    st.markdown("<h1 style='text-align: center;'>Portal de Gestão Integrada</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>Acesse com suas credenciais para gerenciar a operação.</p>", unsafe_allow_html=True)

    # Card de Login centralizado
    col_c1, col_c2, col_c3 = st.columns([1, 1.2, 1])
    with col_c2:
        with st.form("login_master"):
            u_input = st.text_input("E-mail ou Usuário").strip().lower()
            s_input = st.text_input("Senha", type="password")
            btn_entrar = st.form_submit_button("ENTRAR NO SISTEMA", use_container_width=True)
            
            if btn_entrar:
                # Base de usuários (Podemos expandir para um CSV/Banco depois)
                if (u_input == "admin" or u_input == "raphaelcardozo@raphsonengenharia.com.br") and s_input == "1234":
                    st.session_state['autenticado'] = True
                    st.session_state['user_logado'] = u_input
                    st.session_state['nivel'] = "Admin"
                    st.rerun()
                else:
                    st.error("⚠️ Credenciais inválidas. Verifique usuário e senha.")
    st.stop()

# --- 5. INTERFACE DO SISTEMA (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🧭 Menu de Navegação")
    st.divider()
    
    # Definição dos Setores (Menu Principal)
    menu = st.selectbox(
        "Selecione o Setor:",
        ["🏠 Dashboard", "📅 Escala de Trabalho", "👤 Gestão de Usuários", "🛠️ Manutenção/Stands", "🤝 Comercial"],
        label_visibility="collapsed"
    )
    
    # Espaço vazio para empurrar o rodapé
    st.markdown("<br>" * 10, unsafe_allow_html=True)
    
    # Rodapé da Sidebar (Canto Inferior Esquerdo)
    st.markdown("---")
    st.caption("👤 USUÁRIO LOGADO:")
    st.write(f"**{st.session_state['user_logado']}**")
    st.write(f"🛡️ Nível: {st.session_state['nivel']}")
    
    if st.button("🚪 Sair do Sistema", use_container_width=True):
        st.session_state['autenticado'] = False
        st.rerun()

# --- 6. RENDERIZAÇÃO DOS SETORES ---

if menu == "🏠 Dashboard":
    st.title("📊 Painel Geral de Operações")
    st.write("Visão macro da Omega Inc & Raphson Engenharia.")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Stands Ativos", "14", "+2")
    m2.metric("Equipe em Campo", "28", "Ativo")
    m3.metric("Manutenções Hoje", "3", "-1")
    m4.metric("Propostas Comerciais", "R$ 45k", "+12%")

elif menu == "📅 Escala de Trabalho":
    st.title("📅 Calendário de Escalas")
    st.info("Gerencie os horários e locais de cada colaborador.")
    
    # Exemplo de Calendário
    hoje = datetime.now()
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    c_list = st.columns(7)
    for i, d in enumerate(dias): c_list[i].write(f"**{d}**")
    
    for semana in cal:
        c_list = st.columns(7)
        for i, dia in enumerate(semana):
            if dia != 0:
                c_list[i].button(str(dia), key=f"d_{dia}", use_container_width=True)

elif menu == "👤 Gestão de Usuários":
    st.title("👥 Cadastro e Alçadas")
    if st.session_state['nivel'] == "Admin":
        t1, t2 = st.tabs(["Listar Usuários", "Cadastrar Novo"])
        with t1:
            df_usuarios = pd.DataFrame({
                "Nome": ["Raphael Cardozo", "Suporte Admin"],
                "Email": ["raphaelcardozo@raphsonengenharia.com.br", "admin"],
                "Alçada": ["Diretoria", "Administrador"]
            })
            st.table(df_usuarios)
        with t2:
            with st.form("novo_user"):
                st.text_input("Nome Completo")
                st.text_input("E-mail")
                st.selectbox("Nível de Acesso", ["Admin", "Coordenador", "Operacional"])
                st.form_submit_button("Salvar Usuário")
    else:
        st.warning("Seu nível de acesso não permite gerenciar usuários.")

elif menu == "🛠️ Manutenção/Stands":
    st.title("🛠️ Controle de Stands e Manutenção")
    st.write("Acompanhamento técnico de montagem e reparos.")
    st.selectbox("Filtrar por Stand:", ["Stand Alpha", "Stand Beta", "Evento SP"])
    st.warning("Nenhum chamado de manutenção em aberto.")

elif menu == "🤝 Comercial":
    st.title("🤝 Módulo Comercial")
    st.write("Gestão de contratos e parcerias Omega & Raphson.")
    st.file_uploader("Enviar Proposta (PDF)")
