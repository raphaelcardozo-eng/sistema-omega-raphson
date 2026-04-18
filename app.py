import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import json
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA ---
DB_FILE = "database_erp.json"

def salvar_dados():
    dados = {
        "usuarios": st.session_state['usuarios'].to_dict(orient="records"),
        "stands": st.session_state['stands'].to_dict(orient="records"),
        "centros": st.session_state['centros_custo'].to_dict(orient="records"),
        "departamentos": st.session_state['departamentos'].to_dict(orient="records"), # Persistindo Departamentos
        "chamados": st.session_state['chamados'].to_dict(orient="records"),
        "materiais": st.session_state['solicitacoes_material']
    }
    with open(DB_FILE, "w") as f:
        json.dump(dados, f, default=str)

def carregar_dados():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                dados = json.load(f)
                st.session_state['usuarios'] = pd.DataFrame(dados.get("usuarios", []))
                st.session_state['stands'] = pd.DataFrame(dados.get("stands", []))
                st.session_state['centros_custo'] = pd.DataFrame(dados.get("centros", []))
                st.session_state['departamentos'] = pd.DataFrame(dados.get("departamentos", []))
                st.session_state['chamados'] = pd.DataFrame(dados.get("chamados", []))
                st.session_state['solicitacoes_material'] = dados.get("materiais", [])
                return True
        except:
            return False
    return False

# --- INICIALIZAÇÃO ---
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    st.session_state['pagina_atual'] = "Painel de Gestão"
    
    if not carregar_dados():
        # Dados padrão caso o arquivo não exista
        st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphaelcardozo@raphsonengenharia.com.br", "Perfil": "Diretor", "Senha": "1234", "Status": "Ativo"}])
        st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Status"])
        st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Status"])
        st.session_state['departamentos'] = pd.DataFrame(columns=["Nome do Departamento", "Responsável", "Status"])
        st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
        st.session_state['solicitacoes_material'] = []

# --- FUNÇÕES DE INTERFACE ---
def exibir_logo():
    try:
        img = Image.open("Image_from_Image.jpg")
        st.sidebar.image(img, use_container_width=True)
    except:
        st.sidebar.subheader("Omega & Raphson")

def module_cadastro():
    st.header("📝 Gestão de Cadastros")
    tab1, tab2, tab3, tab4 = st.tabs(["Usuários", "Stands", "Centros de Custo", "Departamentos"])
    
    with tab1:
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="ed_u")
        if st.button("Salvar Usuários"): salvar_dados(); st.success("Salvo!")

    with tab2:
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="ed_s")
        if st.button("Salvar Stands"): salvar_dados(); st.success("Salvo!")

    with tab3:
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], num_rows="dynamic", use_container_width=True, key="ed_c")
        if st.button("Salvar Centros de Custo"): salvar_dados(); st.success("Salvo!")

    with tab4:
        # Recuperando a funcionalidade de Departamentos
        st.session_state['departamentos'] = st.data_editor(st.session_state['departamentos'], num_rows="dynamic", use_container_width=True, key="ed_d")
        if st.button("Salvar Departamentos"):
            salvar_dados()
            st.success("Departamentos atualizados e protegidos!")

# --- MÓDULO DE MANUTENÇÃO (CONFORME SOLICITADO) ---
def module_manutencao():
    st.header("🔧 Manutenção")
    col_f, col_b = st.columns([1, 2])
    
    with col_f:
        st.subheader("Abertura de Chamado")
        with st.form("form_os", clear_on_submit=True):
            lista_s = st.session_state['stands']['Nome do Stand'].tolist()
            stand = st.selectbox("Stand", lista_s if lista_s else ["Nenhum"])
            desc = st.text_area("Descrição")
            prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                nova_os = pd.DataFrame([{"ID": new_id, "Stand": stand, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                st.session_state['chamados'] = pd.concat([st.session_state['chamados'], nova_os], ignore_index=True)
                salvar_dados()
                st.rerun()
                    
    with col_b:
        st.subheader("Backlog de Manutenção")
        # Campos de texto bloqueados, apenas Status editável
        df_edit = st.data_editor(
            st.session_state['chamados'],
            column_config={
                "Status": st.column_config.SelectboxColumn("Status", options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"]),
                "ID": st.column_config.Column(disabled=True),
                "Stand": st.column_config.Column(disabled=True),
                "Descrição": st.column_config.Column(disabled=True)
            },
            hide_index=True, use_container_width=True, key="edit_os"
        )
        if not df_edit.equals(st.session_state['chamados']):
            st.session_state['chamados'] = df_edit
            salvar_dados()

        with st.popover("Solicitar Material 📦", use_container_width=True):
            with st.form("f_mat", clear_on_submit=True):
                ids = st.session_state['chamados']['ID'].tolist()
                os_ref = st.selectbox("OS", ids if ids else ["-"])
                item_n = len(st.session_state['solicitacoes_material']) + 1
                mat = st.text_input(f"Item {item_n} - Material")
                qtd = st.number_input("Qtd", min_value=1)
                if st.form_submit_button("Confirmar"):
                    st.session_state['solicitacoes_material'].append({"Item": item_n, "OS": os_ref, "Material": mat, "Qtd": qtd})
                    salvar_dados()
                    st.success("Solicitação salva!")

# --- LOGIN E NAVEGAÇÃO ---
def main():
    if not st.session_state['autenticado']:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.title("Login")
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if senha == "1234":
                    st.session_state['autenticado'] = True
                    st.rerun()
    else:
        with st.sidebar:
            exibir_logo()
            st.divider()
            if st.button("📊 Painel de Gestão", use_container_width=True): st.session_state['pagina_atual'] = "Painel de Gestão"
            if st.button("🔧 Manutenção", use_container_width=True): st.session_state['pagina_atual'] = "Manutenção"
            if st.button("📝 Cadastros", use_container_width=True): st.session_state['pagina_atual'] = "Cadastro"
            st.divider()
            if st.button("Sair"): st.session_state['autenticado'] = False; st.rerun()

        if st.session_state['pagina_atual'] == "Manutenção": module_manutencao()
        elif st.session_state['pagina_atual'] == "Cadastro": module_cadastro()
        else: st.title("📊 Painel de Gestão")

if
