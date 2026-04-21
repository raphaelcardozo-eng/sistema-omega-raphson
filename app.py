import streamlit as st
import pandas as pd
from PIL import Image
import datetime
import json
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Omega & Raphson ERP", layout="wide")

# --- SISTEMA DE PERSISTÊNCIA (BANCO DE DADOS JSON) ---
DB_FILE = "database_erp.json"

def salvar_dados():
    try:
        dados = {
            "usuarios": st.session_state['usuarios'].to_dict(orient="records"),
            "stands": st.session_state['stands'].to_dict(orient="records"),
            "centros": st.session_state['centros_custo'].to_dict(orient="records"),
            "departamentos": st.session_state['departamentos'].to_dict(orient="records"),
            "chamados": st.session_state['chamados'].to_dict(orient="records"),
            "materiais": st.session_state['solicitacoes_material']
        }
        with open(DB_FILE, "w") as f:
            json.dump(dados, f, default=str)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

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
        st.session_state['usuarios'] = pd.DataFrame([{"Nome": "Raphael Cardozo", "Email": "raphael@raphson.com.br", "Perfil": "Diretor", "Status": "Ativo"}])
        st.session_state['stands'] = pd.DataFrame(columns=["Nome do Stand", "Endereço", "Status"])
        st.session_state['centros_custo'] = pd.DataFrame(columns=["Nome do Centro de Custo", "CNPJ", "Status"])
        st.session_state['departamentos'] = pd.DataFrame(columns=["Nome do Departamento", "Responsável", "Status"])
        st.session_state['chamados'] = pd.DataFrame(columns=["ID", "Stand", "Descrição", "Status", "Prioridade"])
        st.session_state['solicitacoes_material'] = []

# --- INTERFACE ---
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
        st.session_state['usuarios'] = st.data_editor(st.session_state['usuarios'], num_rows="dynamic", use_container_width=True, key="u")
        if st.button("Salvar Usuários"): salvar_dados(); st.success("Salvo!")

    with tab2:
        st.session_state['stands'] = st.data_editor(st.session_state['stands'], num_rows="dynamic", use_container_width=True, key="s")
        if st.button("Salvar Stands"): salvar_dados(); st.success("Salvo!")

    with tab3:
        st.session_state['centros_custo'] = st.data_editor(st.session_state['centros_custo'], num_rows="dynamic", use_container_width=True, key="c")
        if st.button("Salvar Centros de Custo"): salvar_dados(); st.success("Salvo!")

    with tab4:
        st.session_state['departamentos'] = st.data_editor(st.session_state['departamentos'], num_rows="dynamic", use_container_width=True, key="d")
        if st.button("Salvar Departamentos"): 
            salvar_dados()
            st.success("Departamentos salvos no banco de dados!")

def module_manutencao():
    st.header("🔧 Manutenção")
    col_f, col_b = st.columns([1, 2])
    with col_f:
        st.subheader("Abertura de Chamado")
        with st.form("f_os", clear_on_submit=True):
            lista = st.session_state['stands']['Nome do Stand'].tolist()
            st_sel = st.selectbox("Stand", lista if lista else ["-"])
            desc = st.text_area("Descrição")
            prio = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente"])
            if st.form_submit_button("Abrir OS"):
                new_id = f"OS-{len(st.session_state['chamados']) + 1:03d}"
                n_os = pd.DataFrame([{"ID": new_id, "Stand": st_sel, "Descrição": desc, "Status": "Aguardando atendimento", "Prioridade": prio}])
                st.session_state['chamados'] = pd.concat([st.session_state['chamados'], n_os], ignore_index=True)
                salvar_dados(); st.rerun()
    with col_b:
        st.subheader("Backlog")
        edit = st.data_editor(st.session_state['chamados'], column_config={"Status": st.column_config.SelectboxColumn("Status", options=["Aguardando atendimento", "Em andamento", "Aguardando Material", "Concluído", "Cancelada"]), "ID": st.column_config.Column(disabled=True)}, hide_index=True, use_container_width=True)
        if not edit.equals(st.session_state['chamados']):
            st.session_state['chamados'] = edit
            salvar_dados()

# --- MAIN ---
def main():
    if not st.session_state['autenticado']:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            exibir_logo()
            user = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            if st.button("Entrar", use_container_width=True):
                if senha == "1234": st.session_state['autenticado'] = True; st.rerun()
    else:
        with st.sidebar:
            exibir_logo()
            st.divider()
            if st.button("📊 Painel de Gestão", use_container_width=True): st.session_state['pagina_atual'] = "Painel de Gestão"
            if st.button("🔧 Manutenção", use_container_width=True): st.session_state['pagina_atual'] = "Manutenção"
            if st.button("📝 Cadastros", use_container_width=True): st.session_state['pagina_atual'] = "Cadastro"
            st.divider()
            # ÁREA DE SEGURANÇA CONTRA PERDA DE DADOS
            with st.expander("💾 Backup de Segurança"):
                st.caption("Se os dados sumirem, cole o código de backup abaixo:")
                if st.button("Gerar Código de Backup"):
                    bkp = {
                        "usuarios": st.session_state['usuarios'].to_dict(orient="records"),
                        "stands": st.session_state['stands'].to_dict(orient="records"),
                        "centros": st.session_state['centros_custo'].to_dict(orient="records"),
                        "departamentos": st.session_state['departamentos'].to_dict(orient="records"),
                        "chamados": st.session_state['chamados'].to_dict(orient="records"),
                        "materiais": st.session_state['solicitacoes_material']
                    }
                    st.code(json.dumps(bkp))
            if st.button("Sair"): st.session_state['autenticado'] = False; st.rerun()

        if st.session_state['pagina_atual'] == "Manutenção": module_manutencao()
        elif st.session_state['pagina_atual'] == "Cadastro": module_cadastro()
        else: st.title("📊 Painel de Gestão")

if __name__ == "__main__":
    main()
