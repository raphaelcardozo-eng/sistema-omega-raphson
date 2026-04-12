import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
import calendar
import os

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Gestão Integrada Omega & Raphson",
    layout="wide",
    page_icon="🏗️"
)

# ============================================================
# 2. CSS - DESIGN PROFISSIONAL E RESPONSIVO
# ============================================================
st.markdown("""
    <style>
    /* Fundo geral */
    .main { background-color: #f0f4f8; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a2332;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #94a3b8 !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stSidebar"] hr {
        border-color: #2d3748 !important;
    }

    /* Cards de métricas */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #3b82f6;
    }

    /* Botões */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }

    /* Formulários */
    .stForm {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }

    /* Título principal */
    h1 { color: #1e293b !important; }
    h2 { color: #334155 !important; }
    h3 { color: #475569 !important; }

    /* Tabelas */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Responsividade mobile */
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem; }
        [data-testid="stMetric"] { margin-bottom: 8px; }
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# 3. INICIALIZAÇÃO DO SESSION STATE
# ============================================================
defaults = {
    'autenticado': False,
    'user_logado': '',
    'nivel': 'Leitor',
    'nome_usuario': ''
}
for chave, valor in defaults.items():
    if chave not in st.session_state:
        st.session_state[chave] = valor

# ============================================================
# 4. BANCO DE DADOS LOCAL (CSV) - TEMPORÁRIO ATÉ INTEGRAR SHEETS
# ============================================================
ARQUIVOS = {
    'usuarios':    'db_usuarios.csv',
    'manutencao':  'db_manutencao.csv',
    'comercial':   'db_comercial.csv',
    'escala':      'db_escala.csv',
    'financeiro':  'db_financeiro.csv',
    'marketing':   'db_marketing.csv',
    'compras':     'db_compras.csv',
    'stands':      'db_stands.csv',
    'inventario':  'db_inventario.csv',
}

COLUNAS = {
    'usuarios':   ['ID','Nome','Email','Senha','Setor','Nivel','Ativo'],
    'manutencao': ['ID','Data','Stand','Descricao','Responsavel','Urgencia','Status'],
    'comercial':  ['ID','Data','Cliente','Contato','Stand','Produto','Etapa','Responsavel','Obs'],
    'escala':     ['ID','Data','DiaSemana','Colaborador','Setor','Stand','Turno','Status'],
    'financeiro': ['ID','Data','Tipo','Categoria','Descricao','Valor','Responsavel'],
    'marketing':  ['ID','Data','Campanha','Tipo','Responsavel','Stand','Status','Prazo'],
    'compras':    ['ID','Data','Item','Quantidade','Unidade','Solicitante','Setor','Urgencia','Status'],
    'stands':     ['ID','Nome','Endereco','Status','Responsavel'],
    'inventario': ['ID','Item','Categoria','Quantidade','Unidade','Stand','Status'],
}

def carregar(modulo):
    arq = ARQUIVOS[modulo]
    if os.path.exists(arq):
        return pd.read_csv(arq)
    return pd.DataFrame(columns=COLUNAS[modulo])

def salvar(df, modulo):
    df.to_csv(ARQUIVOS[modulo], index=False)

def proximo_id(df):
    if df.empty:
        return 1
    return int(df['ID'].max()) + 1

# ============================================================
# 5. SEED — USUÁRIO ADMIN PADRÃO
# ============================================================
def garantir_admin():
    df = carregar('usuarios')
    if df.empty or not (df['Email'] == 'raphaelcardozo@raphsonengenharia.com.br').any():
        novo = pd.DataFrame([[
            1, 'Raphael Cardozo',
            'raphaelcardozo@raphsonengenharia.com.br',
            '1234', 'Diretoria', 'Admin', 'Sim'
        ]], columns=COLUNAS['usuarios'])
        df = pd.concat([df, novo], ignore_index=True)
        salvar(df, 'usuarios')

garantir_admin()

# ============================================================
# 6. SEED — STANDS PADRÃO
# ============================================================
def garantir_stands():
    df = carregar('stands')
    if df.empty:
        stands_iniciais = [
            [1, 'Stand Principal', 'Endereço Principal', 'Ativo', 'Raphael Cardozo'],
            [2, 'Stand Jazz',      'Endereço Jazz',      'Ativo', 'A definir'],
            [3, 'Stand Live',      'Endereço Live',      'Ativo', 'A definir'],
        ]
        df = pd.DataFrame(stands_iniciais, columns=COLUNAS['stands'])
        salvar(df, 'stands')

garantir_stands()

# ============================================================
# 7. FUNÇÕES DE AUTENTICAÇÃO
# ============================================================
def realizar_login(email, senha):
    df = carregar('usuarios')
    usuario = df[
        (df['Email'].str.strip().str.lower() == email.strip().lower()) &
        (df['Senha'].astype(str) == str(senha)) &
        (df['Ativo'] == 'Sim')
    ]
    if not usuario.empty:
        row = usuario.iloc[0]
        st.session_state['autenticado']  = True
        st.session_state['user_logado']  = row['Email']
        st.session_state['nome_usuario'] = row['Nome']
        st.session_state['nivel']        = row['Nivel']
        st.rerun()
    else:
        st.error("⚠️ E-mail ou senha incorretos, ou usuário inativo.")

def realizar_logout():
    for k in ['autenticado', 'user_logado', 'nome_usuario', 'nivel']:
        st.session_state[k] = defaults[k]
    st.rerun()

# ============================================================
# 8. TELA DE LOGIN
# ============================================================
if not st.session_state['autenticado']:
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Logo
    col_a, col_logo, col_b = st.columns([1, 2, 1])
    with col_logo:
        try:
            st.image(Image.open("logo_final.png"), use_container_width=True)
        except:
            st.markdown(
                "<h2 style='text-align:center;'>🏗️ Omega Inc & Raphson Engenharia</h2>",
                unsafe_allow_html=True
            )

    st.markdown(
        "<h1 style='text-align:center; margin-top:10px;'>"
        "Gestão Integrada Omega Inc & Raphson Engenharia</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#64748b; font-size:1.1rem;'>"
        "Bem-vindo ao portal administrativo. Identifique-se para continuar.</p>",
        unsafe_allow_html=True
    )

    # Card de login
    col_x, col_form, col_y = st.columns([1, 1.4, 1])
    with col_form:
        tab_login, tab_reset = st.tabs(["🔐 Acesso ao Sistema", "🔑 Esqueci minha Senha"])

        with tab_login:
            with st.form("form_login"):
                email_in = st.text_input("E-mail corporativo")
                senha_in = st.text_input("Senha", type="password")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ENTRAR NO SISTEMA", use_container_width=True):
                    if email_in and senha_in:
                        realizar_login(email_in, senha_in)
                    else:
                        st.warning("Preencha todos os campos.")

        with tab_reset:
            st.markdown("#### Redefinir Senha")
            email_rst  = st.text_input("Seu e-mail cadastrado")
            nova_senha = st.text_input("Nova senha", type="password")
            conf_senha = st.text_input("Confirme a nova senha", type="password")
            if st.button("Redefinir Senha", use_container_width=True):
                if not email_rst:
                    st.warning("Informe o e-mail.")
                elif nova_senha != conf_senha:
                    st.error("As senhas não coincidem.")
                else:
                    df_u = carregar('usuarios')
                    mask = df_u['Email'].str.strip().str.lower() == email_rst.strip().lower()
                    if mask.any():
                        df_u.loc[mask, 'Senha'] = nova_senha
                        salvar(df_u, 'usuarios')
                        st.success("✅ Senha atualizada! Faça login com a nova senha.")
                    else:
                        st.error("E-mail não encontrado.")
    st.stop()

# ============================================================
# 9. SIDEBAR — NAVEGAÇÃO INTERNA
# ============================================================
with st.sidebar:
    try:
        st.image(Image.open("logo_final.png"), use_container_width=True)
    except:
        st.markdown("### 🏗️ Omega & Raphson")

    st.markdown("---")
    st.markdown("### 🧭 Menu")

    NIVEL = st.session_state['nivel']

    # Monta opções conforme alçada
    opcoes_menu = ["🏠 Dashboard", "📅 Escala de Trabalho", "🛠️ Manutenção", "🤝 Comercial"]
    if NIVEL in ['Admin', 'Editor']:
        opcoes_menu += ["💰 Financeiro", "📣 Marketing", "🛒 Compras"]
    if NIVEL == 'Admin':
        opcoes_menu += ["⚙️ Cadastros & Configurações"]

    modulo = st.selectbox("", opcoes_menu, label_visibility="collapsed")

    # Espaço empurrando rodapé para baixo
    st.markdown("<br>" * 8, unsafe_allow_html=True)
    st.markdown("---")
    st.caption(f"👤 {st.session_state['nome_usuario']}")
    st.caption(f"🛡️ Nível: {NIVEL}")
    if st.button("🚪 Sair", use_container_width=True):
        realizar_logout()

# ============================================================
# 10. HELPERS VISUAIS
# ============================================================
def badge_urgencia(u):
    cores = {"Alta": "🔴", "Média": "🟡", "Baixa": "🟢"}
    return cores.get(u, "⚪")

def badge_status(s):
    cores = {
        "Pendente":    "🟠",
        "Em Andamento":"🔵",
        "Concluído":   "🟢",
        "Cancelado":   "⚫"
    }
    return cores.get(s, "⚪")

def get_stands():
    df = carregar('stands')
    return df[df['Status'] == 'Ativo']['Nome'].tolist() if not df.empty else ['Stand Principal']

def get_usuarios_ativos():
    df = carregar('usuarios')
    return df[df['Ativo'] == 'Sim']['Nome'].tolist() if not df.empty else ['Sem colaboradores']

# ============================================================
# 11. MÓDULO — DASHBOARD
# ============================================================
if modulo == "🏠 Dashboard":
    st.title("📊 Painel de Gestão Integrada")
    st.markdown(f"Bem-vindo, **{st.session_state['nome_usuario']}**! Aqui está a visão geral da operação.")
    st.markdown("---")

    # Métricas dinâmicas
    df_man  = carregar('manutencao')
    df_com  = carregar('comercial')
    df_esc  = carregar('escala')
    df_sta  = carregar('stands')
    df_usr  = carregar('usuarios')

    col1, col2, col3, col4 = st.columns(4)
    stands_ativos = len(df_sta[df_sta['Status'] == 'Ativo']) if not df_sta.empty else 0
    man_pendentes = len(df_man[df_man['Status'] == 'Pendente']) if not df_man.empty else 0
    escalas_hoje  = len(df_esc[df_esc['Data'] == str(date.today())]) if not df_esc.empty else 0
    usuarios_atv  = len(df_usr[df_usr['Ativo'] == 'Sim']) if not df_usr.empty else 0

    col1.metric("🏪 Stands Ativos",       stands_ativos)
    col2.metric("🛠️ Manutenções Pendentes", man_pendentes)
    col3.metric("📅 Escalas Hoje",         escalas_hoje)
    col4.metric("👥 Usuários Ativos",      usuarios_atv)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🛠️ Últimas Manutenções")
        if not df_man.empty:
            st.dataframe(
                df_man[['ID','Data','Stand','Descricao','Status']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma manutenção registrada.")

    with col_b:
        st.markdown("#### 🤝 Últimas Negociações")
        if not df_com.empty:
            st.dataframe(
                df_com[['ID','Data','Cliente','Stand','Etapa']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma negociação registrada.")

# ============================================================
# 12. MÓDULO — ESCALA DE TRABALHO
# ============================================================
elif modulo == "📅 Escala de Trabalho":
    st.title("📅 Escala de Trabalho")

    hoje   = datetime.now()
    ano    = hoje.year
    mes    = hoje.month
    df_esc = carregar('escala')

    st.subheader(f"📆 {calendar.month_name[mes]} / {ano}")

    # Calendário visual
    cal = calendar.monthcalendar(ano, mes)
    nomes_dias = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

    cabecalho = st.columns(7)
    for i, nome in enumerate(nomes_dias):
        cabecalho[i].markdown(f"**{nome}**")

    dia_selecionado = None
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                # Verifica se há escala nesse dia
                data_str = f"{ano}-{mes:02d}-{dia:02d}"
                tem_escala = (
                    not

