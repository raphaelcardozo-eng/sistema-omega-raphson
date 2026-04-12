import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
import calendar
import os
import base64

st.set_page_config(
    page_title="Gestão Integrada Omega & Raphson",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.main { background: linear-gradient(135deg, #f0f4ff 0%, #fafbff 100%); min-height: 100vh; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1400px; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 0.75rem 0; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] label {
    color: #94a3b8 !important; font-size: 0.7rem !important;
    font-weight: 600 !important; text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
.menu-label {
    color: #64748b !important; font-size: 0.65rem !important;
    font-weight: 700 !important; text-transform: uppercase !important;
    letter-spacing: 0.12em !important; padding: 0.5rem 0 0.25rem 0; display: block;
}
.user-footer {
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px; padding: 12px 14px; margin-top: 8px;
}
.user-name { color: #f1f5f9 !important; font-weight: 600; font-size: 0.88rem; }
.user-level { color: #64748b !important; font-size: 0.75rem; }
h1 { color: #0f172a !important; font-weight: 800 !important; font-size: 1.85rem !important; letter-spacing: -0.02em; margin-bottom: 0.15rem !important; }
h2 { color: #1e293b !important; font-weight: 700 !important; font-size: 1.3rem !important; }
h3 { color: #334155 !important; font-weight: 600 !important; font-size: 1.05rem !important; }
.page-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
    border-radius: 16px; padding: 1.5rem 2rem; margin-bottom: 1.75rem;
    display: flex; align-items: center; gap: 1rem;
    box-shadow: 0 8px 32px rgba(30,58,138,0.25);
}
.page-header-icon { font-size: 2.2rem; line-height: 1; }
.page-header-title { color: #ffffff !important; font-size: 1.6rem !important; font-weight: 800 !important; margin: 0 !important; }
.page-header-sub { color: rgba(255,255,255,0.72) !important; font-size: 0.88rem; margin-top: 2px; }
[data-testid="stMetric"] {
    background: #ffffff !important; border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important; box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    border: 1px solid #e2e8f0 !important; border-top: 4px solid #3b82f6 !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(59,130,246,0.15) !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; font-weight: 600 !important; color: #64748b !important; text-transform: uppercase; }
[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 800 !important; color: #0f172a !important; }
[data-testid="stForm"] {
    background: #ffffff; border-radius: 16px; padding: 1.75rem;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    border-radius: 10px !important; border: 1.5px solid #e2e8f0 !important; font-size: 0.9rem !important;
}
.stButton > button {
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1.25rem !important;
    transition: all 0.2s !important; border: none !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #f1f5f9; border-radius: 12px; padding: 4px; gap: 4px; border-bottom: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px !important; font-weight: 600 !important; font-size: 0.85rem !important;
    color: #64748b !important; padding: 0.45rem 1.1rem !important; border: none !important; background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important; color: #1d4ed8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; }
[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; font-weight: 500; }
[data-testid="stExpander"] { background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0 !important; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.25rem 0; }
.custom-card {
    background: #ffffff; border-radius: 14px; padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.os-card {
    background: #ffffff; border-radius: 14px; padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0; border-left: 5px solid #3b82f6;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 1rem;
}
.os-card-alta  { border-left-color: #ef4444 !important; }
.os-card-media { border-left-color: #f59e0b !important; }
.os-card-baixa { border-left-color: #22c55e !important; }
.status-badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.03em;
}
.badge-pendente  { background: #fef3c7; color: #92400e; }
.badge-andamento { background: #dbeafe; color: #1e40af; }
.badge-material  { background: #ede9fe; color: #5b21b6; }
.badge-concluido { background: #dcfce7; color: #166534; }
.badge-cancelado { background: #fee2e2; color: #991b1b; }
.login-title { text-align: center; color: #0f172a !important; font-size: 1.5rem !important; font-weight: 800 !important; }
.login-sub { text-align: center; color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }
.foto-label { font-size: 0.78rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
@media (max-width: 768px) {
    .block-container { padding: 1rem 1rem 2rem !important; }
    .page-header { padding: 1rem 1.25rem; border-radius: 12px; }
    .page-header-title { font-size: 1.2rem !important; }
    [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
    h1 { font-size: 1.4rem !important; }
    .os-card { padding: 1rem; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    'autenticado': False,
    'user_logado': '',
    'nivel': 'Leitor',
    'nome_usuario': '',
    'man_form_key': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# BANCO DE DADOS
# ============================================================
ARQUIVOS = {
    'usuarios': 'db_usuarios.csv',
    'manutencao': 'db_manutencao.csv',
    'comercial': 'db_comercial.csv',
    'escala': 'db_escala.csv',
    'financeiro': 'db_financeiro.csv',
    'marketing': 'db_marketing.csv',
    'compras': 'db_compras.csv',
    'stands': 'db_stands.csv',
    'inventario': 'db_inventario.csv',
}
COLUNAS = {
    'usuarios': ['ID', 'Nome', 'Email', 'Senha', 'Setor', 'Funcao', 'Nivel', 'Ativo'],
    'manutencao': ['ID', 'Data', 'Stand', 'Descricao', 'Responsavel', 'Urgencia',
                   'Status', 'Prazo', 'FotoAntes', 'FotoDepois', 'PedidoCompras', 'Obs'],
    'comercial': ['ID', 'Data', 'Cliente', 'Contato', 'Stand', 'Produto', 'Etapa', 'Responsavel', 'Obs'],
    'escala': ['ID', 'Data', 'DiaSemana', 'Colaborador', 'Setor', 'Stand', 'Turno', 'Status'],
    'financeiro': ['ID', 'Data', 'Tipo', 'Categoria', 'Descricao', 'Valor', 'Responsavel'],
    'marketing': ['ID', 'Data', 'Campanha', 'Tipo', 'Responsavel', 'Stand', 'Status', 'Prazo'],
    'compras': ['ID', 'Data', 'Item', 'Quantidade', 'Unidade', 'Solicitante',
                'Setor', 'Urgencia', 'Status', 'OrigemChamadoID'],
    'stands': ['ID', 'Nome', 'Endereco', 'Status', 'Responsavel'],
    'inventario': ['ID', 'Item', 'Categoria', 'Quantidade', 'Unidade', 'Stand', 'Estado', 'Propriedade'],
}


def carregar(modulo):
    arq = ARQUIVOS[modulo]
    if os.path.exists(arq):
        df = pd.read_csv(arq)
        for col in COLUNAS[modulo]:
            if col not in df.columns:
                df[col] = ''
        return df
    return pd.DataFrame(columns=COLUNAS[modulo])


def salvar(df, modulo):
    df.to_csv(ARQUIVOS[modulo], index=False)


def proximo_id(df):
    if df.empty:
        return 1
    return int(df['ID'].max()) + 1


def get_stands():
    df = carregar('stands')
    ativos = df[df['Status'] == 'Ativo']['Nome'].tolist()
    return ativos if ativos else ['Stand Principal']


def get_usuarios_ativos():
    df = carregar('usuarios')
    ativos = df[df['Ativo'] == 'Sim']['Nome'].tolist()
    return ativos if ativos else ['Sem colaboradores']


def encode_img(uploaded_file):
    if uploaded_file is not None:
        return base64.b64encode(uploaded_file.read()).decode()
    return ''


def decode_img(b64str):
    if b64str and isinstance(b64str, str) and len(b64str) > 10:
        try:
            return base64.b64decode(b64str)
        except Exception:
            return None
    return None


# ============================================================
# SEEDS
# ============================================================
def garantir_admin():
    df = carregar('usuarios')
    if df.empty or not (df['Email'].str.lower() == 'raphaelcardozo@raphsonengenharia.com.br').any():
        novo = pd.DataFrame([[
            1, 'Raphael Cardozo', 'raphaelcardozo@raphsonengenharia.com.br',
            '1234', 'Diretoria', 'Diretor', 'Admin', 'Sim'
        ]], columns=COLUNAS['usuarios'])
        df = pd.concat([df, novo], ignore_index=True)
        salvar(df, 'usuarios')


def garantir_stands():
    df = carregar('stands')
    if df.empty:
        dados = [
            [1, 'Stand Principal', 'Endereco Principal', 'Ativo', 'Raphael Cardozo'],
            [2, 'Stand Jazz', 'Endereco Jazz', 'Ativo', 'A definir'],
            [3, 'Stand Live', 'Endereco Live', 'Ativo', 'A definir'],
        ]
        salvar(pd.DataFrame(dados, columns=COLUNAS['stands']), 'stands')


garantir_admin()
garantir_stands()


# ============================================================
# AUTENTICACAO
# ============================================================
def realizar_login(email, senha):
    df = carregar('usuarios')
    ok = df[
        (df['Email'].str.strip().str.lower() == email.strip().lower()) &
        (df['Senha'].astype(str) == str(senha)) &
        (df['Ativo'] == 'Sim')
    ]
    if not ok.empty:
        row = ok.iloc[0]
        st.session_state.update({
            'autenticado': True,
            'user_logado': row['Email'],
            'nome_usuario': row['Nome'],
            'nivel': row['Nivel']
        })
        st.rerun()
    else:
        st.error("E-mail ou senha incorretos, ou usuario inativo.")


def realizar_logout():
    st.session_state.update(defaults)
    st.rerun()


# ============================================================
# TELA DE LOGIN
# ============================================================
if not st.session_state['autenticado']:
    st.markdown("<br><br>", unsafe_allow_html=True)
    cl, cc, cr = st.columns([1, 2, 1])
    with cc:
        try:
            st.image(Image.open("logo_final.png"), use_container_width=True)
        except:
            st.markdown(
                "<h2 style='text-align:center;color:#1e3a8a;'>Omega Inc & Raphson Engenharia</h2>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    cl2, cc2, cr2 = st.columns([1, 1.3, 1])
    with cc2:
        st.markdown(
            "<div style='background:#fff;border-radius:20px;padding:2.5rem 2rem;"
            "box-shadow:0 20px 60px rgba(0,0,0,0.10);border:1px solid #e2e8f0;'>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p class='login-title'>Gestao Integrada</p>"
            "<p class='login-sub'>Omega Inc & Raphson Engenharia<br>"
            "Identifique-se para acessar o painel.</p>",
            unsafe_allow_html=True
        )

        tab_login, tab_reset = st.tabs(["Entrar", "Esqueci a Senha"])

        with tab_login:
            with st.form("form_login", clear_on_submit=False):
                email_in = st.text_input("E-mail corporativo", placeholder="seu@email.com.br")
                senha_in = st.text_input("Senha", type="password", placeholder="senha")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ACESSAR O PAINEL", use_container_width=True):
                    if email_in and senha_in:
                        realizar_login(email_in, senha_in)
                    else:
                        st.warning("Preencha todos os campos.")

        with tab_reset:
            st.markdown("<br>", unsafe_allow_html=True)
            email_rst = st.text_input("E-mail cadastrado", key="rst_email")
            nova_senha = st.text_input("Nova senha", type="password", key="rst_nova")
            conf_senha = st.text_input("Confirme", type="password", key="rst_conf")
            if st.button("Redefinir Senha", use_container_width=True):
                if not email_rst:
                    st.warning("Informe o e-mail.")
                elif nova_senha != conf_senha:
                    st.error("As senhas nao coincidem.")
                elif not nova_senha:
                    st.warning("Digite a nova senha.")
                else:
                    df_u = carregar('usuarios')
                    mask = df_u['Email'].str.lower() == email_rst.strip().lower()
                    if mask.any():
                        df_u.loc[mask, 'Senha'] = nova_senha
                        salvar(df_u, 'usuarios')
                        st.success("Senha redefinida! Faca login.")
                    else:
                        st.error("E-mail nao encontrado.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:2rem;'>"
        "2025 Omega Inc & Raphson Engenharia - Sistema Integrado de Gestao</p>",
        unsafe_allow_html=True
    )
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================
NIVEL = st.session_state['nivel']
NOME = st.session_state['nome_usuario']

with st.sidebar:
    try:
        st.image(Image.open("logo_final.png"), use_container_width=True)
    except:
        st.markdown(
            "<p style='color:#f1f5f9;font-weight:700;font-size:1rem;"
            "text-align:center;padding:8px 0;'>Omega & Raphson</p>",
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<span class='menu-label'>Navegacao</span>", unsafe_allow_html=True)

    opcoes = ["Dashboard", "Escala de Trabalho", "Manutencao", "Comercial"]
    if NIVEL in ['Admin', 'Editor']:
        opcoes += ["Financeiro", "Marketing", "Compras"]
    if NIVEL == 'Admin':
        opcoes += ["Cadastros e Config"]

    modulo = st.selectbox("", opcoes, label_visibility="collapsed")

    st.markdown("<br>" * 6, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "<div class='user-footer'>"
        "<div class='user-name'>👤 " + NOME + "</div>"
        "<div class='user-level'>🛡️ " + NIVEL + "</div>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Sair do Sistema", use_container_width=True):
        realizar_logout()


# ============================================================
# HELPER CABECALHO
# ============================================================
def page_header(icon, title, subtitle=""):
    sub_html = ""
    if subtitle:
        sub_html = "<p class='page-header-sub'>" + subtitle + "</p>"
    st.markdown(
        "<div class='page-header'>"
        "<span class='page-header-icon'>" + icon + "</span>"
        "<div>"
        "<p class='page-header-title'>" + title + "</p>"
        + sub_html +
        "</div>"
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# DASHBOARD
# ============================================================
if modulo == "Dashboard":
    page_header("📊", "Painel de Gestao Integrada", "Bem-vindo, " + NOME + "!")

    df_man = carregar('manutencao')
    df_com = carregar('comercial')
    df_esc = carregar('escala')
    df_sta = carregar('stands')
    df_usr = carregar('usuarios')

    stands_ativos = len(df_sta[df_sta['Status'] == 'Ativo']) if not df_sta.empty else 0
    man_pendentes = len(df_man[df_man['Status'] == 'Pendente']) if not df_man.empty else 0
    escalas_hoje = len(df_esc[df_esc['Data'] == str(date.today())]) if not df_esc.empty else 0
    usuarios_atv = len(df_usr[df_usr['Ativo'] == 'Sim']) if not df_usr.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stands Ativos", stands_ativos)
    c2.metric("Manutencoes Pendentes", man_pendentes)
    c3.metric("Escalas Hoje", escalas_hoje)
    c4.metric("Usuarios Ativos", usuarios_atv)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns(2)

    with ca:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### Ultimas Manutencoes")
        if not df_man.empty:
            st.dataframe(df_man[['ID', 'Data', 'Stand', 'Descricao', 'Status']].tail(5),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma manutencao registrada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### Ultimas Negociacoes")
        if not df_com.empty:
            st.dataframe(df_com[['ID', 'Data', 'Cliente', 'Stand', 'Etapa']].tail(5),
                         use_container_width=True, hide_index=True)
        else:
            st.info("Nenhuma negociacao registrada.")
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# ESCALA DE TRABALHO
# ============================================================
elif modulo == "Escala de Trabalho":
    hoje = datetime.now()
    page_header("📅", "Escala de Trabalho",
                calendar.month_name[hoje.month] + " / " + str(hoje.year))

    df_esc = carregar('escala')
    cal = calendar.monthcalendar(hoje.year, hoje.month)
    nomes = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sab", "Dom"]
    stands_list = get_stands()

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    cab = st.columns(7)
    for i, n in enumerate(nomes):
        cab[i].markdown(
            "<p style='text-align:center;font-weight:700;color:#1e3a8a;"
            "font-size:0.85rem;margin:0;'>" + n + "</p>",
            unsafe_allow_html=True
        )

    dia_sel = None
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                data_str = str(hoje.year) + "-" + str(hoje.month).zfill(2) + "-" + str(dia).zfill(2)
                tem_escala = (not df_esc.empty and (df_esc['Data'] == data_str).any())
                label = str(dia) + (" 📌" if tem_escala else "")
                if cols[i].button(label, key="cal_" + str(dia), use_container_width=True):
                    dia_sel = data_str

    st.markdown("</div>", unsafe_allow_html=True)

    if dia_sel:
        esc_dia = df_esc[df_esc['Data'] == dia_sel] if not df_esc.empty else pd.DataFrame()
        if not esc_dia.empty:
            st.success("Escala de " + dia_sel)
            st.dataframe(esc_dia[['Colaborador', 'Setor', 'Stand', 'Turno', 'Status']],
                         use_container_width=True, hide_index=True)
        else:
            st.info("Sem escala para " + dia_sel)

    if NIVEL in ['Admin', 'Editor']:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### Gerenciar Escala")
        colaboradores = get_usuarios_ativos()

        with st.form("form_escala"):
            c1, c2, c3 = st.columns(3)
            data_esc = c1.date_input("Data", value=date.today())
            colab = c2.selectbox("Colaborador", colaboradores)
            setor_esc = c3.selectbox("Setor", [
                "Manutencao", "Comercial", "Financeiro", "Marketing", "Compras", "Diretoria"
            ])
            c4, c5, c6 = st.columns(3)
            stand

