import streamlit as st
import pandas as pd
from PIL import Image
import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide", initial_sidebar_state="expanded")

def carregar_logo():
    try:
        return Image.open("Image_from_Image.jpg")
    except FileNotFoundError:
        return None

# --- INICIALIZAÇÃO DE BANCO DE DADOS TEMPORÁRIO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
if 'pagina_atual' not in st.session_state:
    st.session_state['pagina_atual'] = "Painel de Gestão"
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = ""

# Tabelas (Persistência em sessão)
if 'usuarios' not in st.session_state:
    st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphaelcardozo@raphsonengenharia.com.br", "Perfil": "Diretor", "Senha": "1234", "Primeiro_Acesso": False, "Data_Ultima_Senha": datetime.date.today(), "Status": "Ativo"}])
if 'stands' not in st.session_state:
    st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Prazo de Locação", "Status"])
if 'centros_custo' not in st.session_state:
    st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Descrição", "Status"])
if 'chamados' not in st.session_state:
    st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
if 'solicitacoes_material' not in st.session_state:
    st.session_state['solicitacoes_material'] = []

# --- TELAS DE ACESSO ---
def tela_login():
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        logo = carregar_logo()
        if logo: st.image(logo, use_container_width=True)
        st.markdown("<h4 style='text-align: center;'>Acesso Restrito</h4>", unsafe_allow_html=True)
        with st.form("login_form"):
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.form_submit_button("Entrar", use_container_width=True):
                df_users = st.session_state['usuarios']
                user_match = df_users[(df_users['Email'] == user) & (df_users['Senha'] == senha)]
                if not user_match.empty:
                    st.session_state['autenticado'] = True
                    st.session_state['usuario_logado'] = user
                    st.rerun()
                else:
                    st.error("Credenciais inválidas.")

# --- MÓDULOS ---

def module_painel_gestao():
    st.header("📊 Painel de Gestão")
    col1, col2, col3, col4 = st.columns(4)
    abertos = len(st.session_state['chamados'][st.session_state['chamados']['Status'] != 'Concluído'])
    col1.metric("OS Ativas", abertos)
    col2.metric("Lead Time", "4 dias")
    col3.metric("Custos", "R$ 145k")
    col4.metric("MKT", "3 Ativas")
    
    st.divider()
    st.subheader("📋 Tarefas por Setor")
    c1, c2, c3 = st.columns(3)
    with c1: st.info("**Manutenção:** Aprovar OS-001")
    with c2: st.success("**Compras:** Cotação de Tintas")
    with c3: st.error("**Financeiro:** Fornecedor X")

def module_cadastro():
    st.header("📝 Cadastro")
    tab1, tab2, tab3 = st.tabs(["Usuários", "Stands", "Centros de Custo"])
    with tab1:
        with st.expander("➕ Novo Usuário"):
            with st.form("f_user", clear_on_submit=True):
                n = st.text_input("Nome")
                e = st.text_input("Email")
                s = st.text_input("Senha", type="password")
                if st.form_submit_button("Salvar"):
                    new = pd.DataFrame([{"Nome": n, "Email": e, "Perfil": "Gestor", "Senha": s, "Primeiro_Acesso": True, "Data_Ultima_Senha": datetime.date.today(), "Status": "Ativo"}])
                    st.session_state['usuarios'] = pd.concat([st.session_state['usuarios'], new], ignore_index=True)
                    st.rerun()
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], use_container_width=True)

    with tab2:
        with st.expander("➕ Novo Stand"):
            with st.form("f_stand", clear_on_submit=True):
                ns = st.text_input("Nome do Stand")
                if st.form_submit_button("Salvar Stand"):
                    new_s = pd.DataFrame([{"Nome do Stand": ns, "Endereço": "", "Prazo de Locação": "", "Status": "Ativo"}])
                    st.session_state['stands'] = pd.concat([st.session_state['stands'], new_s], ignore_index=True)
                    st.rerun()
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], use_container_width=True)

    with tab3:
        with st.expander("➕ Novo Centro de Custo"):
            with st.form("f_cc", clear_on_submit=True):
                ncc = st.text_input("Nome CC")
                cnpj = st.text_input("CNPJ")
                if st.form_submit_button("Salvar CC"):
                    new_cc = pd.DataFrame([{"Nome do Centro de Custo": ncc, "CNPJ": cnpj, "Descrição": "", "Status": "Ativo"}])
                    st.session_state['centros_custo'] = pd.concat([st.session_state['centros_custo'], new_cc], ignore_index=True)
                    st.rerun()
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], use_container_width=True)

def module_manutencao():
    st.header("🔧 Manutenção")
    col_f, col_b = st.columns([1, 2])
    
    with col_f:
        st.subheader("Abertura de Chamado")
        with st.form("form_os", clear_on_submit=True):
            lista_s = st.session_state['stands']['Nome do Stand'].tolist()
            stand = st.selectbox("Stand", lista_s if lista_s else ["Nenhum cadastrado"])
            desc = st.text_area("Descrição")
            prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                nova_os = pd.DataFrame([{"ID": new_id, "Stand": stand, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                st.session_state['chamados'] = pd.concat([st.session_state['chamados'], nova_os], ignore_index=True)
                st.success("OS Aberta!")
                st.rerun()
                    
    with col_b:
        st.subheader("Backlog de Manutenção")
        # CONFIGURAÇÃO DA TABELA: Apenas status é editável
        st.session_state['chamados'] = st.data_editor(
            st.session_state['chamados'],
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"],
                    required=True,
                ),
                "ID": st.column_config.Column(disabled=True),
                "Stand": st.column_config.Column(disabled=True),
                "Descrição": st.column_config.Column(disabled=True),
                "Prioridade": st.column_config.Column(disabled=True),
            },
            hide_index=True,
            use_container_width=True
        )

        # SEÇÃO DE SOLICITAÇÃO DE MATERIAL (CARD/POPOVER)
        with st.popover("Solicitar Material ao Setor de Compras 📦", use_container_width=True):
            st.markdown("### Nova Requisição de Material")
            with st.form("form_material", clear_on_submit=True):
                # Seleção de OS
                lista_os = st.session_state['chamados']['ID'].tolist()
                os_ref = st.selectbox("Selecione a OS de referência", lista_os if lista_os else ["Nenhuma OS aberta"])
                
                # Número do Item automático
                proximo_item = len(st.session_state['solicitacoes_material']) + 1
                st.info(f"Item Número: {proximo_item}")
                
                mat = st.text_input("Material/Ferramenta")
                qtd = st.number_input("Quantidade", min_value=1, step=1)
                
                if st.form_submit_button("Enviar para Compras"):
                    st.session_state['solicitacoes_material'].append({
                        "Item": proximo_item, "OS": os_ref, "Material": mat, "Qtd": qtd, "Data": datetime.date.today()
                    })
                    st.success(f"Item {proximo_item} solicitado com sucesso!")

# --- MAIN ---
def main():
    if not st.session_state['autenticado']:
        tela_login()
    else:
        with st.sidebar:
            logo = carregar_logo()
            if logo: st.image(logo, use_container_width=True)
            st.divider()
            modulos = ["Painel de Gestão", "Cadastro", "Manutenção", "Financeiro", "Compras", "Inventário", "Marketing", "Escala do Time"]
            for mod in modulos:
                if st.button(mod, use_container_width=True, type="primary" if st.session_state['pagina_atual'] == mod else "secondary"):
                    st.session_state['pagina_atual'] = mod
                    st.rerun()
            if st.button("Sair", use_container_width=True):
                st.session_state['autenticado'] = False
                st.rerun()
                
        p = st.session_state['pagina_atual']
        if p == "Painel de Gestão": module_painel_gestao()
        elif p == "Cadastro": module_cadastro()
        elif p == "Manutenção": module_manutencao()
        else: st.title(p)

if __name__ == "__main__":
    main()
