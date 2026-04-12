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
# 2. CSS — DESIGN PREMIUM E RESPONSIVO
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
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; margin: 0.75rem 0; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
.menu-label {
    color: #64748b !important;
    font-size: 0.65rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    padding: 0.5rem 0 0.25rem 0;
    display: block;
}
.user-footer {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 12px 14px;
    margin-top: 8px;
}
.user-name { color: #f1f5f9 !important; font-weight: 600; font-size: 0.88rem; }
.user-level { color: #64748b !important; font-size: 0.75rem; }

h1 { color: #0f172a !important; font-weight: 800 !important; font-size: 1.85rem !important; letter-spacing: -0.02em; margin-bottom: 0.15rem !important; }
h2 { color: #1e293b !important; font-weight: 700 !important; font-size: 1.3rem !important; }
h3 { color: #334155 !important; font-weight: 600 !important; font-size: 1.05rem !important; }

.page-header {
    background: linear-gradient(135deg, #1e3a8a 0%, #1d4ed8 50%, #2563eb 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(30,58,138,0.25);
}
.page-header-icon { font-size: 2.2rem; line-height: 1; }
.page-header-title { color: #ffffff !important; font-size: 1.6rem !important; font-weight: 800 !important; margin: 0 !important; letter-spacing: -0.02em; }
.page-header-sub { color: rgba(255,255,255,0.72) !important; font-size: 0.88rem; margin-top: 2px; }

[data-testid="stMetric"] {
    background: #ffffff !important;
    border-radius: 14px !important;
    padding: 1.25rem 1.5rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
    border: 1px solid #e2e8f0 !important;
    border-top: 4px solid #3b82f6 !important;
    transition: transform 0.2s, box-shadow 0.2s;
}
[data-testid="stMetric"]:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(59,130,246,0.15) !important; }
[data-testid="stMetricLabel"] { font-size: 0.78rem !important; font-weight: 600 !important; color: #64748b !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { font-size: 2rem !important; font-weight: 800 !important; color: #0f172a !important; }

[data-testid="stForm"] {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.75rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] input {
    border-radius: 10px !important;
    border: 1.5px solid #e2e8f0 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.12) !important;
}
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s !important;
    border: none !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(37,99,235,0.35) !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border-bottom: none !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 9px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: #64748b !important;
    padding: 0.45rem 1.1rem !important;
    border: none !important;
    background: transparent !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #ffffff !important;
    color: #1d4ed8 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
[data-testid="stAlert"] { border-radius: 12px !important; border: none !important; font-weight: 500; }
[data-testid="stExpander"] { background: #f8fafc; border-radius: 12px; border: 1px solid #e2e8f0 !important; }

hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.25rem 0; }

.custom-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.os-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #3b82f6;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.os-card-alta  { border-left-color: #ef4444 !important; }
.os-card-media { border-left-color: #f59e0b !important; }
.os-card-baixa { border-left-color: #22c55e !important; }

.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}
.badge-pendente  { background: #fef3c7; color: #92400e; }
.badge-andamento { background: #dbeafe; color: #1e40af; }
.badge-material  { background: #ede9fe; color: #5b21b6; }
.badge-concluido { background: #dcfce7; color: #166534; }
.badge-cancelado { background: #fee2e2; color: #991b1b; }

.login-title { text-align: center; color: #0f172a !important; font-size: 1.5rem !important; font-weight: 800 !important; }
.login-sub { text-align: center; color: #64748b; font-size: 0.9rem; margin-bottom: 1.5rem; }
.foto-label { font-size: 0.78rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.25rem; }

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
# 4. BANCO DE DADOS LOCAL (CSV)
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
    'usuarios':   ['ID','Nome','Email','Senha','Setor','Funcao','Nivel','Ativo'],
    'manutencao': ['ID','Data','Stand','Descricao','Responsavel','Urgencia',
                   'Status','Prazo','FotoAntes','FotoDepois','PedidoCompras','Obs'],
    'comercial':  ['ID','Data','Cliente','Contato','Stand','Produto','Etapa','Responsavel','Obs'],
    'escala':     ['ID','Data','DiaSemana','Colaborador','Setor','Stand','Turno','Status'],
    'financeiro': ['ID','Data','Tipo','Categoria','Descricao','Valor','Responsavel'],
    'marketing':  ['ID','Data','Campanha','Tipo','Responsavel','Stand','Status','Prazo'],
    'compras':    ['ID','Data','Item','Quantidade','Unidade','Solicitante','Setor',
                   'Urgencia','Status','OrigemChamadoID'],
    'stands':     ['ID','Nome','Endereco','Status','Responsavel'],
    'inventario': ['ID','Item','Categoria','Quantidade','Unidade','Stand',
                   'Estado','Propriedade'],
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
            1, 'Raphael Cardozo',
            'raphaelcardozo@raphsonengenharia.com.br',
            '1234', 'Diretoria', 'Diretor', 'Admin', 'Sim'
        ]], columns=COLUNAS['usuarios'])
        df = pd.concat([df, novo], ignore_index=True)
        salvar(df, 'usuarios')

def garantir_stands():
    df = carregar('stands')
    if df.empty:
        dados = [
            [1, 'Stand Principal', 'Endereço Principal', 'Ativo', 'Raphael Cardozo'],
            [2, 'Stand Jazz',      'Endereço Jazz',      'Ativo', 'A definir'],
            [3, 'Stand Live',      'Endereço Live',      'Ativo', 'A definir'],
        ]
        salvar(pd.DataFrame(dados, columns=COLUNAS['stands']), 'stands')

garantir_admin()
garantir_stands()

# ============================================================
# 6. AUTENTICAÇÃO
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
        st.error("⚠️ E-mail ou senha incorretos, ou usuário inativo.")

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
                "<h2 style='text-align:center;color:#1e3a8a;'>"
                "🏗️ Omega Inc & Raphson Engenharia</h2>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    cl2, cc2, cr2 = st.columns([1, 1.3, 1])
    with cc2:
        st.markdown("""
            <div style='background:#fff;border-radius:20px;padding:2.5rem 2rem;
                        box-shadow:0 20px 60px rgba(0,0,0,0.10);border:1px solid #e2e8f0;'>
        """, unsafe_allow_html=True)

        st.markdown(
            "<p class='login-title'>Gestão Integrada</p>"
            "<p class='login-sub'>Omega Inc & Raphson Engenharia<br>"
            "Identifique-se para acessar o painel.</p>",
            unsafe_allow_html=True
        )

        tab_login, tab_reset = st.tabs(["🔐  Entrar", "🔑  Esqueci a Senha"])

        with tab_login:
            with st.form("form_login", clear_on_submit=False):
                email_in = st.text_input("📧  E-mail corporativo", placeholder="seu@email.com.br")
                senha_in = st.text_input("🔒  Senha", type="password", placeholder="••••••••")
                st.markdown("<br>", unsafe_allow_html=True)
                if st.form_submit_button("ACESSAR O PAINEL →", use_container_width=True):
                    if email_in and senha_in:
                        realizar_login(email_in, senha_in)
                    else:
                        st.warning("Preencha todos os campos.")

        with tab_reset:
            st.markdown("<br>", unsafe_allow_html=True)
            email_rst  = st.text_input("E-mail cadastrado",  key="rst_email")
            nova_senha = st.text_input("Nova senha",          type="password", key="rst_nova")
            conf_senha = st.text_input("Confirme a senha",    type="password", key="rst_conf")
            if st.button("Redefinir Senha", use_container_width=True):
                if not email_rst:
                    st.warning("Informe o e-mail.")
                elif nova_senha != conf_senha:
                    st.error("As senhas não coincidem.")
                elif not nova_senha:
                    st.warning("Digite a nova senha.")
                else:
                    df_u = carregar('usuarios')
                    mask = df_u['Email'].str.lower() == email_rst.strip().lower()
                    if mask.any():
                        df_u.loc[mask, 'Senha'] = nova_senha
                        salvar(df_u, 'usuarios')
                        st.success("✅ Senha redefinida! Faça login.")
                    else:
                        st.error("E-mail não encontrado.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<p style='text-align:center;color:#94a3b8;font-size:0.78rem;margin-top:2rem;'>"
        "© 2025 Omega Inc & Raphson Engenharia · Sistema Integrado de Gestão</p>",
        unsafe_allow_html=True
    )
    st.stop()

# ============================================================
# 8. SIDEBAR
# ============================================================
NIVEL = st.session_state['nivel']
NOME  = st.session_state['nome_usuario']

with st.sidebar:
    try:
        st.image(Image.open("logo_final.png"), use_container_width=True)
    except:
        st.markdown(
            "<p style='color:#f1f5f9;font-weight:700;font-size:1rem;"
            "text-align:center;padding:8px 0;'>🏗️ Omega & Raphson</p>",
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<span class='menu-label'>Navegação</span>", unsafe_allow_html=True)

    opcoes = ["🏠  Dashboard", "📅  Escala de Trabalho",
              "🛠️  Manutenção", "🤝  Comercial"]
    if NIVEL in ['Admin', 'Editor']:
        opcoes += ["💰  Financeiro", "📣  Marketing", "🛒  Compras"]
    if NIVEL == 'Admin':
        opcoes += ["⚙️  Cadastros & Config"]

    modulo = st.selectbox("", opcoes, label_visibility="collapsed")

    st.markdown("<br>" * 6, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='user-footer'>
            <div class='user-name'>👤 {NOME}</div>
            <div class='user-level'>🛡️ {NIVEL}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪  Sair do Sistema", use_container_width=True):
        realizar_logout()

# ============================================================
# 9. HELPER — CABEÇALHO DE PÁGINA
# ============================================================
def page_header(icon, title, subtitle=""):
    st.markdown(f"""
        <div class='page-header'>
            <span class='page-header-icon'>{icon}</span>
            <div>
                <p class='page-header-title'>{title}</p>
                {f"<p class='page-header-sub'>{subtitle}</p>" if subtitle else ""}
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================
# 10. DASHBOARD
# ============================================================
if modulo == "🏠  Dashboard":
    page_header("📊", "Painel de Gestão Integrada",
                f"Bem-vindo, {NOME}! Aqui está a visão geral da operação.")

    df_man = carregar('manutencao')
    df_com = carregar('comercial')
    df_esc = carregar('escala')
    df_sta = carregar('stands')
    df_usr = carregar('usuarios')

    stands_ativos = len(df_sta[df_sta['Status'] == 'Ativo'])          if not df_sta.empty else 0
    man_pendentes = len(df_man[df_man['Status'] == 'Pendente'])        if not df_man.empty else 0
    escalas_hoje  = len(df_esc[df_esc['Data'] == str(date.today())])  if not df_esc.empty else 0
    usuarios_atv  = len(df_usr[df_usr['Ativo'] == 'Sim'])              if not df_usr.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🏪 Stands Ativos",         stands_ativos)
    c2.metric("🛠️ Manutenções Pendentes", man_pendentes)
    c3.metric("📅 Escalas Hoje",           escalas_hoje)
    c4.metric("👥 Usuários Ativos",        usuarios_atv)

    st.markdown("<br>", unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### 🛠️ Últimas Manutenções")
        if not df_man.empty:
            st.dataframe(
                df_man[['ID','Data','Stand','Descricao','Status']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma manutenção registrada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with cb:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("#### 🤝 Últimas Negociações")
        if not df_com.empty:
            st.dataframe(
                df_com[['ID','Data','Cliente','Stand','Etapa']].tail(5),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("Nenhuma negociação registrada.")
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 11. ESCALA DE TRABALHO
# ============================================================
elif modulo == "📅  Escala de Trabalho":
    hoje = datetime.now()
    page_header("📅", "Escala de Trabalho",
                f"{calendar.month_name[hoje.month]} / {hoje.year}")

    df_esc = carregar('escala')
    cal    = calendar.monthcalendar(hoje.year, hoje.month)
    nomes  = ["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"]

    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    cab = st.columns(7)
    for i, n in enumerate(nomes):
        cab[i].markdown(
            f"<p style='text-align:center;font-weight:700;"
            f"color:#1e3a8a;font-size:0.85rem;margin:0;'>{n}</p>",
            unsafe_allow_html=True
        )

    dia_sel = None
    for semana in cal:
        cols = st.columns(7)
        for i, dia in enumerate(semana):
            if dia == 0:
                cols[i].write("")
            else:
                data_str   = f"{hoje.year}-{hoje.month:02d}-{dia:02d}"
                tem_escala = (not df_esc.empty and (df_esc['Data'] == data_str).any())
                if cols[i].button(
                    str(dia) + ("📌" if tem_escala else ""),
                    key=f"cal_{dia}",
                    use_container_width=True
                ):
                    dia_sel = data_str

    st.markdown("</div>", unsafe_allow_html=True)

    if dia_sel:
        esc_dia = df_esc[df_esc['Data'] == dia_sel] if not df_esc.empty else pd.DataFrame()
        if not esc_dia.empty:
            st.success(f"📋 Escala de {dia_sel}:")
            st.dataframe(
                esc_dia[['Colaborador','Setor','Stand','Turno','Status']],
                use_container_width=True, hide_index=True
            )
        else:
            st.info(f"Sem escala para {dia_sel}.")

    if NIVEL in ['Admin', 'Editor']:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ➕ Gerenciar Escala")
        colaboradores = get_usuarios_ativos()
        stands_list   = get_stands()

        with st.form("form_escala"):
            c1, c2, c3 = st.columns(3)
            data_esc  = c1.date_input("Data", value=date.today())
            colab     = c2.selectbox("Colaborador", colaboradores)
            setor_esc = c3.selectbox("Setor", [
                "Manutenção","Comercial","Financeiro","Marketing","Compras","Diretoria"
            ])
            c4, c5, c6 = st.columns(3)
            stand_esc = c4.selectbox("Stand / Local", stands_list + ["Escritório Central"])
            turno     = c5.selectbox("Turno", ["Manhã","Tarde","Integral","Noite"])
            status_e  = c6.selectbox("Status", ["Confirmado","Pendente","Folga","Ausência"])

            if st.form_submit_button("✅ Registrar Escala", use_container_width=True):
                dia_nome = nomes[data_esc.weekday()]
                nova = pd.DataFrame([[
                    proximo_id(df_esc), str(data_esc), dia_nome,
                    colab, setor_esc, stand_esc, turno, status_e
                ]], columns=COLUNAS['escala'])
                df_esc = pd.concat([df_esc, nova], ignore_index=True)
                salvar(df_esc, 'escala')
                st.success(f"✅ {colab} escalado(a) em {stand_esc} — {data_esc}!")
                st.rerun()

        if not df_esc.empty:
            with st.expander("📋 Ver / Remover Escalas"):
                st.dataframe(df_esc, use_container_width=True, hide_index=True)
                id_del = st.number_input("ID para remover:", min_value=1, step=1, key="del_esc")
                if st.button("🗑️ Remover", key="btn_del_esc"):
                    df_esc = df_esc[df_esc['ID'] != id_del]
                    salvar(df_esc, 'escala')
                    st.success("Removido!")
                    st.rerun()

# ============================================================
# 12. MANUTENÇÃO
# ============================================================
elif modulo == "🛠️  Manutenção":
    page_header("🛠️", "Gestão de Manutenção",
                "Ordens de serviço, acompanhamento técnico e histórico dos stands")

    df_man      = carregar('manutencao')
    stands_list = get_stands()

    tab1, tab2, tab3 = st.tabs([
        "📋  Painel de OS",
        "➕  Abrir Chamado",
        "🔧  Atualizar OS"
    ])

    # ── TAB 1: PAINEL ──────────────────────────────────────
    with tab1:
        if df_man.empty:
            st.info("Nenhuma ordem de serviço registrada.")
        else:
            cf1, cf2, cf3 = st.columns(3)
            f_stand  = cf1.multiselect("Stand:", stands_list, default=stands_list)
            f_status = cf2.multiselect(
                "Status:",
                ["Pendente","Em Andamento","Aguardando Material","Concluído","Cancelado"],
                default=["Pendente","Em Andamento","Aguardando Material"]
            )
            f_urg = cf3.multiselect(
                "Urgência:", ["Alta","Média","Baixa"], default=["Alta","Média","Baixa"]
            )
            df_vis = df_man[
                df_man['Stand'].isin(f_stand) &
                df_man['Status'].isin(f_status) &
                df_man['Urgencia'].isin(f_urg)
            ]

            for _, row in df_vis.iterrows():
                urg_class = {"Alta":"os-card-alta","Média":"os-card-media","Baixa":"os-card-baixa"}.get(str(row.get('Urgencia','')), "")
                badge_map = {
                    "Pendente":"badge-pendente","Em Andamento":"badge-andamento",
                    "Aguardando Material":"badge-material",
                    "Concluído":"badge-concluido","Cancelado":"badge-cancelado"
                }
                badge_cls = badge_map.get(str(row.get('Status','')), "")
                prazo_txt = f"&nbsp;|&nbsp;⏰ Prazo: {row.get('Prazo','')}" if str(row.get('Prazo','')) not in ['','nan'] else ''
                pedido_txt = f"<div style='margin-top:6px;font-size:0.8rem;color:#7c3aed;'>📦 Pedido Compras: {row.get('PedidoCompras','')}</div>" if str(row.get('PedidoCompras','')) not in ['','nan'] else ''
                obs_txt = f"<div style='margin-top:4px;font-size:0.8rem;color:#64748b;'>💬 {row.get('Obs','')}</div>" if str(row.get('Obs','')) not in ['','nan'] else ''

                st.markdown(f"""
                    <div class='os-card {urg_class}'>
                        <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;'>
                            <div>
                                <span style='font-weight:800;font-size:1rem;color:#0f172a;'>OS #{int(row['ID'])}</span>
                                &nbsp;<span class='status-badge {badge_cls}'>{row.get('Status','')}</span>
                                &nbsp;<span style='font-size:0.8rem;color:#64748b;'>⚡ {row.get('Urgencia','')}</span>
                            </div>
                            <span style='font-size:0.8rem;color:#94a3b8;'>📅 {row.get('Data','')}{prazo_txt}</span>
                        </div>
                        <div style='margin-top:8px;'>
                            <span style='font-size:0.85rem;color:#334155;'>
                                🏪 <b>{row.get('Stand','')}</b> &nbsp;|&nbsp; 👷 {row.get('Responsavel','')}
                            </span>
                        </div>
                        <div style='margin-top:6px;font-size:0.88rem;color:#475569;'>{str(row.get('Descricao',''))[:180]}</div>
                        {pedido_txt}{obs_txt}
                    </div>
                """, unsafe_allow_html=True)

                foto_antes  = decode_img(str(row.get('FotoAntes', '')))
                foto_depois = decode_img(str(row.get('FotoDepois', '')))
                if foto_antes or foto_depois:
                    col_f1, col_f2 = st.columns(2)
                    if foto_antes:
                        with col_f1:
                            st.markdown("<p class='foto-label'>📷 Foto Antes</p>", unsafe_allow_html=True)
                            st.image(foto_antes, use_container_width=True)
                    if foto_depois:
                        with col_f2:
                            st.markdown("<p class='foto-label'>📷 Foto Depois</p>", unsafe_allow_html=True)
                            st.image(foto_depois, use_container_width=True)

    # ── TAB 2: ABRIR CHAMADO ───────────────────────────────
    with tab2:
        if NIVEL in ['Admin', 'Editor']:
            colaboradores = get_usuarios_ativos()
            form_key = f"form_man_{st.session_state['man_form_key']}"

            with st.form(form_key, clear_on_submit=True):
                st.markdown("#### 📋 Dados da Ocorrência")
                c1, c2, c3 = st.columns(3)
                stand_m = c1.selectbox("Stand:", stands_list)
                resp_m  = c2.selectbox("Responsável:", colaboradores)
                urg_m   = c3.select_slider("Urgência:", ["Baixa","Média","Alta"])
                desc_m  = st.text_area(
                    "📝 Descrição detalhada do problema:", height=120,
                    placeholder="Descreva o problema com o máximo de detalhes possível..."
                )
                st.markdown("#### 📷 Foto do Problema (Antes)")
                foto_antes_up = st.file_uploader(
                    "Anexar foto",
                    type=["jpg","jpeg","png","webp"],
                    key=f"foto_antes_{st.session_state['man_form_key']}"
                )

                if st.form_submit_button("🚀 Abrir Ordem de Serviço", use_container_width=True):
                    if desc_m.strip():
                        df_man = carregar('manutencao')
                        nova = pd.DataFrame([[
                            proximo_id(df_man),
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            stand_m, desc_m, resp_m, urg_m,
                            "Pendente", "", encode_img(foto_antes_up), "", "", ""
                        ]], columns=COLUNAS['manutencao'])
                        df_man = pd.concat([df_man, nova], ignore_index=True)
                        salvar(df_man, 'manutencao')
                        st.session_state['man_form_key'] += 1
                        st.success("✅ OS aberta! Formulário limpo para novo chamado.")
                        st.rerun()
                    else:
                        st.warning("Descreva o problema antes de abrir o chamado.")
        else:
            st.warning("Apenas Editores e Admins podem abrir chamados.")

    # ── TAB 3: ATUALIZAR OS ────────────────────────────────
    with tab3:
        if NIVEL in ['Admin', 'Editor']:
            df_man = carregar('manutencao')
            if df_man.empty:
                st.info("Nenhuma OS registrada.")
            else:
                ids_abertos = df_man[~df_man['Status'].isin(['Concluído','Cancelado'])]['ID'].tolist()
                if not ids_abertos:
                    st.success("🎉 Todas as OS estão concluídas ou canceladas!")
                else:
                    id_sel = st.selectbox(
                        "Selecione a OS:",
                        ids_abertos,
                        format_func=lambda x: (
                            f"OS #{x} — "
                            f"{df_man[df_man['ID']==x]['Stand'].values[0]} | "
                            f"{str(df_man[df_man['ID']==x]['Descricao'].values[0])[:50]}..."
                        )
                    )
                    os_row = df_man[df_man['ID'] == id_sel].iloc[0]

                    st.markdown(f"""
                        <div class='custom-card'>
                            <b>OS #{int(os_row['ID'])}</b> &nbsp;|&nbsp;
                            🏪 {os_row.get('Stand','')} &nbsp;|&nbsp;
                            👷 {os_row.get('Responsavel','')} &nbsp;|&nbsp;
                            ⚡ {os_row.get('Urgencia','')} &nbsp;|&nbsp;
                            📅 Abertura: {os_row.get('Data','')}
                            <br><br>
                            <span style='color:#475569'>{os_row.get('Descricao','')}</span>
                        </div>
                    """, unsafe_allow_html=True)

                    with st.form("form_upd_os"):
                        status_opcoes = ["Pendente","Em Andamento","Aguardando Material","Concluído","Cancelado"]
                        status_atual  = str(os_row.get('Status','Pendente'))
                        idx_status    = status_opcoes.index(status_atual) if status_atual in status_opcoes else 0

                        c1, c2 = st.columns(2)
                        novo_status = c1.selectbox("Novo Status:", status_opcoes, index=idx_status)
                        pra

