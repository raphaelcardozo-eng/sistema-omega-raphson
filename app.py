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
                    not df_esc.empty and
                    (df_esc['Data'] == data_str).any()
                )
                label = f"**{dia}**" + (" 📌" if tem_escala else "")
                if cols[i].button(str(dia), key=f"cal_{dia}", use_container_width=True):
                    dia_selecionado = data_str

    # Exibir escala do dia clicado
    if dia_selecionado and not df_esc.empty:
        esc_dia = df_esc[df_esc['Data'] == dia_selecionado]
        if not esc_dia.empty:
            st.success(f"📋 Escala do dia {dia_selecionado}:")
            st.dataframe(
                esc_dia[['Colaborador','Setor','Stand','Turno','Status']],
                use_container_width=True, hide_index=True
            )
        else:
            st.info(f"Sem escala cadastrada para {dia_selecionado}.")

    st.markdown("---")

    # Formulário de gestão (Editor e Admin)
    if NIVEL in ['Admin', 'Editor']:
        st.subheader("➕ Adicionar / Gerenciar Escala")
        colaboradores = get_usuarios_ativos()
        stands_list   = get_stands()

        with st.form("form_escala"):
            c1, c2, c3 = st.columns(3)
            data_esc   = c1.date_input("Data", value=date.today())
            colab      = c2.selectbox("Colaborador", colaboradores)
            setor_esc  = c3.selectbox("Setor", ["Manutenção","Comercial","Financeiro","Marketing","Compras","Diretoria"])

            c4, c5, c6 = st.columns(3)
            stand_esc  = c4.selectbox("Stand / Local", stands_list + ["Escritório Central"])
            turno      = c5.selectbox("Turno", ["Manhã","Tarde","Integral","Noite"])
            status_esc = c6.selectbox("Status", ["Confirmado","Pendente","Folga","Ausência"])

            if st.form_submit_button("✅ Registrar na Escala", use_container_width=True):
                dia_nome = nomes_dias[data_esc.weekday()]
                nova = pd.DataFrame([[
                    proximo_id(df_esc),
                    str(data_esc), dia_nome,
                    colab, setor_esc, stand_esc, turno, status_esc
                ]], columns=COLUNAS['escala'])
                df_esc = pd.concat([df_esc, nova], ignore_index=True)
                salvar(df_esc, 'escala')
                st.success(f"✅ {colab} escalado em {stand_esc} para {data_esc}!")
                st.rerun()

        # Gerenciar escalas existentes
        if not df_esc.empty:
            st.markdown("#### 📋 Escala Completa")
            st.dataframe(df_esc, use_container_width=True, hide_index=True)

            with st.expander("🗑️ Remover registro de escala"):
                id_del = st.number_input("ID do registro a remover", min_value=1, step=1)
                if st.button("Confirmar Remoção"):
                    df_esc = df_esc[df_esc['ID'] != id_del]
                    salvar(df_esc, 'escala')
                    st.success("Registro removido.")
                    st.rerun()
    else:
        st.info("Apenas Editores e Admins podem gerenciar a escala.")
        if not df_esc.empty:
            st.dataframe(df_esc, use_container_width=True, hide_index=True)

# ============================================================
# 13. MÓDULO — MANUTENÇÃO
# ============================================================
elif modulo == "🛠️ Manutenção":
    st.title("🛠️ Gestão de Manutenção")
    df_man    = carregar('manutencao')
    stands_list = get_stands()

    tab1, tab2 = st.tabs(["📋 Painel de OS", "➕ Abrir Novo Chamado"])

    with tab1:
        if df_man.empty:
            st.info("Nenhuma ordem de serviço aberta.")
        else:
            col_f1, col_f2 = st.columns(2)
            filtro_stand  = col_f1.multiselect("Filtrar por Stand:",  stands_list, default=stands_list)
            filtro_status = col_f2.multiselect(
                "Filtrar por Status:",
                ["Pendente","Em Andamento","Concluído","Cancelado"],
                default=["Pendente","Em Andamento"]
            )
            df_vis = df_man[
                df_man['Stand'].isin(filtro_stand) &
                df_man['Status'].isin(filtro_status)
            ]
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

            if NIVEL in ['Admin', 'Editor']:
                st.markdown("---")
                st.subheader("🔄 Atualizar Status de OS")
                c1, c2, c3 = st.columns(3)
                ids_disp   = df_man['ID'].tolist()
                id_upd     = c1.selectbox("ID da OS:", ids_disp)
                novo_status = c2.selectbox("Novo Status:", ["Pendente","Em Andamento","Concluído","Cancelado"])
                responsavel_upd = c3.text_input("Atualizar Responsável (opcional)")
                if st.button("✅ Confirmar Atualização"):
                    df_man.loc[df_man['ID'] == id_upd, 'Status'] = novo_status
                    if responsavel_upd:
                        df_man.loc[df_man['ID'] == id_upd, 'Responsavel'] = responsavel_upd
                    salvar(df_man, 'manutencao')
                    st.success(f"OS #{id_upd} atualizada para '{novo_status}'!")
                    st.rerun()

    with tab2:
        if NIVEL in ['Admin', 'Editor']:
            colaboradores = get_usuarios_ativos()
            with st.form("form_manutencao"):
                c1, c2, c3 = st.columns(3)
                stand_man  = c1.selectbox("Stand:", stands_list)
                resp_man   = c2.selectbox("Responsável:", colaboradores)
                urgencia   = c3.select_slider("Urgência:", ["Baixa","Média","Alta"])
                desc_man   = st.text_area("Descrição detalhada do problema:")
                if st.form_submit_button("🚀 Abrir Ordem de Serviço", use_container_width=True):
                    if desc_man:
                        nova = pd.DataFrame([[
                            proximo_id(df_man),
                            datetime.now().strftime("%d/%m/%Y %H:%M"),
                            stand_man, desc_man, resp_man, urgencia, "Pendente"
                        ]], columns=COLUNAS['manutencao'])
                        df_man = pd.concat([df_man, nova], ignore_index=True)
                        salvar(df_man, 'manutencao')
                        st.success(f"✅ OS #{proximo_id(df_man)-1} aberta para {resp_man}!")
                        st.rerun()
                    else:
                        st.warning("Descreva o problema antes de abrir o chamado.")
        else:
            st.warning("Apenas Editores e Admins podem abrir chamados.")

# ============================================================
# 14. MÓDULO — COMERCIAL
# ============================================================
elif modulo == "🤝 Comercial":
    st.title("🤝 Gestão Comercial")
    df_com    = carregar('comercial')
    stands_list = get_stands()

    tab1, tab2 = st.tabs(["📋 Negociações Ativas", "➕ Novo Lead / Negociação"])

    with tab1:
        if df_com.empty:
            st.info("Nenhuma negociação registrada.")
        else:
            filtro_etapa = st.multiselect(
                "Filtrar por Etapa:",
                ["Prospecção","Proposta","Negociação","Fechado","Perdido"],
                default=["Prospecção","Proposta","Negociação"]
            )
            df_vis = df_com[df_com['Etapa'].isin(filtro_etapa)] if filtro_etapa else df_com
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

            if NIVEL in ['Admin', 'Editor'] and not df_com.empty:
                st.markdown("---")
                st.subheader("🔄 Atualizar Etapa")
                c1, c2 = st.columns(2)
                id_com  = c1.selectbox("ID:", df_com['ID'].tolist())
                etapa_n = c2.selectbox("Nova Etapa:", ["Prospecção","Proposta","Negociação","Fechado","Perdido"])
                if st.button("✅ Atualizar"):
                    df_com.loc[df_com['ID'] == id_com, 'Etapa'] = etapa_n
                    salvar(df_com, 'comercial')
                    st.success("Etapa atualizada!")
                    st.rerun()

    with tab2:
        if NIVEL in ['Admin', 'Editor']:
            colaboradores = get_usuarios_ativos()
            with st.form("form_comercial"):
                c1, c2 = st.columns(2)
                cliente  = c1.text_input("Nome do Cliente / Empresa")
                contato  = c2.text_input("WhatsApp / E-mail")
                c3, c4, c5 = st.columns(3)
                stand_c  = c3.selectbox("Stand de Interesse:", stands_list)
                produto  = c4.text_input("Produto / Serviço")
                etapa_c  = c5.selectbox("Etapa:", ["Prospecção","Proposta","Negociação","Fechado","Perdido"])
                resp_c   = st.selectbox("Vendedor Responsável:", colaboradores)
                obs_c    = st.text_area("Observações:")
                if st.form_submit_button("💼 Registrar Negociação", use_container_width=True):
                    if cliente:
                        nova = pd.DataFrame([[
                            proximo_id(df_com),
                            datetime.now().strftime("%d/%m/%Y"),
                            cliente, contato, stand_c, produto, etapa_c, resp_c, obs_c
                        ]], columns=COLUNAS['comercial'])
                        df_com = pd.concat([df_com, nova], ignore_index=True)
                        salvar(df_com, 'comercial')
                        st.success(f"✅ Lead '{cliente}' registrado!")
                        st.rerun()
                    else:
                        st.warning("Informe o nome do cliente.")
        else:
            st.warning("Apenas Editores e Admins podem registrar negociações.")

# ============================================================
# 15. MÓDULO — FINANCEIRO (SOMENTE ADMIN/EDITOR)
# ============================================================
elif modulo == "💰 Financeiro":
    st.title("💰 Controle Financeiro")
    df_fin = carregar('financeiro')

    tab1, tab2 = st.tabs(["📊 Resumo Financeiro", "➕ Novo Lançamento"])

    with tab1:
        if df_fin.empty:
            st.info("Nenhum lançamento registrado.")
        else:
            total_ent = df_fin[df_fin['Tipo'] == 'Entrada']['Valor'].astype(float).sum()
            total_sai = df_fin[df_fin['Tipo'] == 'Saída']['Valor'].astype(float).sum()
            saldo     = total_ent - total_sai

            c1, c2, c3 = st.columns(3)
            c1.metric("💚 Total Entradas",  f"R$ {total_ent:,.2f}")
            c2.metric("🔴 Total Saídas",    f"R$ {total_sai:,.2f}")
            c3.metric("🔵 Saldo",           f"R$ {saldo:,.2f}")
            st.dataframe(df_fin, use_container_width=True, hide_index=True)

    with tab2:
        with st.form("form_fin"):
            c1, c2, c3 = st.columns(3)
            tipo_fin  = c1.selectbox("Tipo:", ["Entrada","Saída"])
            cat_fin   = c2.selectbox("Categoria:", ["Fornecedor","Salário","Material","Receita","Imposto","Outros"])
            valor_fin = c3.number_input("Valor (R$):", min_value=0.0, step=0.01, format="%.2f")
            desc_fin  = st.text_input("Descrição:")
            resp_fin  = st.text_input("Responsável:")
            if st.form_submit_button("💾 Registrar Lançamento", use_container_width=True):
                nova = pd.DataFrame([[
                    proximo_id(df_fin),
                    datetime.now().strftime("%d/%m/%Y"),
                    tipo_fin, cat_fin, desc_fin, valor_fin, resp_fin
                ]], columns=COLUNAS['financeiro'])
                df_fin = pd.concat([df_fin, nova], ignore_index=True)
                salvar(df_fin, 'financeiro')
                st.success("✅ Lançamento registrado!")
                st.rerun()

# ============================================================
# 16. MÓDULO — MARKETING
# ============================================================
elif modulo == "📣 Marketing":
    st.title("📣 Gestão de Marketing")
    df_mkt    = carregar('marketing')
    stands_list = get_stands()

    tab1, tab2 = st.tabs(["📋 Campanhas Ativas", "➕ Nova Solicitação"])

    with tab1:
        if df_mkt.empty:
            st.info("Nenhuma campanha registrada.")
        else:
            st.dataframe(df_mkt, use_container_width=True, hide_index=True)

    with tab2:
        colaboradores = get_usuarios_ativos()
        with st.form("form_mkt"):
            c1, c2 = st.columns(2)
            campanha = c1.text_input("Nome da Campanha / Ação")
            tipo_mkt = c2.selectbox("Tipo:", ["Banner","Post Redes Sociais","E-mail Marketing","Evento","Outro"])
            c3, c4, c5 = st.columns(3)
            resp_mkt  = c3.selectbox("Responsável:", colaboradores)
            stand_mkt = c4.selectbox("Stand / Local:", stands_list + ["Todos","Digital"])
            prazo_mkt = c5.date_input("Prazo:")
            if st.form_submit_button("📣 Registrar Campanha", use_container_width=True):
                if campanha:
                    nova = pd.DataFrame([[
                        proximo_id(df_mkt),
                        datetime.now().strftime("%d/%m/%Y"),
                        campanha, tipo_mkt, resp_mkt, stand_mkt, "Em Andamento", str(prazo_mkt)
                    ]], columns=COLUNAS['marketing'])
                    df_mkt = pd.concat([df_mkt, nova], ignore_index=True)
                    salvar(df_mkt, 'marketing')
                    st.success("✅ Campanha registrada!")
                    st.rerun()
                else:
                    st.warning("Informe o nome da campanha.")

# ============================================================
# 17. MÓDULO — COMPRAS
# ============================================================
elif modulo == "🛒 Compras":
    st.title("🛒 Gestão de Compras")
    df_cmp = carregar('compras')

    tab1, tab2 = st.tabs(["📋 Pedidos em Aberto", "➕ Novo Pedido"])

    with tab1:
        if df_cmp.empty:
            st.info("Nenhum pedido registrado.")
        else:
            filtro_st = st.multiselect(
                "Filtrar por Status:",
                ["Pendente","Em Cotação","Aprovado","Entregue","Cancelado"],
                default=["Pendente","Em Cotação"]
            )
            df_vis = df_cmp[df_cmp['Status'].isin(filtro_st)] if filtro_st else df_cmp
            st.dataframe(df_vis, use_container_width=True, hide_index=True)

            if NIVEL in ['Admin', 'Editor']:
                c1, c2 = st.columns(2)
                id_cp  = c1.selectbox("ID do Pedido:", df_cmp['ID'].tolist())
                st_cp  = c2.selectbox("Novo Status:", ["Pendente","Em Cotação","Aprovado","Entregue","Cancelado"])
                if st.button("✅ Atualizar Pedido"):
                    df_cmp.loc[df_cmp['ID'] == id_cp, 'Status'] = st_cp
                    salvar(df_cmp, 'compras')
                    st.success("Pedido atualizado!")
                    st.rerun()

    with tab2:
        with st.form("form_compras"):
            c1, c2, c3 = st.columns(3)
            item_cp  = c1.text_input("Item / Material")
            qtd_cp   = c2.number_input("Quantidade:", min_value=1, step=1)
            unid_cp  = c3.selectbox("Unidade:", ["Un","Kg","Lt","M","M²","Caixa","Pacote"])
            c4, c5, c6 = st.columns(3)
            solic_cp = c4.text_input("Solicitante")
            setor_cp = c5.selectbox("Setor:", ["Manutenção","Obra","Escritório","Marketing","Comercial"])
            urg_cp   = c6.select_slider("Urgência:", ["Baixa","Média","Alta"])
            if st.form_submit_button("🛒 Enviar Pedido", use_container_width=True):
                if item_cp and solic_cp:
                    nova = pd.DataFrame([[
                        proximo_id(df_cmp),
                        datetime.now().strftime("%d/%m/%Y"),
                        item_cp, qtd_cp, unid_cp, solic_cp, setor_cp, urg_cp, "Pendente"
                    ]], columns=COLUNAS['compras'])
                    df_cmp = pd.concat([df_cmp, nova], ignore_index=True)
                    salvar(df_cmp, 'compras')
                    st.success("✅ Pedido enviado para cotação!")
                    st.rerun()
                else:
                    st.warning("Informe o item e o solicitante.")

# ============================================================
# 18. MÓDULO — CADASTROS & CONFIGURAÇÕES (SOMENTE ADMIN)
# ============================================================
elif modulo == "⚙️ Cadastros & Configurações":
    st.title("⚙️ Cadastros & Configurações")
    tab_usr, tab_std, tab_inv = st.tabs(["👥 Usuários", "🏪 Stands", "📦 Inventário"])

    # ---------- USUÁRIOS ----------
    with tab_usr:
        st.subheader("👥 Usuários Cadastrados")
        df_usr = carregar('usuarios')
        st.dataframe(
            df_usr[['ID','Nome','Email','Setor','Nivel','Ativo']],
            use_container_width=True, hide_index=True
        )

        sub1, sub2, sub3 = st.tabs(["➕ Novo Usuário", "✏️ Alterar Senha", "❌ Excluir Usuário"])

        with sub1:
            with st.form("form_novo_user"):
                c1, c2 = st.columns(2)
                nome_u  = c1.text_input("Nome Completo")
                email_u = c2.text_input("E-mail Corporativo")
                c3, c4, c5 = st.columns(3)
                senha_u  = c3.text_input("Senha Inicial", type="password")
                setor_u  = c4.selectbox("Setor:", ["Diretoria","Engenharia","Manutenção","Comercial","Financeiro","Marketing","Compras"])
                nivel_u  = c5.select_slider("Nível de Acesso:", ["Leitor","Editor","Admin"])
                if st.form_submit_button("✅ Cadastrar Usuário", use_container_width=True):
                    if nome_u and email_u and senha_u:
                        df_usr2 = carregar('usuarios')
                        if (df_usr2['Email'].str.lower() == email_u.lower()).any():
                            st.error("E-mail já cadastrado.")
                        else:
                            nova = pd.DataFrame([[
                                proximo_id(df_usr2),
                                nome_u, email_u, senha_u, setor_u, nivel_u, "Sim"
                            ]], columns=COLUNAS['usuarios'])
                            df_usr2 = pd.concat([df_usr2, nova], ignore_index=True)
                            salvar(df_usr2, 'usuarios')
                            st.success(f"✅ Usuário '{nome_u}' cadastrado!")
                            st.rerun()
                    else:
                        st.warning("Preencha todos os campos obrigatórios.")

        with sub2:
            with st.form("form_alt_senha"):
                email_alt = st.text_input("E-mail do usuário")
                nova_s    = st.text_input("Nova Senha", type="password")
                conf_s    = st.text_input("Confirmar Senha", type="password")
                if st.form_submit_button("🔑 Alterar Senha", use_container_width=True):
                    if nova_s != conf_s:
                        st.error("As senhas não coincidem.")
                    else:
                        df_usr2 = carregar('usuarios')
                        mask = df_usr2['Email'].str.lower() == email_alt.lower()
                        if mask.any():
                            df_usr2.loc[mask, 'Senha'] = nova_s
                            salvar(df_usr2, 'usuarios')
                            st.success("✅ Senha alterada com sucesso!")
                        else:
                            st.error("Usuário não encontrado.")

        with sub3:
            with st.form("form_del_user"):
                st.warning("⚠️ Atenção: esta ação desativa o acesso do usuário.")
                email_del = st.text_input("E-mail do usuário a desativar")
                conf_del  = st.checkbox("Confirmo que desejo desativar este usuário.")
                if st.form_submit_button("❌ Desativar Usuário", use_container_width=True):
                    if conf_del and email_del:
                        df_usr2 = carregar('usuarios')
                        mask = df_usr2['Email'].str.lower() == email_del.lower()
                        if mask.any():
                            df_usr2.loc[mask, 'Ativo'] = 'Não'
                            salvar(df_usr2, 'usuarios')
                            st.success("Usuário desativado.")
                            st.rerun()
                        else:
                            st.error("Usuário não encontrado.")
                    elif not conf_del:
                        st.warning("Marque a confirmação.")

    # ---------- STANDS ----------
    with tab_std:
        st.subheader("🏪 Stands Cadastrados")
        df_std = carregar('stands')
        st.dataframe(df_std, use_container_width=True, hide_index=True)

        sub_a, sub_b = st.tabs(["➕ Novo Stand", "✏️ Editar Status"])

        with sub_a:
            with st.form("form_stand"):
                c1, c2 = st.columns(2)
                nome_s = c1.text_input("Nome do Stand")
                end_s  = c2.text_input("Endereço / Localização")
                resp_s = st.text_input("Responsável")
                if st.form_submit_button("✅ Cadastrar Stand", use_container_width=True):
                    if nome_s:
                        nova = pd.DataFrame([[
                            proximo_id(df_std), nome_s, end_s, "Ativo", resp_s
                        ]], columns=COLUNAS['stands'])
                        df_std = pd.concat([df_std, nova], ignore_index=True)
                        salvar(df_std, 'stands')
                        st.success(f"✅ Stand '{nome_s}' cadastrado!")
                        st.rerun()
                    else:
                        st.warning("Informe o nome do stand.")

        with sub_b:
            if not df_std.empty:
                c1, c2 = st.columns(2)
                id_std  = c1.selectbox("ID do Stand:", df_std['ID'].tolist())
                st_std  = c2.selectbox("Novo Status:", ["Ativo","Inativo","Em Manutenção"])
                if st.button("✅ Atualizar Stand"):
                    df_std.loc[df_std['ID'] == id_std, 'Status'] = st_std
                    salvar(df_std, 'stands')
                    st.success("Stand atualizado!")
                    st.rerun()

    # ---------- INVENTÁRIO ----------
    with tab_inv:
        st.subheader("📦 Inventário")
        df_inv    = carregar('inventario')
        stands_list = get_stands()

        if not df_inv.empty:
            st.dataframe(df_inv, use_container_width=True, hide_index=True)

        with st.form("form_inv"):
            c1, c2, c3 = st.columns(3)
            item_i  = c1.text_input("Item / Equipamento")
            cat_i   = c2.selectbox("Categoria:", ["Ferramenta","Equipamento","Material","EPI","Mobiliário","Outro"])
            qtd_i   = c3.number_input("Quantidade:", min_value=0, step=1)
            c4, c5, c6 = st.columns(3)
            unid_i  = c4.selectbox("Unidade:", ["Un","Kg","Lt","M","Par","Conjunto"])
            stand_i = c5.selectbox("Stand / Local:", stands_list + ["Almoxarifado","Escritório"])
            stat_i  = c6.selectbox("Estado:", ["Disponível","Em Uso","Em Manutenção","Descartado"])
            if st.form_submit_button("📦 Registrar Item", use_container_width=True):
                if item_i:
                    nova = pd.DataFrame([[
                        proximo_id(df_inv), item_i, cat_i, qtd_i, unid_i, stand_i, stat_i
                    ]], columns=COLUNAS['inventario'])
                    df_inv = pd.concat([df_inv, nova], ignore_index=True)
                    salvar(df_inv, 'inventario')
                    st.success(f"✅ '{item_i}' registrado no inventário!")
                    st.rerun()
                else:
                    st.warning("Informe o nome do item.")
