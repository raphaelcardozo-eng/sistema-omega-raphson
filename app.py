import streamlit as st
import pandas as pd
from PIL import Image
from datetime import datetime, date
import calendar
import os
import base64

# ============================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ============================================================
st.set_page_config(
    page_title="Gestão Integrada Omega & Raphson",
    layout="wide",
    page_icon="🏗️",
    initial_sidebar_state="expanded"
)

# ============================================================
# 2. CSS
# ============================================================
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
# 3. SESSION STATE
# ============================================================
defaults = {
    'autenticado':  False,
    'user_logado':  '',
    'nivel':        'Leitor',
    'nome_usuario': '',
    'man_form_key': 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# 4. BANCO DE DADOS
# ============================================================
ARQUIVOS = {
    'usuarios':   'db_usuarios.csv',
    'manutencao': 'db_manutencao.csv',
    'comercial':  'db_comercial.csv',
    'escala':     'db_escala.csv',
    'financeiro': 'db_financeiro.csv',
    'marketing':  'db_marketing.csv',
    'compras':    'db_compras.csv',
    'stands':     'db_stands.csv',
    'inventario': 'db_inventario.csv',
}
COLUNAS = {
    'usuarios':   ['ID', 'Nome', 'Email', 'Senha', 'Setor', 'Funcao', 'Nivel', 'Ativo'],
    'manutencao': ['ID', 'Data', 'Stand', 'Descricao', 'Responsavel', 'Urgencia',
                   'Status', 'Prazo', 'FotoAntes', 'FotoDepois', 'PedidoCompras', 'Obs'],
    'comercial':  ['ID', 'Data', 'Cliente', 'Contato', 'Stand', 'Produto', 'Etapa', 'Responsavel', 'Obs'],
    'escala':     ['ID', 'Data', 'DiaSemana', 'Colaborador', 'Setor', 'Stand', 'Turno', 'Status'],
    'financeiro': ['ID', 'Data', 'Tipo', 'Categoria', 'Descricao', 'Valor', 'Responsavel'],
    'marketing':  ['ID', 'Data', 'Campanha', 'Tipo', 'Responsavel', 'Stand', 'Status', 'Prazo'],
    'compras':    ['ID', 'Data', 'Item', 'Quantidade', 'Unidade', 'Solicitante',
                   'Setor', 'Urgencia', 'Status', 'OrigemChamadoID'],
    'stands':     ['ID', 'Nome', 'Endereco', 'Status', 'Responsavel'],
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
# 5. SEEDS
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
            [2, 'Stand Jazz',      'Endereco Jazz',      'Ativo', 'A definir'],
            [3, 'Stand Live',      'Endereco Live',      'Ativo', 'A definir'],
        ]
        salvar(pd.DataFrame(dados, columns=COLUNAS['stands']), 'stands')


garantir_admin()
garantir_stands()

# ============================================================
# 6. AUTENTICACAO
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
            'autenticado':  True,
            'user_logado':  row['Email'],
            'nome_usuario': row['Nome'],
            'nivel':        row['Nivel']
        })
        st.rerun()
    else:
        st.error("E-mail ou senha incorretos, ou usuario inativo.")


def realizar_logout():
    st.session_state.update(defaults)
    st.rerun()


# ============================================================
# 7. TELA DE LOGIN
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
                email_in = st.text_input(
                    "E-mail corporativo", placeholder="seu@email.com.br")
                senha_in = st.text_input(
                    "Senha", type="password", placeholder="senha")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ACESSAR O PAINEL", use_container_width=True):
                    if email_in and senha_in:
                        realizar_login(email_in, senha_in)
                    else:
                        st.warning("Preencha todos os campos.")

        with tab_reset:
            st.markdown("<br>", unsafe_allow_html=True)
            email_rst = st.text_input("E-mail cadastrado",  key="rst_email")
            nova_senha = st.text_input(
                "Nova senha",  type="password", key="rst_nova")
            conf_senha = st.text_input(
                "Confirme",    type="password", key="rst_conf")
            if st.button("Redefinir Senha", use_container_width=True):
                if not email_rst:
                    st.warning("Informe o e-mail.")
                elif nova_senha != conf_senha:
                    st.error("As senhas nao coincidem.")
                elif not nova_senha:
                    st.warning("Digite a nova senha.")
                else:
                    df_u = carregar('usuarios')
                    mask = df_u['Email'].str.lower(
                    ) == email_rst.strip().lower()
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
# 8. SIDEBAR
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
    st.markdown("<span class='menu-label'>Navegacao</span>",
                unsafe_allow_html=True)

    opcoes = [
        "Dashboard",
        "Escala de Trabalho",
        "Manutencao",
        "Comercial"
    ]
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
# 9. HELPER — CABECALHO DE PAGINA
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
# 10. DASHBOARD
# ============================================================
if modulo == "Dashboard":
    page_header("📊", "Painel de Gestao Integrada", "Bem-vindo, " + NOME + "!")

    df_man = carregar('manutencao')
    df_com = carregar('comercial')
    df_esc = carregar('escala')
    df_sta = carregar('stands')
    df_usr = carregar('usuarios')

    stands_ativos = len(
        df_sta[df_sta['Status'] == 'Ativo']) if not df_sta.empty else 0
    man_pendentes = len(
        df_man[df_man['Status'] == 'Pendente']) if not df_man.empty else 0
    escalas_hoje = len(df_esc[df_esc['Data'] == str(
        date.today())]) if not df_esc.empty else 0
    usuarios_atv = len(df_usr[df_usr['Ativo'] == 'Sim']
                       ) if not df_usr.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stands Ativos",         stands_ativos)
    c2.metric("Manutencoes Pendentes", man_pendentes)
    c3.metric("Escalas Hoje",          escalas_hoje)
    c4.metric("Usuarios Ativos",       usuarios_atv)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns(2)

    with ca:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### Ultimas Manutencoes")
        if not df_man.empty:
            st.dataframe(
                df_man[['ID', 'Data', 'Stand', 'Descricao', 'Status']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma manutencao registrada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### Ultimas Negociacoes")
        if not df_com.empty:
            st.dataframe(
                df_com[['ID', 'Data', 'Cliente', 'Stand', 'Etapa']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma negociacao registrada.")
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 11. ESCALA DE TRABALHO
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
                data_str = str(hoje.year) + "-" + \
                    str(hoje.month).zfill(2) + "-" + str(dia).zfill(2)
                tem_escala = (not df_esc.empty and (
                    df_esc['Data'] == data_str).any())
                label = str(dia) + (" 📌" if tem_escala else "")
                if cols[i].button(label, key="cal_" + str(dia), use_container_width=True):
                    dia_sel = data_str

    st.markdown("</div>", unsafe_allow_html=True)

    if dia_sel:
        esc_dia = df_esc[df_esc['Data'] ==
                         dia_sel] if not df_esc.empty else pd.DataFrame()
        if not esc_dia.empty:
            st.success("Escala de " + dia_sel)
            st.dataframe(
                esc_dia[['Colaborador', 'Setor', 'Stand', 'Turno', 'Status']],
                use_container_width=True, hide_index=True
            )
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
            stand_esc = c4.selectbox(
                "Stand / Local", stands_list + ["Escritorio Central"])
            turno = c5.selectbox(
                "Turno", ["Manha", "Tarde", "Integral", "Noite"])
            status_e = c6.selectbox(
                "Status", ["Confirmado", "Pendente", "Folga", "Ausencia"])

            if st.form_submit_button("Registrar Escala", use_container_width=True):
                dia_nome = nomes[data_esc.weekday()]
                nova = pd.DataFrame([[
                    proximo_id(df_esc), str(data_esc), dia_nome,
                    colab, setor_esc, stand_esc, turno, status_e
                ]], columns=COLUNAS['escala'])
                df_esc = pd.concat([df_esc, nova], ignore_index=True)
                salvar(df_esc, 'escala')
                st.success(colab + " escalado em " +
                           stand_esc + " em " + str(data_esc))
                st.rerun()

        if not df_esc.empty:
            with st.expander("Ver / Remover Escalas"):
                st.dataframe(df_esc, use_container_width=True, hide_index=True)
                id_del = st.number_input(
                    "ID para remover:", min_value=1, step=1, key="del_esc")
                if st.button("Remover", key="btn_del_esc"):
                    df_esc = df_esc[df_esc['ID'] != id_del]
                    salvar(df_esc, 'escala')
                    st.success("Removido!")
                    st.rerun()

# ============================================================
# 12. MANUTENCAO
# ============================================================
elif modulo == "Manutencao":
    page_header("🛠️", "Gestao de Manutencao",
                "Ordens de servico, acompanhamento tecnico e historico dos stands")

    df_man = carregar('manutencao')
    stands_list = get_stands()

    tab1, tab2, tab3 = st.tabs(
        ["Painel de OS", "Abrir Chamado", "Atualizar OS"])

    with tab1:
        if df_man.empty:
            st.info("Nenhuma ordem de servico registrada.")
        else:
            cf1, cf2, cf3 = st.columns(3)
            f_stand = cf1.multiselect(
                "Stand:", stands_list, default=stands_list)
            f_status = cf2.multiselect(
                "Status:",
                ["Pendente", "Em Andamento", "Aguardando Material",
                    "Concluido", "Cancelado"],
                default=["Pendente", "Em Andamento", "Aguardando Material"]
            )
            f_urg = cf3.multiselect(
                "Urgencia:", ["Alta", "Media", "Baixa"], default=["Alta", "Media", "Baixa"]
            )
            df_vis = df_man[
                df_man['Stand'].isin(f_stand) &
                df_man['Status'].isin(f_status) &
                df_man['Urgencia'].isin(f_urg)
            ]

            for _, row in df_vis.iterrows():
                urg_str = str(row.get('Urgencia', ''))
                if urg_str == "Alta":
                    urg_class = "os-card-alta"
                elif urg_str == "Media":
                    urg_class = "os-card-media"
                else:
                    urg_class = "os-card-baixa"

                status_str = str(row.get('Status', ''))
                badge_map = {
                    "Pendente":            "badge-pendente",
                    "Em Andamento":        "badge-andamento",
                    "Aguardando Material": "badge-material",
                    "Concluido":           "badge-concluido",
                    "Cancelado":           "badge-cancelado",
                }
                badge_cls = badge_map.get(status_str, "")

                prazo_val = str(row.get('Prazo', ''))
                prazo_txt = ""
                if prazo_val not in ['', 'nan']:
                    prazo_txt = " | Prazo: " + prazo_val

                pedido_val = str(row.get('PedidoCompras', ''))
                pedido_txt = ""
                if pedido_val not in ['', 'nan']:
                    pedido_txt = (
                        "<div style='margin-top:6px;font-size:0.8rem;color:#7c3aed;'>"
                        "Pedido Compras: " + pedido_val + "</div>"
                    )

                obs_val = str(row.get('Obs', ''))
                obs_txt = ""
                if obs_val not in ['', 'nan']:
                    obs_txt = (
                        "<div style='margin-top:4px;font-size:0.8rem;color:#64748b;'>"
                        "Obs: " + obs_val + "</div>"
                    )

                desc_str = str(row.get('Descricao', ''))[:180]
                id_str = str(int(row['ID']))

                st.markdown(
                    "<div class='os-card " + urg_class + "'>"
                    "<div style='display:flex;justify-content:space-between;"
                    "align-items:center;flex-wrap:wrap;gap:8px;'>"
                    "<div>"
                    "<span style='font-weight:800;font-size:1rem;color:#0f172a;'>OS #" + id_str + "</span>"
                    " <span class='status-badge " + badge_cls + "'>" + status_str + "</span>"
                    " <span style='font-size:0.8rem;color:#64748b;'>Urgencia: " + urg_str + "</span>"
                    "</div>"
                    "<span style='font-size:0.8rem;color:#94a3b8;'>"
                    "Data: " + str(row.get('Data', '')) + prazo_txt + "</span>"
                    "</div>"
                    "<div style='margin-top:8px;font-size:0.85rem;color:#334155;'>"
                    "Stand: <b>" + str(row.get('Stand', '')) + "</b>"
                    " | Responsavel: " + str(row.get('Responsavel', '')) +
                    "</div>"
                    "<div style='margin-top:6px;font-size:0.88rem;color:#475569;'>"
                    + desc_str +
                    "</div>"
                    + pedido_txt + obs_txt +
                    "</div>",
                    unsafe_allow_html=True
                )

                foto_antes = decode_img(str(row.get('FotoAntes', '')))
                foto_depois = decode_img(str(row.get('FotoDepois', '')))
                if foto_antes or foto_depois:
                    col_f1, col_f2 = st.columns(2)
                    if foto_antes:
                        with col_f1:
                            st.markdown(
                                "<p class='foto-label'>Foto Antes</p>", unsafe_allow_html=True)
                            st.image(foto_antes, use_container_width=True)
                    if foto_depois:
                        with col_f2:
                            st.markdown(
                                "<p class='foto-label'>Foto Depois</p>", unsafe_allow_html=True)
                            st.image(foto_depois, use_container_width=True)

    with tab2:
        if NIVEL in ['Admin', 'Editor']:
            colaboradores = get_usuarios_ativos()
            form_key = "form_man_" + str(st.session_state['man_form_key'])

            with st.form(form_key, clear_on_submit=True):
                st.markdown("#### Dados da Ocorrencia")
                c1, c2, c3 = st.columns(3)
                stand_m = c1.selectbox("Stand:", stands_list)
                resp_m = c2.selectbox("Responsavel:", colaboradores)
                urg_m = c3.select_slider(
                    "Urgencia:", ["Baixa", "Media", "Alta"])
                desc_m = st.text_area("Descricao detalhada do problema:", height=120,
                                      placeholder="Descreva o problema...")
                st.markdown("#### Foto do Problema (Antes)")
                foto_antes_up = st.file_uploader(
                    "Anexar foto",
                    type=["jpg", "jpeg", "png", "webp"],
                    key="foto_antes_" + str(st.session_state['man_form_key'])
                )
                if st.form_submit_button("Abrir Ordem de Servico", use_container_width=True):
                    if desc_m.strip():
                        df_man = carregar('manutencao')
                        nova = pd.DataFrame([[
                            proximo_id(df_man),
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            stand_m, desc_m, resp_m, urg_m,
                            "Pendente", "", encode_img(
                                foto_antes_up), "", "", ""
                        ]], columns=COLUNAS['manutencao'])
                        df_man = pd.concat([df_man, nova], ignore_index=True)
                        salvar(df_man, 'manutencao')
                        st.session_state['man_form_key'] += 1
                        st.success(
                            "OS aberta! Formulario limpo para novo chamado.")
                        st.rerun()
                    else:
                        st.warning(
                            "Descreva o problema antes de abrir o chamado.")
        else:
            st.warning("Apenas Editores e Admins podem abrir chamados.")

    with tab3:
        if NIVEL in ['Admin', 'Editor']:
            df_man = carregar('manutencao')
            if df_man.empty:
                st.info("Nenhuma OS registrada.")
            else:
                ids_abertos = df_man[
                    ~df_man['Status'].isin(['Concluido', 'Cancelado'])
                ]['ID'].tolist()

                if not ids_abertos:
                    st.success("Todas as OS estao concluidas ou canceladas!")
                else:
                    def fmt_os(x):
                        row_sel = df_man[df_man['ID'] == x]
                        if row_sel.empty:
                            return str(x)
                        stand_v = str(row_sel['Stand'].values[0])
                        desc_v = str(row_sel['Descricao'].values[0])[:50]
                        return "OS #" + str(x) + " - " + stand_v + " | " + desc_v + "..."

                    id_sel = st.selectbox(
                        "Selecione a OS:", ids_abertos, format_func=fmt_os)
                    os_row = df_man[df_man['ID'] == id_sel].iloc[0]

                    st.markdown(
                        "<div class='custom-card'>"
                        "<b>OS #" + str(int(os_row['ID'])) + "</b> | "
                        "Stand: " + str(os_row.get('Stand', '')) + " | "
                        "Responsavel: " +
                        str(os_row.get('Responsavel', '')) + " | "
                        "Urgencia: " + str(os_row.get('Urgencia', '')) + " | "
                        "Abertura: " + str(os_row.get('Data', '')) +
                        "<br><br>"
                        "<span style='color:#475569;'>" +
                        str(os_row.get('Descricao', '')) + "</span>"
                        "</div>",
                        unsafe_allow_html=True
                    )

                    with st.form("form_upd_os"):
                        status_opcoes = [
                            "Pendente", "Em Andamento",
                            "Aguardando Material", "Concluido", "Cancelado"
                        ]
                        status_atual = str(os_row.get('Status', 'Pendente'))
                        idx_status = status_opcoes.index(
                            status_atual) if status_atual in status_opcoes else 0

                        c1, c2 = st.columns(2)
                        novo_status = c1.selectbox(
                            "Novo Status:", status_opcoes, index=idx_status)
                        prazo_os = c2.date_input(
                            "Prazo de Conclusao:", value=date.today())

                        obs_os = st.text_area(
                            "Observacoes / Atualizacao:",
                            placeholder="Descreva o que foi feito ou o motivo...",
                            height=100
                        )

                        st.markdown("---")
                        st.markdown("#### Solicitar Material ao Compras")
                        col_m1, col_m2, col_m3 = st.columns(3)
                        solicitar_mat = col_m1.checkbox(
                            "Enviar pedido de material")
                        material_desc = col_m2.text_input(
                            "Material necessario:")
                        material_qtd = col_m3.number_input(
                            "Quantidade:", min_value=1, step=1)

                        st.markdown("---")
                        st.markdown("#### Registrar Fotos")
                        col_f1, col_f2 = st.columns(2)
                        foto_antes_upd = col_f1.file_uploader(
                            "Foto Antes (atualizar)",
                            type=["jpg", "jpeg", "png", "webp"],
                            key="upd_antes"
                        )
                        foto_depois_upd = col_f2.file_uploader(
                            "Foto Depois",
                            type=["jpg", "jpeg", "png", "webp"],
                            key="upd_depois"
                        )

                        if st.form_submit_button("Salvar Atualizacao", use_container_width=True):
                            df_man = carregar('manutencao')
                            idx = df_man[df_man['ID'] == id_sel].index[0]
                            df_man.at[idx, 'Status'] = novo_status
                            df_man.at[idx, 'Prazo'] = str(prazo_os)
                            df_man.at[idx, 'Obs'] = obs_os

                            if foto_antes_upd:
                                df_man.at[idx, 'FotoAntes'] = encode_img(
                                    foto_antes_upd)
                            if foto_depois_upd:
                                df_man.at[idx, 'FotoDepois'] = encode_img(
                                    foto_depois_upd)

                            pedido_ref = ''
                            if solicitar_mat and material_desc.strip():
                                df_cmp = carregar('compras')
                                novo_id_cmp = proximo_id(df_cmp)
                                pedido_ref = "#" + \
                                    str(novo_id_cmp) + " - " + material_desc
                                nova_cmp = pd.DataFrame([[
                                    novo_id_cmp,
                                    datetime.now().strftime("%d/%m/%Y"),
                                    material_desc, material_qtd, "Un",
                                    str(os_row.get('Responsavel', '')),
                                    "Manutencao",
                                    str(os_row.get('Urgencia', 'Media')),
                                    "Pendente",
                                    "OS #" + str(id_sel)
                                ]], columns=COLUNAS['compras'])
                                df_cmp = pd.concat(
                                    [df_cmp, nova_cmp], ignore_index=True)
                                salvar(df_cmp, 'compras')
                                df_man.at[idx, 'PedidoCompras'] = pedido_ref

                            salvar(df_man, 'manutencao')
                            msg = "OS #" + \
                                str(id_sel) + " atualizada para '" + \
                                novo_status + "'!"
                            if pedido_ref:
                                msg += " Pedido " + pedido_ref + " enviado ao Compras."
                            st.success(msg)
                            st.rerun()
        else:
            st.warning("Apenas Editores e Admins podem atualizar OS.")

# ============================================================
# 13. COMERCIAL
# ============================================================
elif modulo == "Comercial":
    page_header("🤝", "Gestao Comercial",
                "Leads, negociacoes e pipeline de vendas")

    df_com = carregar('comercial')
    stands_list = get_stands()
    tab1, tab2 = st.tabs(["Pipeline", "Novo Lead"])

    with tab1:
        if df_com.empty:
            st.info("Nenhuma negociacao registrada.")
        else:
            f_etapa = st.multiselect(
                "Etapa:",
                ["Prospeccao", "Proposta", "Negociacao", "Fechado", "Perdido"],
                default=["Prospeccao", "Proposta", "Negociacao"]
            )
            df_vis = df_com[df_com['Etapa'].isin(
                f_etapa)] if f_etapa else df_com
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

            if NIVEL in ['Admin', 'Editor'] and not df_com.empty:
                st.markdown("---")
                cx1, cx2 = st.columns(2)
                id_c = cx1.selectbox("ID:", df_com['ID'].tolist())
                et_n = cx2.selectbox(
                    "Etapa:", ["Prospeccao", "Proposta",
                               "Negociacao", "Fechado", "Perdido"],
                    key="etapa_upd"
                )
                if st.button("Atualizar Etapa"):
                    df_com.loc[df_com['ID'] == id_c, 'Etapa'] = et_n
                    salvar(df_com, 'comercial')
                    st.success("Atualizado!")
                    st.rerun()

    with tab2:
        if NIVEL in ['Admin', 'Editor']:
            colaboradores = get_usuarios_ativos()
            with st.form("form_com", clear_on_submit=True):
                c1, c2 = st.columns(2)
                cliente = c1.text_input("Cliente / Empresa")
                contato = c2.text_input("WhatsApp / E-mail")
                c3, c4, c5 = st.columns(3)
                stand_c = c3.selectbox("Stand:", stands_list)
                produto = c4.text_input("Produto / Servico")
                etapa_c = c5.selectbox(
                    "Etapa:", ["Prospeccao", "Proposta",
                               "Negociacao", "Fechado", "Perdido"]
                )
                resp_c = st.selectbox("Responsavel:", colaboradores)
                obs_c = st.text_area("Observacoes:")
                if st.form_submit_button("Registrar", use_container_width=True):
                    if cliente.strip():
                        nova = pd.DataFrame([[
                            proximo_id(df_com),
                            datetime.now().strftime("%d/%m/%Y"),
                            cliente, contato, stand_c, produto, etapa_c, resp_c, obs_c
                        ]], columns=COLUNAS['comercial'])
                        df_com = pd.concat([df_com, nova], ignore_index=True)
                        salvar(df_com, 'comercial')
                        st.success("Lead '" + cliente + "' registrado!")
                        st.rerun()
                    else:
                        st.warning("Informe o nome do cliente.")
        else:
            st.warning("Apenas Editores e Admins podem registrar.")

# ============================================================
# 14. FINANCEIRO
# ============================================================
elif modulo == "Financeiro":
    page_header("💰", "Controle Financeiro",
                "Lancamentos, entradas, saidas e saldo")

    df_fin = carregar('financeiro')
    tab1, tab2 = st.tabs(["Resumo", "Novo Lancamento"])

    with tab1:
        if df_fin.empty:
            st.info("Nenhum lancamento registrado.")
        else:
            total_e = df_fin[df_fin['Tipo'] ==
                             'Entrada']['Valor'].astype(float).sum()
            total_s = df_fin[df_fin['Tipo'] ==
                             'Saida']['Valor'].astype(float).sum()
            saldo = total_e - total_s
            c1, c2, c3 = st.columns(3)
            c1.metric("Entradas", "R$ " + "{:,.2f}".format(total_e))
            c2.metric("Saidas",   "R$ " + "{:,.2f}".format(total_s))
            c3.metric("Saldo",    "R$ " + "{:,.2f}".format(saldo))
            st.dataframe(df_fin, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("form_fin", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            tipo_f = c1.selectbox("Tipo:", ["Entrada", "Saida"])
            cat_f = c2.selectbox("Categoria:", [
                "Fornecedor", "Salario", "Material", "Receita", "Imposto", "Outros"
            ])
            val_f = c3.number_input(
                "Valor (R$):", min_value=0.0, step=0.01, format="%.2f")
            desc_f = st.text_input("Descricao")
            resp_f = st.text_input("Responsavel")
            if st.form_submit_button("Registrar Lancamento", use_container_width=True):
                nova = pd.DataFrame([[
                    proximo_id(df_fin),
                    datetime.now().strftime("%d/%m/%Y"),
                    tipo_f, cat_f, desc_f, val_f, resp_f
                ]], columns=COLUNAS['financeiro'])
                df_fin = pd.concat([df_fin, nova], ignore_index=True)
                salvar(df_fin, 'financeiro')
                st.success("Lancamento registrado!")
                st.rerun()

# ============================================================
# 15. MARKETING
# ============================================================
elif modulo == "Marketing":
    page_header("📣", "Gestao de Marketing",
                "Campanhas, acoes e materiais de comunicacao")

    df_mkt = carregar('marketing')
    stands_list = get_stands()
    tab1, tab2 = st.tabs(["Campanhas", "Nova Acao"])

    with tab1:
        if df_mkt.empty:
            st.info("Nenhuma campanha registrada.")
        else:
            st.dataframe(df_mkt, use_container_width=True, hide_index=True)

    with tab2:
        colaboradores = get_usuarios_ativos()
        with st.form("form_mkt", clear_on_submit=True):
            c1, c2 = st.columns(2)
            camp = c1.text_input("Campanha / Acao")
            tipo_m = c2.selectbox("Tipo:", [
                "Banner", "Post Redes Sociais", "E-mail Marketing", "Evento", "Outro"
            ])
            c3, c4, c5 = st.columns(3)
            resp_m = c3.selectbox("Responsavel:", colaboradores)
            stand_m = c4.selectbox(
                "Stand:", stands_list + ["Todos", "Digital"])
            prazo_m = c5.date_input("Prazo:")
            if st.form_submit_button("Registrar Campanha", use_container_width=True):
                if camp.strip():
                    nova = pd.DataFrame([[
                        proximo_id(df_mkt),
                        datetime.now().strftime("%d/%m/%Y"),
                        camp, tipo_m, resp_m, stand_m, "Em Andamento", str(
                            prazo_m)
                    ]], columns=COLUNAS['marketing'])
                    df_mkt = pd.concat([df_mkt, nova], ignore_index=True)
                    salvar(df_mkt, 'marketing')
                    st.success("Campanha registrada!")
                    st.rerun()
                else:
                    st.warning("Informe o nome da campanha.")

# ============================================================
# 16. COMPRAS
# ============================================================
elif modulo == "Compras":
    page_header("🛒", "Gestao de Compras",
                "Pedidos, cotacoes e controle de materiais")

    df_cmp = carregar('compras')
    tab1, tab2 = st.tabs(["Pedidos", "Novo Pedido"])

    with tab1:
        if df_cmp.empty:
            st.info("Nenhum pedido registrado.")
        else:
            f_st = st.multiselect(
                "Status:",
                ["Pendente", "Em Cotacao", "Aprovado", "Entregue", "Cancelado"],
                default=["Pendente", "Em Cotacao"]
            )
            df_vis = df_cmp[df_cmp['Status'].isin(f_st)] if f_st else df_cmp
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

            if NIVEL in ['Admin', 'Editor']:
                c1, c2 = st.columns(2)
                id_cp = c1.selectbox("ID:", df_cmp['ID'].tolist())
                st_cp = c2.selectbox("Novo Status:", [
                    "Pendente", "Em Cotacao", "Aprovado", "Entregue", "Cancelado"
                ])
                if st.button("Atualizar"):
                    df_cmp.loc[df_cmp['ID'] == id_cp, 'Status'] = st_cp
                    salvar(df_cmp, 'compras')
                    st.success("Atualizado!")
                    st.rerun()

    with tab2:
        with st.form("form_cmp", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            item_c = c1.text_input("Item / Material")
            qtd_c = c2.number_input("Quantidade:", min_value=1, step=1)
            unid_c = c3.selectbox(
                "Unidade:", ["Un", "Kg", "Lt", "M", "M2", "Caixa", "Pacote"])
            c4, c5, c6 = st.columns(3)
            solic_c = c4.text_input("Solicitante")
            setor_c = c5.selectbox("Setor:", [
                "Manutencao", "Obra", "Escritorio", "Marketing", "Comercial"
            ])
            urg_c = c6.select_slider("Urgencia:", ["Baixa", "Media", "Alta"])
            if st.form_submit_button("Enviar Pedido", use_container_width=True):
                if item_c.strip() and solic_c.strip():
                    nova = pd.DataFrame([[
                        proximo_id(df_cmp),
                        datetime.now().strftime("%d/%m/%Y"),
                        item_c, qtd_c, unid_c, solic_c, setor_c, urg_c, "Pendente", ""
                    ]], columns=COLUNAS['compras'])
                    df_cmp = pd.concat([df_cmp, nova], ignore_index=True)
                    salvar(df_cmp, 'compras')
                    st.success("Pedido enviado!")
                    st.rerun()
                else:
                    st.warning("Informe item e solicitante.")

# ============================================================
# 17. CADASTROS E CONFIGURACOES
# ============================================================
elif modulo == "Cadastros e Config":
    page_header("⚙️", "Cadastros e Configuracoes",
                "Usuarios, stands e inventario")

    tab_usr, tab_std, tab_inv = st.tabs(["Usuarios", "Stands", "Inventario"])

    # ── USUARIOS ──────────────────────────────────────────
    with tab_usr:
        df_usr = carregar('usuarios')
        st.markdown("#### Usuarios Cadastrados")

        cols_show = ['ID', 'Nome', 'Email',
                     'Setor', 'Funcao', 'Nivel', 'Ativo']
        cols_exist = [c for c in cols_show if c in df_usr.columns]
        st.dataframe(df_usr[cols_exist],
                     use_container_width=True, hide_index=True)

        s1, s2, s3 = st.tabs(["Novo Usuario", "Alterar Senha", "Desativar"])

        with s1:
            with st.form("form_new_usr", clear_on_submit=True):
                c1, c2 = st.columns(2)
                nome_u = c1.text_input("Nome Completo")
                email_u = c2.text_input("E-mail Corporativo")
                c3, c4, c5 = st.columns(3)
                senha_u = c3.text_input("Senha Inicial", type="password")
                setor_u = c4.selectbox("Setor:", [
                    "Diretoria", "Engenharia", "Manutencao",
                    "Comercial", "Financeiro", "Marketing", "Compras"
                ])
                nivel_u = c5.select_slider(
                    "Nivel de Acesso:", ["Leitor", "Editor", "Admin"])
                funcao_u = st.text_input("Funcao / Cargo")
                if st.form_submit_button("Cadastrar Usuario", use_container_width=True):
                    if nome_u and email_u and senha_u and funcao_u:
                        df2 = carregar('usuarios')
                        if (df2['Email'].str.lower() == email_u.strip().lower()).any():
                            st.error("E-mail ja cadastrado.")
                        else:
                            nova = pd.DataFrame([[
                                proximo_id(df2), nome_u, email_u.strip(),
                                senha_u, setor_u, funcao_u, nivel_u, "Sim"
                            ]], columns=COLUNAS['usuarios'])
                            df2 = pd.concat([df2, nova], ignore_index=True)
                            salvar(df2, 'usuarios')
                            st.success("Usuario '" + nome_u + "' cadastrado!")
                            st.rerun()
                    else:
                        st.warning("Preencha todos os campos obrigatorios.")

        with s2:
            with st.form("form_senha", clear_on_submit=True):
                email_a = st.text_input("E-mail do usuario")
                nova_s = st.text_input("Nova senha",  type="password")
                conf_s = st.text_input("Confirme",    type="password")
                if st.form_submit_button("Alterar Senha", use_container_width=True):
                    if not nova_s:
                        st.warning("Digite a nova senha.")
                    elif nova_s != conf_s:
                        st.error("As senhas nao coincidem.")
                    else:
                        df2 = carregar('usuarios')
                        mask = df2['Email'].str.lower(
                        ) == email_a.strip().lower()
                        if mask.any():
                            df2.loc[mask, 'Senha'] = nova_s
                            salvar(df2, 'usuarios')
                            st.success("Senha alterada com sucesso!")
                        else:
                            st.error("Usuario nao encontrado.")

                        with s3:
            st.markdown("#### Desativar Usuario")
            with st.form("form_del_usr", clear_on_submit=True):
                st.warning("Esta acao revoga o acesso do usuario ao sistema.")
                email_d = st.text_input("E-mail do usuario a desativar")
                conf_d = st.checkbox(
                    "Confirmo que desejo desativar este usuario.")
                if st.form_submit_button("Desativar Usuario", use_container_width=True):
                    if not conf_d:
                        st.warning("Marque a caixa de confirmacao.")
                    elif not email_d:
                        st.warning("Informe o e-mail.")
                    else:
                        df2 = carregar('usuarios')
                        mask = df2['Email'].str.lower(
                        ) == email_d.strip().lower()
                        if mask.any():
                            df2.loc[mask, 'Ativo'] = 'Nao'
                            salvar(df2, 'usuarios')
                            st.success("Usuario desativado com sucesso.")
                            st.rerun()
                        else:
                            st.error("Usuario nao encontrado.")
    with tab_std:
        df_std = carregar('stands')
        st.markdown("#### Stands Cadastrados")
        st.dataframe(df_std, use_container_width=True, hide_index=True)

        sa, sb = st.tabs(["Novo Stand", "Editar Status"])

        with sa:
            with st.form("form_std", clear_on_submit=True):
                c1, c2 = st.columns(2)
                nome_s = c1.text_input("Nome do Stand")
                end_s = c2.text_input("Endereco / Localizacao")
                resp_s = st.text_input("Responsavel pelo Stand")
                if st.form_submit_button("Cadastrar Stand", use_container_width=True):
                    if nome_s.strip():
                        df_std2 = carregar('stands')
                        nova = pd.DataFrame([[
                            proximo_id(df_std2),
                            nome_s.strip(), end_s, "Ativo", resp_s
                        ]], columns=COLUNAS['stands'])
                        df_std2 = pd.concat([df_std2, nova], ignore_index=True)
                        salvar(df_std2, 'stands')
                        st.success("Stand " + nome_s + " cadastrado!")
                        st.rerun()
                    else:
                        st.warning("Informe o nome do stand.")

        with sb:
            df_std2 = carregar('stands')
            if not df_std2.empty:
                c1, c2 = st.columns(2)

                def fmt_stand(x):
                    r = df_std2[df_std2['ID'] == x]
                    if r.empty:
                        return str(x)
                    return str(x) + " - " + str(r['Nome'].values[0])
                id_s = c1.selectbox(
                    "Stand:", df_std2['ID'].tolist(), format_func=fmt_stand)
                nst_s = c2.selectbox(
                    "Novo Status:", ["Ativo", "Inativo", "Em Manutencao"])
                if st.button("Atualizar Status do Stand"):
                    df_std2.loc[df_std2['ID'] == id_s, 'Status'] = nst_s
                    salvar(df_std2, 'stands')
                    st.success("Stand atualizado!")
                    st.rerun()
            else:
                st.info("Nenhum stand cadastrado.")

    with tab_inv:
        df_inv = carregar('inventario')
        stands_list = get_stands()

        st.markdown("#### Inventario de Materiais e Equipamentos")
        if not df_inv.empty:
            st.dataframe(df_inv, use_container_width=True, hide_index=True)
        else:
            st.info("Inventario vazio.")

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_inv", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            item_i = c1.text_input("Item / Equipamento")
            cat_i = c2.selectbox("Categoria:", [
                "Ferramenta", "Equipamento", "Material", "EPI", "Mobiliario", "Outro"
            ])
            qtd_i = c3.number_input("Quantidade:", min_value=0, step=1)

            c4, c5, c6 = st.columns(3)
            unid_i = c4.selectbox("Unidade:", [
                "Un", "Kg", "Lt", "M", "Par", "Conjunto", "Caixa"
            ])
            stand_i = c5.selectbox("Stand / Local:", [
                "Almoxarifado", "Escritorio"
            ] + stands_list)
            stat_i = c6.selectbox("Estado:", [
                "Disponivel", "Em Uso", "Em Manutencao", "Descartado"
            ])

            prop_i = st.selectbox("Propriedade:", [
                "Raphson",
                "Omega",
                "Raphson x Omega",
                "Raphson x Omega x 4V"
            ])

            if st.form_submit_button("Registrar Item", use_container_width=True):
                if item_i.strip():
                    df_inv2 = carregar('inventario')
                    nova = pd.DataFrame([[
                        proximo_id(df_inv2),
                        item_i.strip(), cat_i, qtd_i,
                        unid_i, stand_i, stat_i, prop_i
                    ]], columns=COLUNAS['inventario'])
                    df_inv2 = pd.concat([df_inv2, nova], ignore_index=True)
                    salvar(df_inv2, 'inventario')
                    st.success(item_i + " registrado no inventario!")
                    st.rerun()
                else:
                    st.warning("Informe o nome do item.")
